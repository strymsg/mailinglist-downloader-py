# Mail listing downloader scripts

Collection of scripts to download emails from a mailing list archive.

To exectue the scripts you must activate the python virtualenv.

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Then install dependencies 

```
pip install -r requirements.py
```

## Debian mailist

Check File: `debian-mailisting.yaml` and modify if neccesary.

Execution

```
python3 debian-mailisting.py
```

Download files should be at `output directory` (developing)

LICENSE: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
