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

# Initiatialize with location
LOCATION_ID = "0123456789abcdef01234567"  # Replace with location ID hash
ripple = Rippler(location_id=LOCATION_ID)

# Test with image file
image_number = ripple.send_image_file(image_path="image.png")
print(f"{image_number=}")
