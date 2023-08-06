from optel.datalake import provision
import googleapiclient.discovery
import pytest
import os


@pytest.fixture()
def provision_file():
    return "provision/dataproc.sh"


@pytest.fixture()
def config_file():
    return "provision/cluster-data.yml"


@pytest.mark.skip(reason="We do not want to test this on every push")
def test_create_machines():
    compute = googleapiclient.discovery.build('compute', 'v1')
    tf_config = "test_gc"
    project = "optel-data-lab"
    zone = "us-east1-d"
    instance = "test-terraform"
    provision.create_machines(tf_config)
    request = compute.instances().get(
        project=project, zone=zone, instance=instance)
    assert request.execute()
    provision.destroy_machines(tf_config)


def test_get_dataproc_client(mocker):
    mocker.patch(
        "optel.datalake.provision.googleapiclient.discovery.build")
    provision.get_dataproc_client()
    provision.googleapiclient.discovery.build \
        .assert_called_once_with('dataproc', 'v1')


@pytest.mark.skip("Does not work on the datalake-swimmer runners")
def test_upload_config(mocker, provision_file):
    mocker.patch("optel.datalake.provision.storage.Client.get_bucket")
    provision.upload_config(provision_file)

    provision.storage.Client.get_bucket.assert_called_once_with(
        "instances-provisioning")
    assert os.path.exists(provision_file)


def test_read_cluster_data(config_file):
    cluster_data = provision.read_cluster_data(config_file)
    assert cluster_data != ""
