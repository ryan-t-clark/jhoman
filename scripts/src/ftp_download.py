"""
To encrypt or decrypt some text
"""

__author__ = "Ryan Clark"

import sys

from lib import logging_utils, config_utils

logger = logging_utils.get_logger(__name__)

def ftp_download(config: dict):
    logger.info(f"Hello world")
    logger.info(config['ftp_connection']['password'])
    

def main():
    parser = config_utils.create_parser()

    args = parser.parse_args()

    config = config_utils.load_config(args)
    logger.initialize_from_config(config)

    ftp_download(config)


if __name__ == '__main__':
    main()