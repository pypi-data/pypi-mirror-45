import click
import logging
from optel.datalake import cluster_events
from optel.datalake import provision
from optel.datalake import __version__, __project__


@click.group()
@click.version_option(__version__)
def main():
    logging.basicConfig(filename='info.log',
                        level=logging.INFO,
                        filemode='w')


@main.group()
def cluster():
    pass


@cluster.command()
@click.option('--project', help='Project where the instances are')
@click.option('--zone', help='Zone where the project exist')
@click.option('--cluster', help='Cluster to boot')
def boot(project, zone, cluster):
    """Boot a production cluster"""
    instances = cluster_events.get_instances_names(project, zone, cluster)[0]
    cluster_events.boot_cluster(instances, project, zone)


@cluster.command()
@click.option('--project', help='Project where the instances are')
@click.option('--zone', help='Zone where the project exist')
@click.option('--cluster', help='Cluster to kill')
def kill(project, zone, cluster):
    """
    Shutdown a production cluster.

    .. note::

       This will shutdown a cluster ONLY IF not active jobs are runnuing.
    """
    instances = cluster_events.get_instances_names(project, zone, cluster)[0]
    cluster_events.shutdown_cluster(instances, project, zone, cluster)


@cluster.command('create-elk')
@click.option('--config', help='Terraform configuration file to use')
def create_elk(config):
    """
    Create an Elastic Stack with Terraform.
    """
    provision.create_machines(config)


@cluster.command('create-dataproc-cluster')
@click.option('--provision_file', default="provision/dataproc.sh")
@click.option('--config_file', default="provision/cluster-data.yml")
@click.option('--cluster_name', default=None)
def create_dataproc_cluster(provision_file, config_file, cluster_name):
    """
    Create and deploy a dataproc cluster.

    Args:
        provision_file (str): The provisioning file where all the
                        configuration of the cluster is defined, as
                        machines type, number of workers, cluster name
                        ect...
    """
    cluster_data = provision.read_cluster_data(config_file)
    if cluster_name:
        cluster_data['clusterName'] = cluster_name
    provision.upload_config(provision_file)
    dataproc = provision.get_dataproc_client()
    print('Creating cluster...')
    print(cluster_data['config'])
    print(cluster_data['clusterName'])
    result = dataproc.projects().regions().clusters().create(
        projectId=cluster_data['projectId'],
        region="us-east1",
        body=cluster_data).execute()
    return result


@cluster.command('destroy-dataproc-cluster')
@click.option('--cluster_name')
@click.option('--project', default="optel-data-lab")
@click.option('--region', default="us-east1")
def destroy_dataproc_cluster(project, region, cluster_name):
    """
    Completely remove a Dataproc cluster.
    """
    print('Removing cluster')
    dataproc = provision.get_dataproc_client()
    result = dataproc.projects().regions().clusters().delete(
        projectId=project,
        region=region,
        clusterName=cluster_name).execute()
    return result


if __name__ == '__main__':
    main(progname=__project__)
