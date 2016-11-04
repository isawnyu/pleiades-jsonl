# (Down)load Pleiades gazetteer JSON dumps and convert to JSONL

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
 * jsonlines
 * progressbar2
 * wget

## Todo

 * Convert to package for better distribution and requirements management.
 
