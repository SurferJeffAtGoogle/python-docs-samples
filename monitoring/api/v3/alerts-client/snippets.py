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


def list_alert_policies(project_name: str):
    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(project_name)
    for policy in policies:
        print(policy.display_name or policy.name)


def enable_alert_policies(project_name: str, enable, filter_: str = None):
    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(project_name, filter_=filter_)
    for policy in policies:
        if bool(enable) == policy.enabled.value:
            print('Policy', policy.name, 'is already',
                'enabled' if policy.enabled.value else 'disabled')
        else:
            policy.enabled.value = bool(enable)
            mask = monitoring_v3.types.field_mask_pb2.FieldMask()
            mask.paths.append('enabled')
            client.update_alert_policy(policy, mask)
            print('Enabled' if enable else 'Disabled', policy.name)


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
        raise MissingProjectIdError('Set the environment variable ' +
            'GCLOUD_PROJECT to your Google Cloud Project Id.')
    return project_id


def project_name():
    return 'projects/' + project_id()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Demonstrates AlertPolicy API operations.')

    subparsers = parser.add_subparsers(dest='command')

    list_alert_policies_parser = subparsers.add_parser(
        'list-alert-policies',
        help=list_alert_policies.__doc__
    )

    enable_alert_policies_parser = subparsers.add_parser(
        'enable-alert-policies',
        help=enable_alert_policies.__doc__
    )
    enable_alert_policies_parser.add_argument(
        '--filter',
    )

    disable_alert_policies_parser = subparsers.add_parser(
        'disable-alert-policies',
        help=enable_alert_policies.__doc__
    )
    disable_alert_policies_parser.add_argument(
        '--filter',
    )

    args = parser.parse_args()

    if args.command == 'list-alert-policies':
        list_alert_policies(project_name())

    if args.command == 'enable-alert-policies':
        enable_alert_policies(project_name(), enable=True, filter_=args.filter)

    if args.command == 'disable-alert-policies':
        enable_alert_policies(project_name(), enable=False, filter_=args.filter)
