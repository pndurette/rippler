import json
from urllib import response

from rippler.main import Ripple

LAT = 49.284477848441846
LON = -123.09544576137593
LOCATION_ID = "62bb58f0a30e8137e0f5eb4e"

# locations = Ripple.locations(lat=LAT, lon=LON)
# print(json.dumps(locations, indent=4))

ripple = Ripple(location_id=LOCATION_ID)
# response = ripple.send_image_url(
#     # image_url="https://logos-world.net/wp-content/uploads/2020/04/Nike-Logo.png"
#     image_url=
#     "https://cdn.freebiesupply.com/logos/large/2x/a-w-1-logo-png-transparent.png"
# )

# print(response)

response = ripple.send_image_file(image_path="file.png")

print(response)