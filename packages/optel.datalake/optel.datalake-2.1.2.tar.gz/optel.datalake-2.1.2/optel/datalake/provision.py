from python_terraform import Terraform
import os
import googleapiclient.discovery
from google.cloud import storage
import yaml

provision_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "provision")


def create_machines(config):
    """Create and provision machines with *terraform*.

    Args:
        config (str): Terraform configuration dir. The
                    directory is used to store the config
                    file as well as Terraform specific stuff.
                    .. note::

                        Each directory has to be cloud provider specific.
    """
    kwargs = {"auto-approve": True}
    config_dir = os.path.join(provision_dir, config)
    tf = Terraform(working_dir=config_dir)
    tf.init()
    tf.apply(config_dir, capture_output=False, **kwargs)


def destroy_machines(config):
    """Destroy machines with *terraform*.

    Args:
        config(str): Terraform configuration dir to use.
    """
    kwargs = {"auto-approve": True}
    config_dir = os.path.join(provision_dir, config)
    tf = Terraform(working_dir=config_dir)
    tf.destroy(capture_output=False, **kwargs)


def get_dataproc_client():
    """
    Builds a client to the dataproc API.
    """
    dataproc = googleapiclient.discovery.build('dataproc', 'v1')
    return dataproc


def upload_config(provision_file):
    """
    Upload the provisioning file (initialization action) to a GC bucket.

    Args:
        provision_file (str): The provisioning file containing commands to
                           execute after creating a cluster.
    """
    storage_client = storage.Client()
    bucket_name = "instances-provisioning"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(provision_file)
    blob.upload_from_filename(provision_file)


def read_cluster_data(config_file):
    """
    Reads all cluster data from a yaml file.

    Args:
        config_file
    """
    config = open(config_file, 'r')
    cluster_data = yaml.load(config)
    return cluster_data
