# -*- coding: utf-8 -*-
import os
import logging
import base64
import requests
import requests_oauth2
from oauth2client import file, client
from google.oauth2 import service_account
from googleapiclient import discovery, _auth
from googleapiclient.discovery import build

from datetime import datetime, timedelta
from apiclient import errors
from requests_oauth2 import OAuth2BearerToken

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import re
import random
import string

logger = logging.getLogger(__name__)


class GoogleApi:
      
  __webdev_cred = ''
  __mentor_cred = ''

  def __init__(self):
    # see https://developers.google.com/identity/protocols/oauth2/scopes
    # Define the auth scopes to request.
    scopes = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group',
    ]
    SERVICE_ACCOUNT_FILE = os.path.join("vbb_backend", "service-account.json")

    # Use the credentials object to call Google APIs in the application.
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes)
    self.__webdev_cred = credentials.with_subject(
        'webdevelopment@villagebookbuilders.org')
    self.__mentor_cred = credentials.with_subject(
        'mentor@villagebookbuilders.org')

  def account_create(self, firstName, lastName, personalEmail):
        
        """ Creates the mentor's google account.

        Args:
          firstName: Mentor FirstName
          lastName:  Mentor Lastname
          personalEmail: Mentor Personal Email

        """
        http = _auth.authorized_http(self.__webdev_cred)
        self.__webdev_cred.refresh(http._request)
        url = "https://www.googleapis.com/admin/directory/v1/users"
        headers = {
            # 'Authorization': 'Bearer' delegated_credentials.token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        # checking if the email id already exists, adds an id to the end to differentiate
        addedID = 0  # on repeat, email will start from firstname.lastname1@villagementors.org

        def userExists(email):
              url = 'https://www.googleapis.com/admin/directory/v1/users/' + email
              with requests.Session() as s:
                s.auth = OAuth2BearerToken(self.__webdev_cred.token)
                r = s.get(url)
                if (r.status_code == 404):
                  return False
                return True

        primaryEmail = firstName + '.' + lastName + '@villagementors.org'

        while(userExists(primaryEmail)):
          addedID += 1
          primaryEmail = firstName + '.' + lastName + \
              str(addedID) + '@villagementors.org'
        pwd = 'VBB' + random.choice(['!', '@', '#', '$', '%', '&']) + \
                  str(random.randint(100000000, 1000000000))

        data = '''
        {
          "primaryEmail": "%s",
          "name": {
            "familyName": "%s",
            "givenName": "%s"
          },
          "password": "%s",
          "changePasswordAtNextLogin": "true",
          "recoveryEmail": "%s",
        }
        ''' % (primaryEmail, lastName, firstName, pwd, personalEmail)

        with requests.Session() as s:
          s.auth = OAuth2BearerToken(self.__webdev_cred.token)
          r = s.post(url, headers=headers, data=data)
        return (primaryEmail, pwd)

  def calendar_event(self, mentorFirstName, menteeEmail, mentorEmail, personalEmail, directorEmail, start_time, end_date, calendar_id, room, duration=1):
        
        """ Creates a new calendar event with the Google Hangout Link 

        https://developers.google.com/calendar/v3/reference/events/insert 
        The calendarId is the Calendar identifier. Value type string
        The request body suppy an event resource

        Args:
            mentorFirstName: Mentor's First Name
            menteeEmail: Email's Mentee
            mentorEmail: Mentor's Email @villagementors.org
            personalEmail: Mentor's personal email
            directorEmail: Director's Email
            start_time: Start time of the session (yyyy-mm-ddThh:mm:ss)
            end_date: End date of the session
            calendar_id: Calendar's identifier

        Returns:
            An object event containing all properties of the session
        """
        
        calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
        timezone = 'UTC'
        start_date_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end_time = start_date_time_obj + timedelta(hours=duration)
        end_date_formated = end_date.replace(':', '')
        end_date_formated = end_date_formated.replace('-', '')
        end_date_formated += 'Z'

        event = {
            'summary': mentorFirstName + ' - VBB Mentoring Session',
            'start': {
                'dateTime': start_date_time_obj.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=' + end_date_formated
            ],
            'attendees': [
                {'email': menteeEmail},
                {'email': mentorEmail},
                {'email': personalEmail},
                {'email': directorEmail},
                {'email': room, 'resource': "true"}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # reminder 24 hrs before event
                    # pop up reminder, 10 min before event
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                }
            },
        }
        event_obj = calendar_service.events().insert(calendarId=calendar_id, body=event,
                                                    sendUpdates="all", conferenceDataVersion=1).execute()
        print(event_obj['id'])

        return(event_obj['id'], event_obj['hangoutLink'])
        
  def email_send(self, to, subject, templatePath, extraData=None, cc=None):
        
      """ Sends an email message

      Args:
        to: Email address of the receiver.
        subject: The subject of the email message.
        templatePath: The path to reference a html template.

      """
      http = _auth.authorized_http(self.__mentor_cred)
      email_service = build('gmail', 'v1', http=http)
      personalizedPath = os.path.join(
          "api", "emails", "templates", "placeholder.html")
      if cc is not None:
        cc = ','.join(cc)

      def updatePersonalizedHTML(templatePath, personalizedPath, extraData):
        
        """ Get HTML with the extraData filled in where specified.
          - Use Beautiful soup to find and replace the placeholder values with the proper user
            specific info
          - Use 'with' to write the beautifulSoup string into a newFile - the personalized version of the
            original templatePath. This personalized version will be sent out in the email and will be
            rewritten everytime the function is called.
        """
        with open(templatePath, 'r', encoding="utf8") as f:
          template = f.read()
        soup = BeautifulSoup(template, features="html.parser")
        if extraData != None:
          for key in extraData:
            target = soup.find_all(text=re.compile(r'%s' % key))
            for v in target:
              v.replace_with(v.replace('%s' % key, extraData[key]))
          # now soup string has the proper values
        with open(personalizedPath, "w") as file:
          file.write(str(soup))

  def update_event(self, calendar_id, event_id, end_date=None, start_time=None, end_time=None):
      """ Updates an existing event
      
      https://developers.google.com/calendar/v3/reference/events/update

      Args:
        calendar_id: Calendar's identifier
        event_id: Event identifier
        end_date: New end date of the session after update

      """
      calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
      event = calendar_service.events().get(
          calendarId=calendar_id, eventId=event_id).execute()
      if (end_date != None):
        end_date_formated = end_date.replace(':', '')
        end_date_formated = end_date_formated.replace('-', '')
        end_date_formated += 'Z'
        event['recurrence'] = ['RRULE:FREQ=WEEKLY;UNTIL=' + end_date_formated]
        event['summary'] = 'update worked 2021!'
        updated_event = calendar_service.events().update(
        calendarId=calendar_id, eventId=event['id'], body=event).execute()





# # FOR TESTING PURPOSES -- REMOVE IN PROD
def testFunction():
    g = GoogleApi()

  # g.shift_event("c_oha2uv7abp2vs6jlrl96aeoje8@group.calendar.google.com","0vjr0aj0e3nv1tmc2ui2mtshbi")

    # g.account_create(
    #     "Testname",
    #     "TestLastname",
    #     "mentor@villagementors.org")

    # g.calendar_event(
    #     "TestNewCalendarEvent",
    #     "test@villagementors.org",
    #     "mentoremail@villagementors.org",
    #     "testmentee@gmail.com",
    #     "testdirector@gmail.com",
    #     "2021-04-24T23:30:00", "2021-10-30T22:00:00",
    #     "c_oha2uv7abp2vs6jlrl96aeoje8@group.calendar.google.com",
    #     "ximena.rodriguez1@villagementors.org")

    # g.update_event(
      # "c_oha2uv7abp2vs6jlrl96aeoje8@group.calendar.google.com",
      # "b9uhgcrdjt6gea7nlj82rubig8",
      # "2022-09-27T22:00:00")

#   print("updated")


# testFunction()
