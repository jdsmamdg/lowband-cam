import requests
from pathlib import Path
import logging
import urllib3
logging.getLogger(__name__)


def download_image(filename, camera_url):

    try:

        resp = requests.get(camera_url)

        logging.info("Camera HTTP status: {}".format(
            resp.status_code))
        logging.info("Camera response: {0} bytes took {1}".format(
            len(resp.content), resp.elapsed))

        img_file = Path(filename)
        img_file.write_bytes(resp.content)

        logging.info("Camera image saved: {}".format(filename))

    except requests.exceptions.RequestException as e:
        logging.error("Error getting image from camera")
        logging.debug(str(e))

    except OSError as e:
        logging.error("OS error while writing image to disk")
        logging.debug(str(e))
