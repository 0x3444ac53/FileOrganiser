# File Organiser

#### What it does

Given a set of rules, this program will organize a directory based on those rules. 

#### Installation

```
$ git clone https://github.com/Lifesgood123/FileOrganiser
$ cd FileOrganiser
$ python3 -m venv .
$ source bin/activate
$ pip install -r requirements.txt
```

#### Usage 

In the directory that you want organized create a `rule.toml` file. Here is an example file

```toml
mode = "Extensions"

Documents = [ ".pdf", ".doc", ".docx", ".html", ".epub", ".mobi",".rtf", ".txt", ".odt", ".md", ".tex", ".pptx", ".otf", ".odf"]
Pictures = [ ".jpeg", ".jpg", ".png", ".bmp", ".gif", ".svg"]
Archives = [ ".zip", ".7zip", ".tar", ".bz", ".gz", ".xz", ".bz2"]
Videos = ['.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.ogg', '.mp4']
ProgramFiles = [".py", ".jar", ".crx", ".cpp", ".run", ".so", ".deb"]
DiskImages = [".iso"]
```

The `mode` rule is mandatory (check the `modes` directory) and then the rules. Each rule is a Folder name and then a condition for any given file to be checked against. The Extension mode checks if a given file has an extension in the list. Currently the only other mode is for regex matching, and that config file looks like this

```toml
mode = "regex"

Phi310 = "^PHI[_ ]?310.*"
Scans = "^Scan.*"
"Case Study" = "^CS.*"
```

After you create a rule file, point the script at that directory, i.e. 

```
$ main.py path/to/folder
```

It'll do a first pass, and you're welcome to leave it running and it will automatically move other files

#### Creating your own modes

Each mode is a python file that contains at least one function called `make_mover` this function returns a function that will move a file if a condition is met. There is probably a better way to do this, but I'll figure that out late, for now feel free to template your files off of the regex and extension modes. 
Regex:

```python
import re
import os 

def make_mover(folder, pattern):
    pattern = re.compile(pattern)
    def tester(x):
        if pattern.search(os.path.basename(x)) and not os.path.isdir(x):
            os.rename(x, os.path.join(folder, os.path.basename(x)))
        else:
            return False
        return True
    return tester

```

Extension:

```python
import os

def make_mover(folder, rules):
    return lambda x: os.rename(x, os.path.join(folder, os.path.basename(x))
                               ) if os.path.splitext(x)[-1] in rules else False

```

### Todo
- [] Add proper command line options
- [] Add some more modes
- [] Fix sloppy coding
- [] General Housekeeping
- [] Notify programs such as google-chrome that a file is moved and provide the new address
