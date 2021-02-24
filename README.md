# Filename Renamer
Rename file names

## Usage
```
usage: rename.py [-h] [-t] [-c] [-C] [-F] [-rt <Directory>] [-R] [-d] [-f] [-m <Regex pattern>] [-s <Search string>][-e <Regex pattern>] [-r <Replace string>] [-ex] [-fn] [-l] [-u][oldstr] [newstr] [<File path>...]
```

### Command Line Arguments
```
positional arguments:
  oldstr                Old string; This value override from -c or -e
  newstr                New String; This value override from -r
  <File path> ...       File list

optional arguments:
  -h, --help            show this help message and exit

global arguments:
  -t, --tree            Show target directory tree

confirm arguments:
  -c, --confirm         Confirm every time before rename. Enter y or n
  -C, --confirm-all     Confirm before rename. Enter y or n
  -F, --force           Force to rename

directory arguments:
  -rt <Directory>, --root <Directory>
                        Target directory of files to rename
  -R, --recursive       Recursive into sub directories

replace arguments:
  -d, --directory       Apply only to directory
  -f, --file            Apply only to files
  -m <Regex pattern>, --match <Regex pattern>
                        Apply only to file that match pattern. Must be enclosed in double quotation when using symbols
  -s <Search string>, --search <Search string>
                        This string will be replace with Replace string.
  -e <Regex pattern>, --expression <Regex pattern>
                        Regular expression pattern; Must be enclosed in double quotation when using symbols
  -r <Replace string>, --replace <Replace string>
                        Search string replace to this string
  -ex, --extension      Apply only to file extensions
  -fn, --filename       Apply only to file name

text-style arguments:
  -l, --lower           Transform path string to lower case
  -u, --upper           Transform path string to upper case
```

## License
MIT License Copyright (c) 2021 Y-Ysss