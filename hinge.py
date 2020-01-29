import requests
import json
import config
from auth import get_access_token


class Hinge(object):

    def __init__(self, headers=None):

        self.headers = {
            'content-type': 'application/json',
            'x-device-platform': 'iOS',
            'x-session-id': '3E3CCF47-BF71-4F2C-A1D4-D99C9C980F95',
            'x-install-id': 'FC9E889B-9DF2-4AC1-B716-64CAC5A8EAEA',
            'accept-language': 'en-us',
            'accept-encoding': 'gzip, deflate, br',
            'x-build-number': '11098',
            'user-agent': 'Hinge/11098 CFNetwork/1121.2.2 Darwin/19.2.0',
            'x-app-version': '7.12.2',
            'x-os-version': '13.3',
            'x-device-model': 'iPhone 7 Plus',
            'Authorization': None
        }

        self.generate_token()

    def generate_token(self):

        request_body = {
            "facebookId": "10152933244684657",
            "facebookToken": None,
            "installId": "FC9E889B-9DF2-4AC1-B716-64CAC5A8EAEA"
        }

        request_body['facebookToken'] = str(get_access_token())

        url = "https://prod-api.hingeaws.net/identity"
        identity_response = requests.post(
            url,
            data=json.dumps(request_body),
            headers=self.headers
        )

        identity_json = identity_response.json()
        auth_token = identity_json['token']

        self.headers['Authorization'] = f'Bearer {auth_token}'
        return auth_token

    def get_feed(self):

        url = 'https://prod-api.hingeaws.net/potential'
        feed = requests.get(url, headers=self.headers)
        return feed.json()

    def get_profile(self, subjects):

        url = f"https://prod-api.hingeaws.net/user/public?ids={subjects}"
        profiles = requests.get(url, headers=self.headers)
        return profiles.json()

    def swipe(self, subject):

        request_body = [
            {
                "content": [
                    {
                        "photo": {
                            "boundingBox": subject['box'],
                            "url": subject['url']
                        }
                    }
                ],
                "origin": "potential",
                "rating": "like",
                "subjectId": subject['id']
            }
        ]

        url = "https://prod-api.hingeaws.net/rate"
        res = requests.post(
            url,
            data=json.dumps(request_body),
            headers=self.headers
        )

        return res.json()


if __name__ == '__main__':
    hinge = Hinge()
    hinge.get_feed()
