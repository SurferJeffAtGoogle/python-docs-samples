#!/usr/bin/env python

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

from google_auth_oauthlib import flow

# Authenticate to get user's credentials.
client_secrets_json = '/usr/local/google/home/rennie/Downloads/client_secret_356971158591-ioap1g4kkd0nki1vn045va49s3nstmvo.apps.googleusercontent.com.json'
# 'path/to/your/client_secrets.json'

appflow = flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_json,
    scopes=['https://www.googleapis.com/auth/bigquery'])

appflow.run_local_server()
# appflow.run_console()

# Call Bigquery with credentials.
from google.cloud import bigquery
import json

with open(client_secrets_json) as f:
    project = json.load(f)['installed']['project_id']

client = bigquery.Client(project=project, credentials=appflow.credentials)
query_job = client.query(
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
    'WHERE state = "TX" '
    'LIMIT 100')

# Print the results.
for row in query_job.result():  # Wait for the job to complete.
    print(row)
