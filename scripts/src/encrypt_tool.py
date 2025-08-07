"""
To encrypt or decrypt some text
"""

__author__ = "Ryan Clark"

import sys

from lib import logging_utils, config_utils, encryption_utils

logger = logging_utils.get_logger(__name__)

def encrypt_tool(config: dict):
    text: str = config['args']['text']

    if config['args']['encrypt']:
        logger.info(f'Encrypting: "{text}"')
        logger.info(encryption_utils.encrypt(text))

    elif config['args']['decrypt']:
        logger.info(f'Decrypting: "{text}"')
        logger.info(encryption_utils.decrypt(text))
    
    else:
        raise RuntimeError("How did you get here")
    

def main():
    parser = config_utils.create_parser()

    parser.add_argument('--text', type=str, required=True, help='The text to encrypt or decrypt')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', action='store_true', help='Encrypt the input')
    group.add_argument('--decrypt', action='store_true', help='Decrypt the input')

    args = parser.parse_args()

    config = config_utils.load_config(args)
    logger.initialize_from_config(config)

    encrypt_tool(config)


if __name__ == '__main__':
    main()