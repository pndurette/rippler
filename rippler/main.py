import json

from email.mime import image
from urllib.parse import urljoin

import requests

RIPPLE_API_URL = "https://webapp.drinkripples.com/api/v1/"


def extract_data(response: dict):
    return response['data']


# https://stackoverflow.com/a/42658558
def convert(obj):
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, (list, tuple)):
        return [convert(item) for item in obj]
    if isinstance(obj, dict):
        return {convert(key):convert(value) for key, value in obj.items()}
    return obj

class Ripple:

    @staticmethod
    def locations(lat: int, lon: int):
        endpoint = urljoin(RIPPLE_API_URL, "locations")
        data = {"latitude": lat, "longitude": lon}
        r = requests.post(endpoint, data=data)
        return extract_data(r.json())

    def __init__(self, location_id: str):
        self.location_id = location_id

    def send_image_url(self, image_url: str):
        return self._push_url(image_url=image_url)

    def send_image_file(self, image_path: str):
        # Get signed upload URL
        upload_info = self._get_signed_url()
        print(f"{upload_info=}")

        # Upload
        upload_response = self._upload_image(image_path=image_path,
                                             upload_url=upload_info['url'],
                                             params=upload_info['params'])
        print(f"{upload_response=}")

        # Push URL of uploaded image
        return self._push_url(image_url=upload_response['url'])

    def _get_signed_url(self):
        endpoint = urljoin(RIPPLE_API_URL, f"getSignedUrl/{self.location_id}")
        r = requests.get(endpoint)
        return extract_data(r.json())

    def _upload_image(self, image_path: str, upload_url: str, params: dict):
        files = {"file": (image_path, open(image_path, 'rb'))}
        # JSON values (e.g. booleans) must be strings (e.g. 'true' instead of True)
        r = requests.post(upload_url, files=files, data=convert(params))
        # print(f"{r.request.body=}")
        return r.json()

    def _push_url(self, image_url: str):
        endpoint = urljoin(RIPPLE_API_URL, f"pushUrl/{self.location_id}")
        data = {"rippleUri": image_url}
        r = requests.post(endpoint, data=data)
        return extract_data(r.json())


# TODO: Error handling
# TODO: Better reusable "request crafter" method