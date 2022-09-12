import logging
from typing import BinaryIO

import requests

# Logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

RIPPLES_API_URL = "https://webapp.drinkripples.com/api/v1/"


def api_endpoint(*url_parts) -> str:
    """Build a Ripples API URL endpoint

    Args:
        *url_parts: parts of the URL,
            e.g. "pushUrl", "123"

    Returns:
        str: the Ripples API URL followed by url_parts joined by slashes
    """
    url_parts = (RIPPLES_API_URL, ) + url_parts

    # Strip the ending slash of each part before joining
    return '/'.join([x.rstrip('/') for x in url_parts])


def stringify(obj):
    """Recursively stringify the boolean values of a dict

    Args:
        obj: any type or complex type

    Returns:
        the same object but with booleans transformed to lowercase strings
    """
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, (list, tuple)):
        return [stringify(i) for i in obj]
    if isinstance(obj, dict):
        return {k: stringify(v) for k, v in obj.items()}
    return obj


class Rippler:

    def __init__(self, location_id: str):
        """Rippler: An interface to the Ripples drink printer platform

            Args:
                location_id: the location string of the Ripples machine location.
                    Use `Ripple.locations()` to find the `location_id` (as `id`)
        """
        self.location_id = location_id

    @staticmethod
    def locations(lat: int, lon: int) -> dict:
        """Fetches closest Ripples machine locations

        Args:
            lat (int): the latitude, in decimal degrees
            lon (int): the longitude, in decimal degrees

        Returns:
            list: A list of dicts of the type:

                {id: str, name: str, address: str,
                distance: int, variants: list[str],
                latitude: int, longtitude: int, shortId: str}

        """
        endpoint = api_endpoint("locations")
        data = {"latitude": lat, "longitude": lon}

        try:
            r = requests.post(endpoint, data=data)
            r.raise_for_status()
            return RipplesResponse(r.json()).data
        except requests.exceptions.RequestException as e:
            raise RipplesException(str(e))

    def send_image_file(self, image_path: str) -> dict:
        """Send an image file to the printer

        Args:
            image_path: the path of an image to send to the printer

        Returns:
            int: the number representing the image in the
                custom images print queue on the machine
        """
        with open(image_path, "rb") as img:
            return self.send_image(img)

    def send_image(self, image_fp: BinaryIO):
        """Send an image file-like object to the printer

        Args:
            image_fp: file-like object of an image to send to the printer

        Returns:
            int: the number representing the image in the
                custom images print queue on the machine
        """
        # Get image upload service URL and parameters
        upload_service_config = self._upload_service_config()
        url = upload_service_config['url']
        params = upload_service_config['params']

        # Call upload service
        uploaded_image_url = self._upload_image(image_fp=image_fp,
                                                upload_url=url,
                                                params=params)

        # Send uploaded image URL (aka 'Push URL) to printer
        return self.send_image_url(image_url=uploaded_image_url)

    def send_image_url(self, image_url: str):
        """Send a public image url to the printer (/pushUrl endpoint)

        Args:
            image_url: image url to send to the printer

        Returns:
            int: the number representing the image in the
                custom images print queue on the machine
        """
        endpoint = api_endpoint("pushUrl", self.location_id)
        data = {"rippleUri": image_url}

        try:
            r = requests.post(endpoint, data=data)
            r.raise_for_status()

            # 'ordinal' is the number on the Ripples' machine custom images queue
            rr = RipplesResponse(r.json()).data
            return rr['ordinal']
        except requests.exceptions.RequestException as e:
            raise RipplesException(str(e))

    def _upload_service_config(self):
        """Get URL and params to Ripples' image upload service (/getSignedUrl endpoint)
        
        Returns:
            dict: the image upload service url and params to use of the type::

                {url: str, downloadUrl: str, params: dict}

                'url' is the endpoint of the image upload service
                'params' is a dict that must be passed to the upload service
        """
        endpoint = api_endpoint("getSignedUrl", self.location_id)

        try:
            r = requests.get(endpoint)
            return RipplesResponse(r.json()).data
        except requests.exceptions.RequestException as e:
            raise RipplesException(str(e))

    def _upload_image(self, image_fp: str, upload_url: str, params: dict):
        """Upload an image (file-like object) to Ripple's image upload service
        
        Args:
            image_fp: file-like object of an image to upload

        Returns:
            str: the url of the uploaded image
        """

        files = {"file": image_fp}
        data = stringify(params)

        try:
            r = requests.post(upload_url, files=files, data=data)
            # Not a Ripples API endpoint, so no RipplesResponse
            log.debug(f"image service response: {r.json()}")

            # Uploaded image URL
            return r.json()['url']
        except requests.exceptions.RequestException as e:
            raise RipplesException(str(e))
        except KeyError as e:
            # The url field isn't in the response
            msg = f"Unexpected API response, got: {str(r.json())}"
            raise RipplesException(msg)


class RipplesResponse:

    def __init__(self, raw_response: dict):
        """Response of the Ripples API

        Response had 'data' and 'err' fields.
        When there's no error, 'err' is None.

        Args:
            raw_response (dict): the response from the http request
        """
        try:
            log.debug(f"{raw_response=}")
            self._data = raw_response['data']
            self._error = raw_response['err']
        except KeyError:
            msg = f"Unexpected API response, got: {str(raw_response)}"
            raise RipplesException(msg)

        if self._error != None:
            msg = f"Error in API response: {str(self._error)}"
            raise RipplesException(msg)
        else:
            log.debug(f"{self.data=}")

    @property
    def data(self):
        return self._data

    @property
    def error(self):
        return self._error


class RipplesException(Exception):
    pass
