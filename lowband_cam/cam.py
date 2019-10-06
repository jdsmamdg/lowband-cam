from lowband_cam.scripts import cam_util
from lowband_cam.scripts import aws_util
from lowband_cam.scripts import util
import boto3
import logging
import os

logging.getLogger(__name__)


def main():

    try:

        args = util.parse_args()

        util.setup_logging(args.log_level)

        cfg = util.get_config_dict_from_file(args.config_file)

        filename = util.get_filename()

        cam_util.download_image(filename, cfg['camera']['url'])
        transformed_image_filename = util.transform_save_image(filename, cfg['image']['height'], cfg['image']
                                                            ['width'], cfg['image']['optimize'], cfg['image']['quality'])

        s3 = aws_util.S3Client()
        s3.client.upload_file(transformed_image_filename,
                                            cfg['s3']['bucket_name'], transformed_image_filename)

    except KeyError as e:
        logging.error("Key error: Item not found in config")
        logging.debug(str(e))


if __name__ == "__main__":
    main()
