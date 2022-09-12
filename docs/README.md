## [rippler.main.py](/rippler/main.py)
---
### rippler.main.`api_endpoint` [function]
```Python
Build a Ripples API URL endpoint

Args:
    *url_parts: parts of the URL,
        e.g. "pushUrl", "123"

Returns:
    str: the Ripples API URL followed by url_parts joined by slashes
```
### rippler.main.`Rippler` [class]
None
#### Rippler.`__init__`
```Python
Rippler: An interface to the Ripples drink printer platform

Args:
    location_id: the location string of the Ripples machine location.
        Use `Ripple.locations()` to find the `location_id` (as `id`)
```
#### Rippler.`locations`
```Python
Fetches closest Ripples machine locations

Args:
    lat (int): the latitude, in decimal degrees
    lon (int): the longitude, in decimal degrees

Returns:
    list: A list of dicts of the type:

        {id: str, name: str, address: str,
        distance: int, variants: list[str],
        latitude: int, longtitude: int, shortId: str}
```
#### Rippler.`send_image_file`
```Python
Send an image file to the printer

Args:
    image_path: the path of an image to send to the printer

Returns:
    int: the number representing the image in the
        custom images print queue on the machine
```
#### Rippler.`send_image`
```Python
Send an image file-like object to the printer

Args:
    image_fp: file-like object of an image to send to the printer

Returns:
    int: the number representing the image in the
        custom images print queue on the machine
```
#### Rippler.`send_image_url`
```Python
Send a public image url to the printer (/pushUrl endpoint)

Args:
    image_url: image url to send to the printer

Returns:
    int: the number representing the image in the
        custom images print queue on the machine
```
#### Rippler.`_upload_service_config`
```Python
Get URL and params to Ripples' image upload service (/getSignedUrl endpoint)

Returns:
    dict: the image upload service url and params to use of the type::

        {url: str, downloadUrl: str, params: dict}

        'url' is the endpoint of the image upload service
        'params' is a dict that must be passed to the upload service
```
#### Rippler.`_upload_image`
```Python
Upload an image (file-like object) to Ripple's image upload service

Args:
    image_fp: file-like object of an image to upload

Returns:
    dict: the response from the upload service, with many fields.
        'url' is the URL of the uploaded image
```
#### Rippler.`_stringify`
```Python
Recursively stringify the values of a dict
```
### rippler.main.`RipplesResponse` [class]
None
#### RipplesResponse.`__init__`
```Python
Response of the Ripples API

Response had 'data' and 'err' fields.
When there's no error, 'err' is None.

Args:
    raw_response (dict): the response from the http request
```
#### RipplesResponse.`data`
None
#### RipplesResponse.`error`
None
### rippler.main.`RipplesException` [class] [inherits: `Exception`]
None
