# Install

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Use

```
python -m googlesearch data.csv -
```

# API

```
from googlesearch import search, result_count
print(result_count(search("linux")))
```

# Help

```
python -m googlesearch -h
```

```
usage: __main__.py [-h] [--remove-duplicates] infile outfile

positional arguments:
  infile               file of keywords - one item per line
  outfile              file of keywords,result_count

optional arguments:
  -h, --help           show this help message and exit
  --remove-duplicates  removes duplicates: not recommended, remove before
                       supplying
```
