# deluge_rss_client
 External RSS Client for Deluge, either using subprocess or netmiko to run the deluge CLI commands to add Torrents from an RSS feed.
 This is a simple module without any error checking or reporting that I threw together.
## Requirements
This script requires Python3 (tested with python 3.8) as well as the following modules to be installed:

### Built-in Modules
 - sys
 - re
 - argparse
 - xml
 - yaml
 - datetime
 - pydoc
 - subprocess (if a local connection is used)
 - time

### 3rd party modules
 - requests
 - netmiko (if a remote connection is used)
 

## Usage

```bash
python3 rss_client.py --url "https://distrowatch.com/news/torrents.xml" \
--remote remote.hostname.com \
--username user \
--password password \
--download_dir /media/folder/to/download/to/ \
--deluge-console 127.0.0.1:52835
```