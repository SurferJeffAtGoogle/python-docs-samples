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

def list_alert_policies():
    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(project())
    for policy in policies:
        print(policy.display_name or policy.name)

class MissingProjectIdError(Exception):
    pass

def project():
    project_id = os.environ['GCLOUD_PROJECT']
    if not project_id:
        raise MissingProjectIdError('Set the environment variable ' +
            'GCLOUD_PROJECT to your Google Cloud Project Id.')
    return 'projects/' + project_id

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Demonstrates AlertPolicy API operations.')

    subparsers = parser.add_subparsers(dest='command')

    list_alert_policies_parser = subparsers.add_parser(
        'list-alert-policies',
        help=list_alert_policies.__doc__
    )

    args = parser.parse_args()

    if args.command == 'list-alert-policies':
        list_alert_policies()
