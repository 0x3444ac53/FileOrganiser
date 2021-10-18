# File Organiser

#### What it does

Given a set of rules, this program will organize a directory based on those rules. 

#### Installation

```shell
$ pip3 install FileOrganiser
```

#### Usage 

##### Command Line Options

```shell
usage: main.py [-h] [-d] [-r] watchpath

positional arguments:
  watchpath        The Directory to watch

optional arguments:
  -h, --help       show this help message and exit
  -d, --daemon     run as daemon
  -r, --recursive  Crawl down directories
```

##### Rules and Modes

In the directory that you want organised, create a `rule.toml` file, with the first line defining the 'mode' of the rules. Individual modes have different criteria for valid rules, but follow the same pattern:

```toml
DirectoryToMoveFileTo = SomeRule
```
You can now have multiple rulefiles in a single directory, following the pattern `rules01.toml`, number them in order of importance

###### Extension Mode

The extension mode defines a list of file extensions. If newly created files have extensions that appear in that list, they are moved to the specified directory. Here is a standard example file:

```toml
mode = "Extensions"

Documents = [ ".pdf", ".doc", ".docx", ".html"]
Pictures = [ ".jpeg", ".jpg", ".png", ".bmp", ".gif", ".svg"]
Archives = [ ".zip", ".7zip", ".tar", ".bz", ".gz", ".xz", ".bz2"]
Videos = ['.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.mp4']
ProgramFiles = [".py", ".jar", ".crx", ".cpp", ".run", ".so", ".deb"]
DiskImages = [".iso"]
```

###### Regex

Self-explanatory. File gets moved to specified directory if it matches a pattern.

```toml
mode = "regex"

Phi310 = "^PHI[_ ]?310.*"
Scans = "^Scan.*"
"Case Study" = "^CS.*"
```

###### Script

Script mode is complicated and should be used with caution. It's good for hacks and esoteric operations. First, create a `rule.toml` that looks like this:

```toml
mode = "script"
aScript = '/absolute/path/to/script.py'
```

Then your script just needs to have a function called `main` that takes in a filename as an argument. In this example, if a file has a `.zip` extension, we extract it and then delete the zip file.

```python
import zipfile
import os
def main(file):
    if not os.path.isdir(file) and file.split('.')[-1] == 'zip':
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall('/path/to/folder')
        os.remove(file)
        return True
    return False
```

#### Creating your own modes

Each mode is a python file that contains at least one function called `make_mover`. This function returns a function that will move a file if a condition is met. [Take a look through the modes directory for inspiration](https://github.com/Lifesgood123/FileOrganiser/tree/master/modes) 

There is probably a better way to do this, but I'm stubborn.



#### Todo

- [ ] Add directory for custom modes in ~/.config
