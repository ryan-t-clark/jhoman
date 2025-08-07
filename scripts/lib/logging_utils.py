"""
Wrapper around Python's built in logging functionality to simplify configuration
"""

__author__ = "Ryan Clark"

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

from .encryption_utils import DecryptedValue

STACK_LEVEL = 2
_LINE_LEN = 30

def hide_decrypted_val(value) -> str:
    if isinstance(value, DecryptedValue):
        return "*" * 10
    return str(value)

class ScriptLogger:
    def __init__(self, name: str, log_level=logging.INFO):
        self.name = name
        self.log_level = log_level
        self._logger = None
        self._initialized = False

    def _init_logging(self, log_dir):
        log_dir.mkdir(exist_ok=True, parents=True)

        current_datetime: str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        log_filename: str = f"{current_datetime}-{self.name}.log"
        log_file: Path = log_dir / log_filename

        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(self.log_level)

        self._logger.handlers.clear()

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(self.log_level)

        formatter: logging.Formatter = logging.Formatter(
            '[%(asctime)s] (%(funcName)-12.12s:%(lineno)3d) [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        self._initialized = True
        self.log_filepath = log_file

    def _display_config(self):
        self.info(f"Running {self.config['context']['script_name']}")
        self.info(f"Command line: {''.join(sys.argv)}")
        self.info("=" * _LINE_LEN)
        formatted_lines = format_dict(self.config)
        for line in formatted_lines:
            self.info(line)
        self.info("=" * _LINE_LEN)

    def initialize_from_config(self, config: dict):
        self.config = config

        if 'logging' not in config.keys():
            raise RuntimeError(f"CONFIG ERROR: Invalid configuration provided. No 'logging' section provided")

        REQUIRED_FIELDS = ['log_dir', 'log_level']

        logging_config: dict = config['logging']
        for field in REQUIRED_FIELDS:
            if field not in logging_config:
                raise RuntimeError(f"CONFIG ERROR: Invalid configuration provided. No 'logging.{field}' section provided.")

        log_level_mapping = logging.getLevelNamesMapping()
        config_log_level: str = logging_config['log_level']
        if config_log_level not in log_level_mapping.keys():
            raise RuntimeError(f"CONFIG ERROR: Invalid configuration provided. {config_log_level} is not a valid logging level. "
                               f"Available options: {list(log_level_mapping.keys())}")
        self.log_level = log_level_mapping[config_log_level]

        log_dir = Path(config['logging']['log_dir'])

        self._init_logging(log_dir)
        self._display_config()

    def initialize(self, log_dir: str):
        # For use when you don't have a config setup, quick way to get a logger that writes to a file
        self._init_logging(Path(log_dir))
        self.info(f"Executing script '{self.name}.py' without loading a configuration")
        self.info(f"Current time: {datetime.now()}")
    
    def _ensure_initialized(self):
        if not self._initialized:
            raise RuntimeError("Logger not initialized. Call the initialize function to complete setup.")
        
    def debug(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.debug(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def info(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.info(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def warning(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.warning(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def warn(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.warning(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def error(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.error(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def critical(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.critical(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def exception(self, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.exception(message, *args, **kwargs, stacklevel=STACK_LEVEL)
    
    def log(self, level, message, *args, **kwargs):
        self._ensure_initialized()
        self._logger.log(level, message, *args, **kwargs, stacklevel=STACK_LEVEL)


def get_logger(name: str, log_level=logging.INFO):
    if name is None or name == "__main__":
        script_name = os.path.basename(sys.argv[0])
        if script_name.endswith('.py'):
            script_name = script_name[:-3]
        name = script_name
    return ScriptLogger(name, log_level)


def format_dict(d, indent=0):
    lines = []
    spacing = "  " * indent
    
    for key, value in d.items():
        if isinstance(value, dict) and value:
            lines.append(f"{spacing}[{key}]")
            lines.extend(format_dict(value, indent + 1))
        else:
            if isinstance(value, dict):
                lines.append(f"{spacing}{key} -> {{}}")
            else:
                if isinstance(value, DecryptedValue):
                    lines.append(f"{spacing}{key} -> {hide_decrypted_val(value)}")
                else:
                    lines.append(f"{spacing}{key} -> {value}")
    
    return lines
