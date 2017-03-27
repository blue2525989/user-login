#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import re


# top of html page
def buildTop():
    html = '''<html>
                <head>
                <title>User Login</title>
                </head>
                <body bgcolor="lightblue">
                <div align="center">'''

    return html


# bottom of html page
def buildBottom():
    image = '''<img src="https://media3.giphy.com/media/rDIbIO2O7UStO/200_s.gif">'''
    html_end = '''
                <br/><br/>''' + image + '''
                </div>
                </body>
                </html>'''
    return html_end


# starter form
def form():
    form = '''

                <h1>  User Login </h1>
                    <form method="POST">
                    <label>Enter Login Info Below:
                    <br>
                    <label>Username:</label>
                    <input type="text" name="username">
                    <br>
                    <label>Password:</label>
                    <input type="password" name="password">
                    <br>
                    <label>Verify Password:</label>
                    <input type="password" name="verify">
                    <br>
                    <label>Email:</label>
                    <input type="text" name="email">
                    <br>
                    <input type="submit">
                    </form>
                '''
    return form


# invalid username form
def formUser(email):
    form = '''

                <h1>  User Login </h1>
                    <form method="POST">
                    <label>Enter Login Info Below:
                    <br>
                    <label>Username:</label>
                    <input type="text" name="username">That's not a valid username.
                    <br>
                    <label>Password:</label>
                    <input type="password" name="password">
                    <br>
                    <label>Verify Password:</label>
                    <input type="password" name="verify">
                    <br>
                    <label>Email:</label>
                    <input type="text" name="email"  value="'''+email+'''">
                    <br>
                    <input type="submit">
                    </form>
                '''
    return form


# invalid password form
def formPass(username, email):
    form = '''

                <h1>  User Login </h1>
                    <form method="POST">
                    <label>Enter Login Info Below:
                    <br>
                    <label>Username:</label>
                    <input type="text" name="username"  value="'''+username+'''">
                    <br>
                    <label>Password:</label>
                    <input type="password" name="password">That wasn't a valid password.
                    <br>
                    <label>Verify Password:</label>
                    <input type="password" name="verify">
                    <br>
                    <label>Email:</label>
                    <input type="text" name="email"  value="'''+email+'''">
                    <br>
                    <input type="submit">
                    </form>
                '''
    return form


# invalid verify form
def formVerify(username, email):
    form = '''

                <h1>  User Login </h1>
                    <form method="POST">
                    <label>Enter Login Info Below:
                    <br>
                    <label>Username:</label>
                    <input type="text" name="username"  value="'''+username+'''">
                    <br>
                    <label>Password:</label>
                    <input type="password" name="password">That wasn't a valid password.
                    <br>
                    <label>Verify Password:</label>
                    <input type="password" name="verify">Your passwords didn't match.
                    <br>
                    <label>Email:</label>
                    <input type="text" name="email"  value="'''+email+'''">
                    <br>
                    <input type="submit">
                    </form>
                '''
    return form


# invalid email form
def formEmail(username):
    form = '''

                <h1>  User Login </h1>
                    <form method="POST">
                    <label>Enter Login Info Below:
                    <br>
                    <label>Username:</label>
                    <input type="text" name="username"  value="'''+username+'''">
                    <br>
                    <label>Password:</label>
                    <input type="password" name="password">
                    <br>
                    <label>Verify Password:</label>
                    <input type="password" name="verify">
                    <br>
                    <label>Email:</label>
                    <input type="text" name="email">That's not a valid email.
                    <br>
                    <input type="submit">
                    </form>
                '''
    return form

# to check username against
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{5,20}$")


# checks for valid username
def valid_username(username):
    return username and USER_RE.match(username)

# to test password against
PASS_RE = re.compile(r"^.{5,10}$")


# check to make sure password is of length and no crazy chars
def valid_password(password):
    return password and PASS_RE.match(password)

# to test email against
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


# check to make sure it is valid email
def valid_email(email):
    return not email or EMAIL_RE.match(email)


# main handler for /
class MainHandler(webapp2.RequestHandler):

    # loads the page
    def get(self):
        # builds the page
        top = buildTop()
        username = form()
        bottom = buildBottom()
        main_page = top + username + bottom
        self.response.write(main_page)

    # when you click submit
    def post(self):
        # boolean flag in-case entry is invalid
        invalid = False
        # create variables for checking error conditions
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        # empty dictionary to store types of error and messages
        error = {}
        # check for each error
        if not valid_username(username):
            error['error_username'] = "That's not a valid username."
            invalid = True

        if not valid_password(password):
            error['error_password'] = "That wasn't a valid password."
            invalid = True
        elif password != verify:
            error['error_verify'] = "Your passwords didn't match."
            invalid = True

        if not valid_email(email):
            error['error_email'] = "That's not a valid email."
            invalid = True

        # if an entry is invalid
        if invalid:
            for key in error:
                if key == 'error_username':
                    main_page = buildTop() + formUser(email) + buildBottom()
                elif key == 'error_password':
                    main_page = buildTop() + formPass(username, email) + buildBottom()
                elif key == 'error_verify':
                    main_page = buildTop() + formVerify(username, email) + buildBottom()
                elif key == 'error_email':
                    main_page = buildTop() + formEmail(username) + buildBottom()
            # writes invalid page
            self.response.write(main_page)
        # if page s valid
        else:
            # had to add the username like a get request to end of redirect for username to show up
            # on the next page.
            self.redirect('/welcome?username=' + username)


# handler for /welcome
class WelcomeHandler(webapp2.RequestHandler):

    # loads the page
    def get(self):
        image = '''<img src="http://www.i-love-cats.com/images/2015/04/12/cat-wallpaper-38.jpg"
        width="811" height="456">'''
        # gets the username variable
        username = self.request.get("username")
        # makes it look nice
        prompt = '<div align="center"><h2>Welcome <strong><marquee>' + username + '</marquee></strong></h2>' + \
                 image + '</div>'
        # builds page
        top = buildTop()
        bottom = buildBottom()
        main_page = top + prompt + bottom
        self.response.write(main_page)

# handlers
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
