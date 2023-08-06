# Top Drawer

Ever had trouble finding a valid name for that new package ? 

`top-drawer` is command line tool to help with that by searching for synonyms and validate if they are available on pypi or npm.

### Install

Python >= 3.6:

`$ pip install top-drawer`

### Usage

```
$ top-drawer --help
top-drawer 0.0.1
usage: top-drawer [-h] [-v] {search,validate,clear-cache} ...

    Search for synonyms and validate if the name is available on pypi or npm.
    

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose

Commands:
  {search,validate,clear-cache}
    search              Search for valid synonyms of the provided word.
    validate            Validate a name is available
    clear-cache         Clear the validations cache.
```

```
$ top-drawer search --help                                                                                                                                      ✔  17:37 
top-drawer 0.0.1
usage: top-drawer search [-h] [-c {snakecase,spinalcase}] [--pypi] [--npm]
                         [-f] [--definition DEFINITION]
                         word

Search for valid synonyms of the provided word.

positional arguments:
  word                  The word to generate synonyms for

optional arguments:
  -h, --help            show this help message and exit
  -c {snakecase,spinalcase}, --casing {snakecase,spinalcase}
                        The casing to apply to synonyms (default: spinalcase)
  --pypi                Disable validation on pypi (default: True)
  --npm                 Disable validation on npm (default: True)
  -f, --full            Include the invalids in the output (default: False)
  --definition DEFINITION
                        Set to a number representing the tab of the search
                        result on thesaurus.com or `all`. (default: 0)
```

## Links

- [thesaurus](https://github.com/Manwholikespie/thesaurus)
- [precept](https://github.com/T4rk1n/precept)
