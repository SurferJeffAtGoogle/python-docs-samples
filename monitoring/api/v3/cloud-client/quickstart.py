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

import os

def run_quickstart():
    # [START monitoring_quickstart]
    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.environ['GCLOUD_PROJECT'])

    series = monitoring_v3.types.TimeSeries()
    series.metric.type = 'custom.googleapis.com/my_metric'
    series.resource.type = 'gce_instance'
    series.resource.labels['instance_id'] = '1234567890123456789'
    series.resource.labels['zone'] = 'us-central1-f'
    series.points.add().value.double_value = 3.14
    print('Successfully wrote time series.')
    # [END monitoring_quickstart]


if __name__ == '__main__':
    run_quickstart()
