import os
import json

from typing import Union

from google.oauth2 import service_account
from google.auth import compute_engine

from google.cloud import storage
from injector import inject

from gumo.core.exceptions import ServiceAccountConfigurationError
from gumo.core.injector import injector
from gumo.core.domain.configuration import GumoConfiguration


Credentials = Union[service_account.Credentials, compute_engine.Credentials]


class GoogleOAuthCredentialManager:
    _credential = None

    @classmethod
    def get_credential(cls) -> Credentials:
        if cls._credential:
            return cls._credential

        cls._credential = injector.get(cls).build_credential()
        return cls._credential

    @inject
    def __init__(
            self,
            gumo_configuration: GumoConfiguration,
    ):
        self._gumo_configuration = gumo_configuration
        self._credential_config = self._gumo_configuration.service_account_credential_config

    def build_credential(self) -> Credentials:
        _credentials = None

        try:
            if self._gumo_configuration.is_google_app_engine:
                _credentials = compute_engine.Credentials()
            elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                _credentials = service_account.Credentials.from_service_account_info(
                    info=self._get_content_from_local()
                )
            elif self._credential_config.enabled:
                # will be deprecated.
                _credentials = service_account.Credentials.from_service_account_info(
                    info=self._get_content_from_storage()
                )
        except ServiceAccountConfigurationError:
            raise
        except RuntimeError as e:
            raise ServiceAccountConfigurationError(e)

        if _credentials is None:
            raise ServiceAccountConfigurationError(f'ServiceAccount Credential Config disabled.')

        return _credentials

    def _get_content_from_storage(self):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name=self._credential_config.bucket_name)
        blob = bucket.blob(blob_name=self._credential_config.blob_path)
        content = blob.download_as_string(client=storage_client)

        return json.loads(content)

    def _get_content_from_local(self):
        credential_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        if not os.path.exists(credential_path):
            raise ServiceAccountConfigurationError(f'GOOGLE_APPLICATION_CREDENTIALS={credential_path} is not found.')

        with open(credential_path, 'r') as f:
            content = f.read()

        return json.loads(content)


def get_google_oauth_credential() -> Credentials:
    return GoogleOAuthCredentialManager.get_credential()
