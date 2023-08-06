# getfoldersize
*Python3 module to easily get a folder size.*

## Installation
### Install with pip
```
pip3 install -U getfoldersize
```

## Usage
```
In [1]: import getfoldersize

In [2]: from pathlib import Path

In [3]: getfoldersize.get_folder_size(
    Path("/home/user/Documents")
    )
Out[3]: 954460474

In [4]: getfoldersize.get_folders_size(
    Path("/home/user/Documents")
    )
Out[4]: 466944

In [5]: getfoldersize.get_files_size(
    Path("/home/user/Documents")
    )
Out[5]: 953993530
```
