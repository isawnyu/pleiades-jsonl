# (Down)load Pleiades gazetteer JSON dumps and convert to JSONL

## What?

### Pleiades

A community-built gazetteer and graph of ancient places: https://pleiades.stoa.org/

### JSON Lines

A convenient format for storing structured data that may be processed one record at a time (a.k.a. newline-delimited JSON): http://jsonlines.org/


## Usage

```
$ python pleiades-jsonl.py -h
usage: pleiades-jsonl.py [-h] [-l LOGLEVEL] [-v] [-w] [-p PLEIADES]

Convert Pleiades JSON dump to JSON Lines (new-line-delimited JSON)

optional arguments:
  -h, --help            show this help message and exit
  -l LOGLEVEL, --loglevel LOGLEVEL
                        desired logging level (case-insensitive string: DEBUG,
                        INFO, WARNING, or ERROR (default: WARNING)
  -v, --verbose         verbose output (logging level == INFO) (default:
                        False)
  -w, --veryverbose     very verbose output (logging level == DEBUG) (default:
                        False)
  -p PLEIADES, --pleiades PLEIADES
                        Pleiades JSON dataset to use (default: http://atlantid
                        es.org/downloads/pleiades/json/pleiades-places-
                        latest.json.gz) (default: http://atlantides.org/downlo
                        ads/pleiades/json/pleiades-places-latest.json.gz)
```

Use the ```-p``` (```--pleiades```) option to specify an alternative remote or local source file. An uncompressed file may be specified, if available. If the filename ends in ".gz", the script will attempt to uncompress it and store the uncompressed version in the local directory. 

The script writes the result to the local directory with teh filename: ```{inputfilename-minus-extension}.jsonl```

## Dependencies

 * Python 3.x (tested on 3.5.2)
 * [jsonlines](https://jsonlines.readthedocs.io/en/latest/)
 * [progressbar2](http://pythonhosted.org/progressbar2/)
 * [wget](https://pypi.python.org/pypi/wget)

## Todo

 * Convert to package for better distribution and requirements management.
 
