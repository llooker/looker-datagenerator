# Data Generator

### This repo contains a ficitious data-generator that handles relationships between tables and fields within table(s)

### Set-Up

1. Setting Up Enviornment

Clone repo

```
git clone https://github.com/llooker/looker-datagenerator.git
```

Set up [Virtual Enviornment](https://docs.python.org/3/tutorial/venv.html)

```
python3 -m venv MY_ENV
```

Install dependencies

```
pip install -r requirements.txt
```

2. Directory Structure

- Create a directory for your dataset if it doesn't exist
- Inside your dataset directory, create a `yaml`, `code`, `output` directory

The file tree for your dataset should look like this:

```
datasets/
└── $DATASET/
   ├─ code/
        └─ yaml1.py
        └─ yaml2.py
        └─ ...
   └─ output/
        └─ table1.csv
        └─ table2.csv
        └─ ...
   └── yaml/
        └─ schema1.yaml
        └─ schema2.yaml
        └─ ...
```
