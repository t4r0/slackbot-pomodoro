import os
import requests
import json
import datetime

USER_TOKEN_STRING = os.environ['SLACK_USER_TOKEN_STRING']

class User:
    """docstring for User"""
    def __init__(self, user_id):
        self.id = user_id

        self.username, self.real_name = self.fetch_names()

        self.tasks_history = []

        self.tasks = {}

        self.past_tasks = {}

        self.tasks_counts = {}

        print "New user: " + self.real_name + "(" + self.usenanme + ")"

    def store_session(self, run_name):
        try:
            self.past_tasks[run_name] = self.tasks
        except:
            self.past_tasks = {}

        self.past_tasks[run_name] = self.tasks
        self.tasks = {}
        self.tasks_counts = {}

    def fetch_names(self):
        params = {'token':USER_TOKEN_STRING, 'user': self.id}
        response = requests.get('http://slack.com/api/users.info', params=params)

        user_obj = json.loads(response.text, encoding='utf-8')['user']

        username = user_obj['name']
        real_name = user_obj['profile']['real_name']

        return username, real_name

    def get_user_handle(self):
        return ("@" + self.username).encode('utf-8')

    def is_active(self):
        try:
            params = {'token': USER_TOKEN_STRING, 'user':self.id}
            response = requests.get('http://slack.com/api/users.getPresence', params=params)
            status = json.loads(response.text, encoding='utf-8')['presence']

            return status == 'active'
        except:
            print 'Error fetching online status for' + self.get_user_handle()
            return False

    def add_task(self, task, hour):
        self.tasks[task['name']] = self.tasks.get(task['name'],0) + hour

        self.tasks_history.append([datetime.datetime.now().isoformat(), task['name'], hour])
