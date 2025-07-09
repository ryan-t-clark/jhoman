"""
Script to merge csv's
"""

__author__ = "Ryan Clark"

import sys
import pandas as pd
from pathlib import Path

from lib import logging_utils, config_utils

logger = logging_utils.get_logger(__name__)


def merge_new_orders(config: dict):
    input_dir: Path = Path(config['paths']['input_dir'])
    
    if not input_dir.exists():
        logger.error(f"Provided input path does not exist: {input_dir}")
        sys.exit(1)

    output_path: Path = Path(config['paths']['output_path'])

    merged_df: pd.DataFrame = pd.DataFrame()
    for path in input_dir.iterdir():
        if path.is_file() and path.suffix == '.csv' and path != output_path:
            data = pd.read_csv(path)
            logger.info(f"Found {len(data)} rows in {path}")
            merged_df = pd.concat([merged_df, data], ignore_index=True)

    if merged_df.empty:
        logger.warning(f"No rows merged.")
        return 0

    logger.info(f"Merged {len(merged_df)} rows")

    

    logger.info(f"Writing output to: {output_path}")
    merged_df.to_csv(output_path)
    

def main():
    parser = config_utils.create_parser()

    args = parser.parse_args()

    config = config_utils.load_config(args)
    logger.initialize_from_config(config)

    merge_new_orders(config)


if __name__ == '__main__':
    main()