import optel.datalake.bigquery as odbq

from pyspark.sql.types import DecimalType


def test_sanitize_decimals_for_bigquery(decimal_df):
    new_df = odbq.sanitize_datatypes_for_bigquery(decimal_df)
    for field in new_df.schema:
        assert isinstance(field.dataType, DecimalType)
        assert field.dataType.scale <= 9
        assert field.dataType.precision - field.dataType.scale <= 29


def test_create_bq_load_job_config(mocker):
    mocker.patch("optel.datalake.bigquery.bigquery.LoadJobConfig")
    config = odbq.create_bq_load_job_config("Hello", "World")
    assert config.source_format == "Hello"
    assert config.write_disposition == "World"


def test_cleanup(mocker):
    config = {
        'list_blobs.return_value': [mocker.MagicMock() for i in range(3)]
    }
    mocker.patch("optel.datalake.bigquery.get_storage_bucket", **config)
    odbq.get_storage_bucket.return_value = odbq.get_storage_bucket  # hack
    odbq.cleanup("", "", "")

    # verify each MagicMock delete mock was called once
    for mock in config['list_blobs.return_value']:
        assert mock.delete.call_count == 1


def test_sanitize_datatypes_for_bigquery(all_types_df):
    df = odbq.sanitize_datatypes_for_bigquery(all_types_df)
    assert 'decimal' not in [types[1] for types in df.dtypes]


def test_get_storage_bucket(mocker):
    client_mock = mocker.patch("optel.datalake.bigquery.storage.Client")
    odbq.get_storage_bucket("")
    client_mock.assert_called_once()
