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

LOCATION_ID = "62bb58f0a30e8137e0f5eb4e"
ripple = Rippler(location_id=LOCATION_ID)

# Test w/ image file
img_file_response = ripple.send_image_file(image_path="file.png")
print(f"{img_file_response=}")

print("----")

# Test w/ image fp
with open("file.png", "rb") as f:
    img_fp_response = ripple.send_image(image_fp=f)
    print(f"{img_fp_response=}")

print("----")

# Test w/ image URL
img_url_response = ripple.send_image_url(
    "https://lthub.ubc.ca/files/2021/06/GitHub-Logo.png")
print(f"{img_url_response=}")
