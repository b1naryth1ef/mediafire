import requests, os, hashlib

DEBUG = os.getenv("MEDIAFIRE_DEBUG", False)

class MediaFireAPI(object):
    """
    An object representing a Python implementation of the mediafire API.
    """
    BASE_URL = "https://www.mediafire.com/api/%s"

    def __init__(self):
        self.session_token = None

    @staticmethod
    def get_signature(email, password, appid, appsecret):
        """
        Returns a signature from email, password, appid and appsecret.
        """
        return hashlib.sha1(email + password + appid + appsecret).hexdigest()

    def request(self, fmt, url, data={}, **kwargs):
        data['response_format'] = "json"
        if self.session_token:
            data['session_token'] = self.session_token

        r = getattr(requests, fmt.lower())(self.BASE_URL % url, params=data, **kwargs)
        r.raise_for_status()
        data = r.json()['response']
        if DEBUG: print data

        if 'result' not in data:
            raise Exception("Invalid API Response: `%s`" % data)

        if data['result'] == "Error":
            raise Exception("API Error: `%s`" % data)

        return data

    def authenticate(self, email, password, appid, appsecret):
        """
        Authenticates this instance with the backend, creating a valid session
        ID.
        """
        self.session_token = self.get_session_token(email, password, appid, appsecret)

    def get_session_token(self, email, password, appid, appsecret):

        signature = self.get_signature(email, password, appid, appsecret)
        r = self.request("GET", "user/get_session_token.php", {
            "email": email,
            "password": password,
            "application_id": appid,
            "signature": signature
        })

        return r['session_token']

    def get_new_session_token(self, old_token):
        r = self.request("GET", "user/renew_session_token.php", {
            "session_token": old_token
        })

        return r['session_token']

    def get_user_info(self):
        r = self.request("GET", "user/get_info.php")
        return r['user_info']

    def upload_file(self, fobj, data={}):
        r = self.request("POST", "upload/upload.php", data, files={
            "file": fobj
        })
        return r['doupload']['key']

    def create_folder(self, name):
        r = self.request("POST", "folder/create.php", {
            "foldername": name
        })
        return r['folder_key']
