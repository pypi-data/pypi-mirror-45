# pydownloadfile
*Python3 module to download files using requests.*

## Installation
### Install with pip
```
pip3 install -U pydownloadfile
```

## Usage
```
In [1]: from pathlib import Path

In [2]: import pydownloadfile

In [3]: pydownloadfile.download_file(
    url="https://...",
    filename=Path("foobar...")
    headers=None
    proxies=None
    )
```
