## Python Environment and Setup

I'm currently looking into setting up an easy way to set up the python environment, but for now to run the code you will need

```
pip install pandas
```
```
pip install pyyaml
```
```
pip install cryptography
```

## Repository Structure

All Python code can be found in the `scripts` directory. Within the scripts directory there are three subdirectories

### src
`src` contains the scripts themselves. In general, we'll try to keep the layout of scripts consistent, such that they all use the framework setup through the `logging_utils` and `config_utils` modules. An example script of a basic script layout is below:
```python
"""
Description of the script
"""

__author__ = "Author"

import sys

from lib import logging_utils, config_utils

logger = logging_utils.get_logger(__name__)


def script_name(config: dict):
	# TODO
	sys.exit(0)
  
  
def main():
	parser = config_utils.create_parser()
	
	args = parser.parse_args()
	
	config = config_utils.load_config(args)
	logger.initialize_from_config(config)

	script_name(config)

if  __name__ == '__main__':
	main()
```
Using this framework, executing the script will require the use of the command line argument `-c` or `--config`, which will be a path to the corresponding config for the script. For example, calling this script could look like:
```
python script.py --config=/path/to/config/script.yaml
```
If you don't need a config file for a script, you can point to `common.yaml`

### config
This directory will contain all of the config files for the scripts.

Config files uses the standard **yaml** format, and I added support for including other config files so they can be shared between multiple scripts.

An example config file is below:
```yaml
includes:
- common.yaml

paths:
	input_dir: /Users/ryanclark/workspace/jhoman/testing
	output_path: /Users/ryanclark/workspace/jhoman/testing/output.csv
```
When the config is loaded, it will include all fields in `common.yaml` as well as whatever `common.yaml` includes. You can include as many other config files as you want by just adding another to that list.

Then in the script, you can get config fields like this:
```
input_dir: Path = config['paths']['input_dir']
```

### lib
`lib` contains utilities that are shared between scripts such as logging, config, and general helper functions that might be useful in many places.
