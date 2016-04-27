# Copyright 2016 Google Inc. All rights reserved.
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

"""
Sample application that demonstrates different ways of fetching
URLS on App Engine
"""

# [START inbound-message-handler]
import logging
import webapp2
from google.appengine.api import mail

class InboundEmailMessageHandler(webapp2.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        logging.info('Received message from %s', message.sender)
# [END inbound-message-handler]

app = webapp2.WSGIApplication([
    ('/_ah/mail/<recipient:.+>', InboundEmailMessageHandler),
], debug=True)
