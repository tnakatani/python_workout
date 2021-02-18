# Python Workout

This repo contains code I wrote to solve challenges in the book _Python Workout_ by Reuven Lerner.

## Requirements

Python environment requirements are listed in the environment.yaml file.  This file was created by the following 
command:
```
conda env export > environment.yaml
```

## Repo at a glance

```
# tree -I __pycache__ | pbcopy

.
├── README.md
├── __init__.py
├── environment.yaml
├── notes.md
├── src
│   ├── __init__.py
│   ├── comprehensions
│   │   └── comprehensions.py
│   ├── dicts_sets
│   │   └── dicts_sets.py
│   ├── files
│   │   ├── data
│   │   │   ├── log.txt
│   │   │   └── nums.tsv
│   │   └── files.py
│   ├── functions
│   │   └── functions.py
│   ├── lists_tuples
│   │   ├── __init__.py
│   │   └── list_tuples.py
│   ├── modules
│   │   ├── menu
│   │   │   ├── call_menu.py
│   │   │   └── menu.py
│   │   └── tax
│   │       ├── calculate_tax.py
│   │       └── freedonia.py
│   ├── numbers
│   │   ├── __init__.py
│   │   └── numbers.py
│   ├── objects
│   │   ├── dummy.log
│   │   └── objects.py
│   └── strings
│       ├── __init__.py
│       ├── pig_latin.py
│       ├── strsort.py
│       └── ubbi_dubbi.py
└── test
    ├── __init__.py
    ├── comprehensions
    │   └── test_comprehensions.py
    ├── dicts_sets
    │   ├── __init__.py
    │   └── test_dicts_sets.py
    ├── files
    │   ├── __init__.py
    │   └── test_files.py
    ├── functions
    │   └── functions.py
    ├── lists_tuples
    │   ├── __init__.py
    │   └── test_list_tuples.py
    ├── modules
    │   └── tax
    │       └── test_calculate_tax.py
    ├── numbers
    │   ├── __init__.py
    │   ├── test_mysum.py
    │   ├── test_run_timing.py
    │   └── test_to_hex.py
    ├── objects
    │   ├── dummy.log
    │   └── test_objects.py
    ├── output.tsv
    ├── output.txt
    └── strings
        ├── __init__.py
        ├── test_pig_latin.py
        ├── test_strsort.py
        └── test_ubbi_dubbi.py

24 directories, 47 files
```