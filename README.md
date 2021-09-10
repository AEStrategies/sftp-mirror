# SFTP Mirror

Mirrors a remote SFTP site to a local directory.

## Setup

1. Create a python virtual environment:
```shell
python3 -m venv venv
```
2. Activate the virtual environment:
```shell
source ./venv/bin/activate
```
3. Install package requirements:
```shell
pip install -r requirements.txt
```

## Configure the mirror

Create an ini configuration file (e.g., `mirror.ini`) with settings similar to the following:

```ini
[mirror]
host = bgcloudfeed.burning-glass.com
username = tiffany.seward.ctr@govini.com
password = [PASSWORD_HERE]
local_base = /data/mirror/burning-glass
verbosity = info
dry_run = False
```

## Create the local mirror of the remote SFTP site:

```shell
python ./mirror.py --config ./mirror.ini
```

Directories and files from the remote site will be mirrored into the `local_base` directory.  It will ignore files that
already exist on the destination, if the file size and modification time are identical.
