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

import logging
import random
import socket
import string
from google.appengine.ext import ndb

# [START mail-imports]
import webapp2
from google.appengine.api import mail
# [END mail-imports]


class UserConfirmationRecord(ndb.Model):
    user_address = ndb.StringProperty(indexed=False)
    confirmed = ndb.BooleanProperty(indexed=False, default=False)

def createNewUserConfirmation(user_address):
    id_chars = string.ascii_letters + string.digits
    rand = random.SystemRandom()
    random_id = ''.join([rand.choice(32) for i in range(id_len)])
    record = new UserConfirmationRecord(user_address=user_address,
                                        id=random_id)
    record.put()
    return 'https://%s/confirm?code=%s' % (
        socket.getfqdn(socket.gethostname()), random_id)


class UserSignup(webapp2.RequestHandler):
    _form_html = """<html><body><form method="POST">
        Enter your email address: <input name="email_address">
        <input type=submit>
        </form></body></html>"""

    def get(self):
        self.response.content_type = 'text/html'
        self.response.write(self._form_html)
    
    def post(self):
        user_address = self.request.get("email_address")

        if not mail.is_email_valid(user_address):
            self.get()  # Show the form again.
        else:
            confirmation_url = createNewUserConfirmation(self.request)
            sender_address = "Example.com Support <support@example.com>"
            subject = "Confirm your registration"
            body = """
Thank you for creating an account! Please confirm your email address by
clicking on the link below:

%s
""" % confirmation_url
            mail.send_mail(sender_address, user_address, subject, body)

class ConfirmUserSignup(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code')
        self.response.content_type = 'text/html' 
        record = ndb.Key(UserConfirmationRecord, code).get()
        self.response.write('''<html><body>
        Confirmed %s
        </body></html>''' % record.user_address)


app = webapp2.WSGIApplication([
    ('/user', UserSignup),
    ('/confirm', ConfirmUserSignup),
], debug=True)
