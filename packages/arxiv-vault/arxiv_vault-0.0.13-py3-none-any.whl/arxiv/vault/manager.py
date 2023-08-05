"""Provides :class:`.SecretsManager`."""

from typing import List, Dict, Tuple, Iterable, Optional
from dataclasses import dataclass

from datetime import datetime, timedelta
from pytz import UTC

import logging

from .core import Vault, Secret

logger = logging.getLogger(__name__)
logger.propagate = False

MYSQL = 'mysql'


@dataclass
class SecretRequest:
    """Represents a request for a secret from Vault."""

    name: str

    @classmethod
    def factory(cls, request_type: str, **data: str) -> 'SecretRequest':
        """Genereate a request of the appropriate type."""
        for klass in cls.__subclasses__():
            if klass.slug == request_type:
                return klass(**data)
        raise ValueError('No such request type')


@dataclass
class AWSSecretRequest(SecretRequest):
    """Represents a request for AWS credentials."""

    slug = "aws"

    role: str
    """An AWS role that has been pre-configured with IAM policies in Vault."""


@dataclass
class DatabaseSecretRequest(SecretRequest):
    """Represents a request for database credentials."""

    slug = "database"

    endpoint: str
    """Name of the Vault database secrets endpoint."""

    role: str
    """Name of the database role for which to obtain credentials."""

    engine: str
    """
    Database dialect for which secret is required, e.g. ``mysql+mysqldb``.

    See https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls
    """

    host: str
    """Hostname of the database server."""

    port: str
    """Port number of the database server."""

    database: str
    """Name of the database."""

    params: str
    """Param-part of the database URI connection string."""


@dataclass
class GenericSecretRequest(SecretRequest):
    """Represents a request for a generic (kv) secret."""

    slug = "generic"

    mount_point: str
    """Mount point of the KV engine."""

    path: str
    """Path to the secret."""

    key: str
    """Key within the secret."""

    minimum_ttl: int = 0
    """Renewal will be attempted no more frequently than ``minimum_ttl``."""


class SecretsManager:
    """
    Fulfills requests for Vault secrets, and manages renewal transparently.

    A typical use case for working with Vault secrets is that we want to
    generate some configuration variables for use at run-time. For example,
    in a Flask application we want things like secret keys and sensitive
    database URIs to be available in the application config when handling a
    request. The goal of the secrets manager is to fulfill requests for
    secrets that will be used in that kind of key-value paradigm.

    The manager should only call Vault if the secret has not been retrieved
    yet, or if the secret is expired or about to expire.

    A request is a description of the secret that is desired and (depending on
    its type) the form in which it should be returned.

    Should be one of:

    - :class:`.AWSSecretRequest`
    - :class:`.DatabaseSecretRequest`
    - :class:`.GenericSecretRequest`

    """

    def __init__(self, vault: Vault, requests: List[SecretRequest],
                 expiry_margin: int = 300) -> None:
        """Initialize a new manager with :class:`.Vault` connection."""
        self.vault = vault
        self.requests = requests
        self.secrets: Dict[str, Secret] = {}
        self.expiry_margin = timedelta(seconds=expiry_margin)

    def _about_to_expire(self, secret: Secret) -> bool:
        """Check if a secret is about to expire within `margin` seconds."""
        return secret.is_expired(datetime.now(UTC) + self.expiry_margin)

    def _format_database(self, request: DatabaseSecretRequest,
                         secret: Secret) -> str:
        """Format a database secret."""
        username, password = secret.value
        return f'{request.engine}://{username}:{password}@' \
               f'{request.host}:{request.port}/{request.database}?' \
               f'{request.params}'

    def _fresh_secret(self, request: SecretRequest) -> Secret:
        """Get a brand new secret."""
        if type(request) is AWSSecretRequest:
            secret = self.vault.aws(request.role)
        elif type(request) is DatabaseSecretRequest:
            if request.engine.split('+', 1)[0] == MYSQL:
                secret = self.vault.mysql(request.role, request.endpoint)
            else:
                raise NotImplementedError('No other database engine available')
        elif type(request) is GenericSecretRequest:
            secret = self.vault.generic(request.path, request.key,
                                        request.mount_point)
        return secret

    def _can_freshen(self, request: SecretRequest, secret: Secret) -> bool:
        """Enforce minimum TTL."""
        if not hasattr(request, 'minimum_ttl'):
            return True
        age = (datetime.now(UTC) - secret.issued).total_seconds()
        return age >= request.minimum_ttl

    def _is_stale(self, request: SecretRequest,
                  secret: Optional[Secret]) -> bool:
        """Determine whether or not a secret requires renewal."""
        return secret is None or \
            (secret.is_expired() and self._can_freshen(request, secret))

    def _get_secret(self, request: SecretRequest) -> Secret:
        """Get a secret for a :class:`.SecretRequest`."""
        secret = self.secrets.get(request.name, None)
        if self._is_stale(request, secret):
            secret = self._fresh_secret(request)
        elif self._about_to_expire(secret):
            if secret.renewable:
                secret = self.vault.renew(secret)
            else:
                secret = self._fresh_secret(request)
        self.secrets[request.name] = secret
        return secret

    def yield_secrets(self, tok: str, role: str) -> Iterable[Tuple[str, str]]:
        """Generate config var + secret tuples."""
        # Make sure that we have a current authentication with vault.
        if not self.vault.authenticated:
            self.vault.authenticate(tok, role)

        for request in self.requests:
            secret = self._get_secret(request)
            if type(request) is AWSSecretRequest:
                yield 'AWS_ACCESS_KEY_ID', secret.value[0]
                yield 'AWS_SECRET_ACCESS_KEY', secret.value[1]
            elif type(request) is DatabaseSecretRequest:
                yield request.name, self._format_database(request, secret)
            elif type(request) is GenericSecretRequest:
                yield request.name, secret.value
