# Copyright 2018 Google LLC
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

from __future__ import print_function

import argparse
import json
import os

from google.cloud import monitoring_v3
import google.protobuf.json_format
import tabulate
import pprint


def create_uptime_check_config(project_name, host_name=None, display_name=None):
    config = monitoring_v3.types.uptime_pb2.UptimeCheckConfig()
    config.display_name = display_name or 'New uptime check'
    config.monitored_resource.type = 'uptime_url'
    config.monitored_resource.labels.update(
        {'host': host_name or 'example.com'})
    config.http_check.path = '/'
    config.http_check.port = 80
    config.timeout.seconds = 10
    config.period.seconds = 300

    client = monitoring_v3.UptimeCheckServiceClient()
    new_config = client.create_uptime_check_config(project_name, config)
    pprint.pprint(new_config)


def list_uptime_check_configs(project_name):
    client = monitoring_v3.UptimeCheckServiceClient()
    configs = client.list_uptime_check_configs(project_name)
    for config in configs:
        pprint.pprint(config)        


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


def project_name():
    return 'projects/' + project_id()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Demonstrates Uptime Check API operations.')

    subparsers = parser.add_subparsers(dest='command')

    list_uptime_check_configs_parser = subparsers.add_parser(
        'list-uptime-check-configs',
        help=list_uptime_check_configs.__doc__
    )

    create_uptime_check_config_parser = subparsers.add_parser(
        'create-uptime-check',
        help=create_uptime_check_config.__doc__
    )
    create_uptime_check_config_parser.add_argument(
        '-d', '--display_name',
        required=False,
    )
    create_uptime_check_config_parser.add_argument(
        '-o', '--host_name',
        required=False,
    )

    args = parser.parse_args()

    if args.command == 'list-uptime-check-configs':
        list_uptime_check_configs(project_name())

    elif args.command == 'create-uptime-check':
        create_uptime_check_config(project_name(), args.host_name, 
                                   args.display_name)
