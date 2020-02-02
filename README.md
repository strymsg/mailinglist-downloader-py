# Mail listing downloader scripts

Collection of scripts to download email messages from a mailing list archive.

To exectue the scripts you must activate the python virtualenv.

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Then install dependencies 

```
pip install -r requirements.py
```

Or using make:

```
make install  # install
```

## Debian mailisting

Check File: `debian-mailinglist.yaml` and modify if neccesary.

Execution

```
python3 debian-malinglist.py
```

Download files should be at `output/` directory. 

or using make:

```
make donwload-debian # executes the script reading debian-mailinglist.yaml
```

### Create csv file

Creates a single csv file with all email messages downloades, useful for data analysis.

```
python3 utils/debianMailinglistToCsv.py
```

or using make:

```
make csv-debian # create a csv file from output
```

### All make commands

```
make prepared-dev # install system dependencies and python dependencies
make install # install pyython dependencies
make donwload-debian # donwloads debian mailinglist
make compress # compress output
make csv-debian # creates a single csv from output
make nuke # nukes!
```

> LICENSE: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
