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

from gcp_devrel.testing import eventually_consistent

import snippets
import pytest
from google.cloud import monitoring_v3
import google.protobuf.json_format
import random
import string

def random_name(length):
    return ''.join([random.choice(string.ascii_lowercase) for i in range(length)])

class PochanFixture:
    """A test fixture that creates an alert POlicy and a notification CHANnel,
       hence the name, pochan.
    """

    def __init__(self):
        self.project_id = snippets.project_id()
        self.project_name = snippets.project_name()
        self.alert_policy_client = monitoring_v3.AlertPolicyServiceClient()
        self.notification_channel_client = (
            monitoring_v3.NotificationChannelServiceClient())
    
    def __enter__(self):
        # Create a policy.
        policy = monitoring_v3.types.alert_pb2.AlertPolicy()
        json = open('test_alert_policy.json').read()
        google.protobuf.json_format.Parse(json, policy)
        policy.display_name = 'snippets-test-' + random_name(10)
        self.alert_policy = self.alert_policy_client.create_alert_policy(
            self.project_name, policy)
        # Create a notification channel.
        notification_channel = (
            monitoring_v3.types.notification_pb2.NotificationChannel())
        json = open('test_notification_channel.json').read()
        google.protobuf.json_format.Parse(json, notification_channel)
        notification_channel.display_name = 'snippets-test-' + random_name(10)
        self.notification_channel = (
            self.notification_channel_client.create_notification_channel(
                self.project_name, notification_channel))
        return self

    def __exit__(self, type, value, traceback):
        # Delete the policy and channel we created.
        self.notification_channel_client.delete_notification_channel(
            self.notification_channel.name)
        self.alert_policy_client.delete_alert_policy(self.alert_policy.name)


@pytest.fixture()
def pochan():
    with PochanFixture() as pochan:
        yield pochan


def test_list_alert_policies(capsys, pochan: PochanFixture):
    snippets.list_alert_policies(pochan.project_name)
    out, _ = capsys.readouterr()
    assert pochan.alert_policy.display_name in out
    