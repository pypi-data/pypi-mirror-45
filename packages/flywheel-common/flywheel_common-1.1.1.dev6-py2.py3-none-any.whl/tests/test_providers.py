from marshmallow import exceptions
from mock import patch
import pytest

from flywheel_common.providers import ProviderClass
from flywheel_common.providers.creds import Creds
from flywheel_common.providers.provider import BaseProvider
from flywheel_common.providers.storage.base import BaseStorageProvider
from flywheel_common.providers.compute.base import BaseComputeProvider


# === Model Tests ===
def test_creds():

    cred_test = Creds(
        provider_class='test',
        provider_type='anything',
        provider_label='Test creds',
        config=None)

    assert cred_test.provider_class == 'test'
    assert cred_test.provider_type == 'anything'
    assert cred_test.label == 'Test creds'

    # No schema
    with pytest.raises(ValueError):
        cred_test.validate()

def test_provider():

    provider_test = BaseProvider(
        provider_class='test',
        provider_type='anything',
        provider_label='Test provider',
        config=None,
        creds=None)

    assert provider_test.provider_class == 'test'
    assert provider_test.provider_type == 'anything'
    assert provider_test.label == 'Test provider'

    # No schema
    with pytest.raises(ValueError):
        provider_test.validate()
def test_storage_provider(mocker):

    mocker.patch('flywheel_common.providers.storage.base.create_flywheel_fs', return_value={'storage': 'test'})
    provider_test = BaseStorageProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider',
        config={'path': '/var/'},
        creds=None)

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.storage_plugin == {'storage': 'test'}

    # No schema
    with pytest.raises(ValueError):
        provider_test.validate()


def test_compute_provider(mocker):

    # TODO: extend this once its implemented
    assert True
