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

class PochanFixture:
    def __init__(self):
        self.project = snippets.project()
        self.alert_policy_client = monitoring_v3.AlertPolicyServiceClient()
        self.notification_channel_client = monitoring_v3.NotificationChannelServiceClient()
        self.policy = monitoring_v3.types.alert_pb2.AlertPolicy()
        self.policy.display_name = "snippets_test.py"
        self.policy.enabled.value = False
        self.policy.combiner = monitoring_v3.enums.AlertPolicy.ConditionCombinerType.OR        
        condition = self.policy.conditions.add()
        condition.condition_threshold.filter = "metric.label.state=\"blocked\" AND metric.type=\"agent.googleapis.com/processes/count_by_state\"  AND resource.type=\"gce_instance\""
        aggregation = condition.threshold.aggregations.add()
        

@pytest.fixture()
def pochan():
    yield PochanFixture()

def test_create_get_delete_metric_descriptor(capsys, pochan):
    snippets.list_alert_policies(snippets.project())