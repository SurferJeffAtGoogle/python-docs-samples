# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import argparse
import os
import pprint

from google.cloud import monitoring_v3


def create_metric_descriptor(project_id):
    # [START monitoring_create_metric]
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)
    descriptor = monitoring_v3.types.MetricDescriptor()
    descriptor.type = 'custom.googleapis.com/my_metric'
    descriptor.metric_kind = (
        monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE)
    descriptor.value_type =  (
        monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE)
    descriptor.description = 'This is a simple example of a custom metric.'
    descriptor = client.create_metric_descriptor(project_name, descriptor)
    print('Created {}.'.format(descriptor.name))    
    # [END monitoring_create_metric]


def delete_metric_descriptor(descriptor_name):
    # [START monitoring_delete_metric]
    client = monitoring_v3.MetricServiceClient()
    client.delete_metric_descriptor(descriptor_name)
    print('Deleted metric descriptor {}.'.format(descriptor_name))
    # [END monitoring_delete_metric]


def write_time_series():
    # [START monitoring_write_timeseries]
    client = monitoring.Client()
    resource = client.resource(
        'gce_instance',
        labels={
            'instance_id': '1234567890123456789',
            'zone': 'us-central1-f',
        }
    )

    metric = client.metric(
        type_='custom.googleapis.com/my_metric',
        labels={
        }
    )
    client.write_point(metric, resource, 3.14)
    # [END monitoring_write_timeseries]


def list_time_series():
    # [START monitoring_read_timeseries_simple]
    client = monitoring.Client()
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    query_results = client.query(metric, minutes=5)
    for result in query_results:
        print(result)
    # [END monitoring_read_timeseries_simple]


def list_time_series_header():
    # [START monitoring_read_timeseries_fields]
    client = monitoring.Client()
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    query_results = client.query(metric, minutes=5).iter(headers_only=True)
    for result in query_results:
        print(result)
    # [END monitoring_read_timeseries_fields]


def list_time_series_aggregate():
    # [START monitoring_read_timeseries_align]
    client = monitoring.Client()
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    query_results = client.query(metric, hours=1).align(
        monitoring.Aligner.ALIGN_MEAN, minutes=5)
    for result in query_results:
        print(result)
    # [END monitoring_read_timeseries_align]


def list_time_series_reduce():
    # [START monitoring_read_timeseries_reduce]
    client = monitoring.Client()
    metric = 'compute.googleapis.com/instance/cpu/utilization'
    query_results = client.query(metric, hours=1).align(
        monitoring.Aligner.ALIGN_MEAN, minutes=5).reduce(
        monitoring.Reducer.REDUCE_MEAN, 'resource.zone')
    for result in query_results:
        print(result)
    # [END monitoring_read_timeseries_reduce]


def list_metric_descriptors(project_id):
    # [START monitoring_list_descriptors]
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)
    for descriptor in client.list_metric_descriptors(project_name):
        print(descriptor.type)
    # [END monitoring_list_descriptors]


def list_monitored_resources():
    # [START monitoring_list_resources]
    client = monitoring.Client()
    for descriptor in client.list_resource_descriptors():
        print(descriptor.type)
    # [END monitoring_list_resources]


def get_monitored_resource_descriptor(resource_type_name):
    # [START monitoring_get_resource]
    client = monitoring.Client()
    print(client.fetch_resource_descriptor(resource_type_name))
    # [END monitoring_get_resource]


def get_metric_descriptor(metric_name):
    # [START monitoring_get_descriptor]
    client = monitoring_v3.MetricServiceClient()
    descriptor = client.get_metric_descriptor(metric_name)
    pprint.pprint(descriptor)
    # [END monitoring_get_descriptor]


class MissingProjectIdError(Exception):
    pass


def project_id():
    """Retreieves the project id from the environment variable.

    Raises:
        MissingProjectIdError -- When not set.

    Returns:
        str -- the project name
    """
    project_id = os.environ['GCLOUD_PROJECT']

    if not project_id:
        raise MissingProjectIdError(
            'Set the environment variable ' +
            'GCLOUD_PROJECT to your Google Cloud Project Id.')
    return project_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Demonstrates Monitoring API operations.')

    subparsers = parser.add_subparsers(dest='command')

    create_metric_descriptor_parser = subparsers.add_parser(
        'create-metric-descriptor',
        help=create_metric_descriptor.__doc__
    )

    list_metric_descriptor_parser = subparsers.add_parser(
        'list-metric-descriptors',
        help=list_metric_descriptors.__doc__
    )

    get_metric_descriptor_parser = subparsers.add_parser(
        'get-metric-descriptor',
        help=get_metric_descriptor.__doc__
    )

    get_metric_descriptor_parser.add_argument(
        '--metric-type-name',
        help='The metric type of the metric descriptor to see details about.',
        required=True
    )

    delete_metric_descriptor_parser = subparsers.add_parser(
        'delete-metric-descriptor',
        help=list_metric_descriptors.__doc__
    )

    delete_metric_descriptor_parser.add_argument(
        '--metric-descriptor-name',
        help='Metric descriptor to delete',
        required=True
    )

    list_resources_parser = subparsers.add_parser(
        'list-resources',
        help=list_monitored_resources.__doc__
    )

    get_resource_parser = subparsers.add_parser(
        'get-resource',
        help=get_monitored_resource_descriptor.__doc__
    )

    get_resource_parser.add_argument(
        '--resource-type-name',
        help='Monitored resource to view more information about.',
        required=True
    )

    write_time_series_parser = subparsers.add_parser(
        'write-time-series',
        help=write_time_series.__doc__
    )

    list_time_series_parser = subparsers.add_parser(
        'list-time-series',
        help=list_time_series.__doc__
    )

    list_time_series_header_parser = subparsers.add_parser(
        'list-time-series-header',
        help=list_time_series_header.__doc__
    )

    read_time_series_reduce = subparsers.add_parser(
        'list-time-series-reduce',
        help=list_time_series_reduce.__doc__
    )

    read_time_series_aggregate = subparsers.add_parser(
        'list-time-series-aggregate',
        help=list_time_series_aggregate.__doc__
    )

    args = parser.parse_args()

    if args.command == 'create-metric-descriptor':
        create_metric_descriptor(project_id())
    if args.command == 'list-metric-descriptors':
        list_metric_descriptors(project_id())
    if args.command == 'get-metric-descriptor':
        get_metric_descriptor(args.metric_type_name)
    if args.command == 'delete-metric-descriptor':
        delete_metric_descriptor(args.metric_descriptor_name)
    if args.command == 'list-resources':
        list_monitored_resources()
    if args.command == 'get-resource':
        get_monitored_resource_descriptor(args.resource_type_name)
    if args.command == 'write-time-series':
        write_time_series()
    if args.command == 'list-time-series':
        list_time_series()
    if args.command == 'list-time-series-header':
        list_time_series_header()
    if args.command == 'list-time-series-reduce':
        list_time_series_reduce()
    if args.command == 'list-time-series-aggregate':
        list_time_series_aggregate()
