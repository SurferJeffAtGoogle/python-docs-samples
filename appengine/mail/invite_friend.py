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

import random
import socket
import string
from google.appengine.ext import ndb
# [START invite_friend]
import webapp2
from google.appengine.api import mail
from google.appengine.api import users

class InviteFriendHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        to_addr = self.request.get("friend_email")
        if not mail.is_email_valid(to_addr):
            # Return an error message...
            pass

        message = mail.EmailMessage()
        message.sender = user.email()
        message.subject = "Invitation to Example.com"
        message.to = to_addr
        message.body = """
I've invited you to Example.com!

To accept this invitation, click the following link,
or copy and paste the URL into your browser's address
bar:

%s
        """ % generate_invite_link(to_addr)

        message.send()
# [END invite_friend]

    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""<html><body><form method="POST">
        Enter your friend's email address: <input name="friend_email">
        <input type=submit>
        </form></body></html>""")


class InvitationRecord(ndb.Model):
    """Datastore record with email address and confirmation code."""
    user_address = ndb.StringProperty(indexed=False)
    confirmed = ndb.BooleanProperty(indexed=False, default=False)
    timestamp = ndb.DateTimeProperty(indexed=False, auto_now_add=True)


class ConfirmInvitationHandler(webapp2.RequestHandler):
    """Invoked when the user clicks on the confirmation link in the email."""

    def get(self):
        code = self.request.get('code')
        if code:
            record = ndb.Key(InvitationRecord, code).get()
            # 2-hour time limit on confirming.
            if record:
                record.confirmed = True
                record.put()
                self.response.content_type = 'text/plain'
                self.response.write('Welcome %s' % record.user_address)
                return
        self.response.status_int = 404


def generate_invite_link(user_address):
    """Create a new user confirmation.

    Args:
        user_address: string, an email addres

    Returns: The url to click to confirm the email address."""
    id_chars = string.ascii_letters + string.digits
    rand = random.SystemRandom()
    random_id = ''.join([rand.choice(id_chars) for i in range(42)])
    record = InvitationRecord(user_address=user_address,
                                    id=random_id)
    record.put()
    return 'https://%s/confirm_friend?code=%s' % (
        socket.getfqdn(socket.gethostname()), random_id)

app = webapp2.WSGIApplication([
    ('/invite_friend', InviteFriendHandler),
    ('/confirm_friend', ConfirmInvitationHandler),
], debug=True)
