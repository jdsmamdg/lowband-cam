import argparse
import configparser
import datetime
from PIL import Image
import logging
logging.getLogger(__name__)


def setup_logging(log_level):
    logging.basicConfig(level=log_level,
                        format="%(asctime)s [%(module)-14.14s] [%(levelname)-8.8s]  %(message)s",
                        handlers=[
                            logging.FileHandler(
                                "{0}/{1}.log".format('./log', 'lowband-cam')),
                            logging.StreamHandler()
                        ]
                        )


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run the lowband-cam application to get the camera image, process the image, and upload to S3.')
    parser.add_argument('--log_level', type=str, default='INFO', choices=[
                        'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='Desired log level')
    parser.add_argument('--config_file', type=str, default='./config/config.ini',
                        help="Complete path and filename for configuration INI file.")
    return parser.parse_args()


def get_config_dict_from_file(filename='./config/config.ini'):
    try:
        config = configparser.ConfigParser()
        config.read(filename)

        return {s: dict(config.items(s)) for s in config.sections()}

    except OSError as e:
        logging.error("Error reading config file")
        logging.debug(str(e))


def get_filename():
    path = "images/"
    filename = f"_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}"
    extension = ".jpg"

    return path + filename + extension


def transform_save_image(filename, img_height, img_width, img_optimize, img_quality):
    try:
        transformed_image_filename = filename + '_sm.jpg'
        im = Image.open(filename)
        im = im.resize((int(img_height), int(img_width)), Image.ANTIALIAS)
        im.save(transformed_image_filename, format='JPEG',
                optimize=bool(img_optimize), quality=int(img_quality))
        return transformed_image_filename
    except TypeError:
        logging.error(
            "Type error: confirm image height, width, quality are integers, and image optimize is a boolean.")
