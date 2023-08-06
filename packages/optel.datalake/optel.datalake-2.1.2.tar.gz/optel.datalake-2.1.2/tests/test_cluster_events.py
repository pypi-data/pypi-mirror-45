from optel.datalake import cluster_events
import pytest

project = "optel-data-lab"
zone = "us-east1-b"
cluster = "transformations-cluster"


@pytest.mark.skip("Does not work on the datalake-swimmer.")
def test_get_instances_names(gc_instances):
    instances = cluster_events.get_instances_names(project, zone, cluster)
    print(instances[1])
    assert "runner" not in instances
    assert instances[1] != ""


def test_boot_cluster(mocker, instances_names):
    """"""
    mocker.patch("optel.datalake.cluster_events.googleapiclient.discovery.build")

    cluster_events.boot_cluster(instances_names, "", "")
    cluster_events.googleapiclient.discovery.build.assert_called_once_with('compute', 'v1')

    calls = [mocker.call(project="", zone="", instance=name) for name in instances_names]
    assert cluster_events.googleapiclient.discovery.build().instances.call_count == 3
    cluster_events.googleapiclient.discovery.build().instances().start.assert_has_calls(calls, any_order=True)


def test_shutdown_cluster_job_running(mocker, instances_names):
    mocker.patch("optel.datalake.cluster_events.googleapiclient.discovery.build")
    mocker.patch("optel.datalake.cluster_events.subprocess.check_output")
    cluster_events.subprocess.check_output.return_value = b"JOB_ID 1111"

    cluster_events.shutdown_cluster(instances_names, "", "", "")
    cluster_events.googleapiclient.discovery.build.assert_called_once_with('compute', 'v1')
    cluster_events.googleapiclient.discovery.build().instances.assert_not_called()


def test_shutdown_cluster_no_job_running(mocker, instances_names):
    mocker.patch("optel.datalake.cluster_events.googleapiclient.discovery.build")
    mocker.patch("optel.datalake.cluster_events.subprocess.check_output")
    cluster_events.subprocess.check_output.return_value = b""

    cluster_events.shutdown_cluster(instances_names, "", "", "")
    cluster_events.googleapiclient.discovery.build.assert_called_once_with('compute', 'v1')
    calls = [mocker.call(project="", zone="", instance=name) for name in
             instances_names]
    assert cluster_events.googleapiclient.discovery.build().instances.call_count == 3
    cluster_events.googleapiclient.discovery.build().instances().stop.assert_has_calls(
        calls, any_order=True)
