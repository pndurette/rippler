import json
import logging

from rippler import Rippler

logging.basicConfig(
    level=logging.DEBUG,
    format=
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])

rippler_logger = logging.getLogger('rippler.main')
urllib3_logger = logging.getLogger('urllib3')

rippler_logger.setLevel(logging.DEBUG)
urllib3_logger.setLevel(logging.DEBUG)

LAT = 49.284477848441846
LON = -123.09544576137593

locations = Rippler.locations(lat=LAT, lon=LON)
print(json.dumps(locations, indent=4))