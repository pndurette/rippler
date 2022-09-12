import json
import logging

from rippler import Rippler

# Configure basic logger
logging.basicConfig(
    level=logging.DEBUG,
    format=
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

# Get loggers for rippler and urllib3 (via requests)
rippler_logger = logging.getLogger('rippler.main')
urllib3_logger = logging.getLogger('urllib3')

# Set to debug
rippler_logger.setLevel(logging.DEBUG)
urllib3_logger.setLevel(logging.DEBUG)

# Define latitude and longitude
LAT = 40.74880
LON = -73.98559

# Fetch locations and pretty print
locations = Rippler.locations(lat=LAT, lon=LON)
print(json.dumps(locations, indent=4))