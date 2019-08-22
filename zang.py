import os
from keyword import kwlist
import requests

class Client():
    def __init__(self, account_sid=None, auth_token=None, ):
        if account_sid is None:
            account_sid = os.getenv('ZANG_ACCOUNT_SID')

        if auth_token is None:
            auth_token = os.getenv('ZANG_AUTH_TOKEN')

        self.account_sid = account_sid
        self.auth_token = auth_token
        self.url = 'https://api.zang.io/v2'

    def _get(self, url):
        return requests.get(url, auth=(self.account_sid, self.auth_token))


    def list_calls(self):
        url = os.path.join(self.url, 'Accounts', self.account_sid, 'Calls.json')
        response = self._get(url)

        if response.ok:
            calls = response.json().get('calls')
            calls = [self.Call(call) for call in calls]
            return calls


    def list_numbers(self):
        url = os.path.join(self.url, 'Accounts', self.account_sid, 'IncomingPhoneNumbers.json')
        response = self._get(url)
        
        if response.ok:
            numbers = response.json().get('incoming_phone_numbers')
            numbers = [self.Number(number) for number in numbers]
            return numbers


    class Object():
        def __init__(self, data):
            keys = set(data.keys())
            kwset = set(kwlist)
            intersection = keys.intersection(kwset)

            #append a '_' to any keys that are python keywords (from, True, None, etc) 
            if intersection:
                for key in intersection:
                    value = data.pop(key)
                    data['{}_'.format(key)] = value
            
            self.__dict__.update(data)
            

    class Call(Object):
        def __str__(self):
            return "{} --> {}".format(self.from_, self.to)


    class Number(Object):
        def __str__(self):
            return self.phone_number

    class NumberList():
        pass
