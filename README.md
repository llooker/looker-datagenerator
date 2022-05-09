# Data Generator

### This repo contains a ficitious data-generator that handles relationships between tables and fields within table(s)

### Setting up Enviornment

1. Clone repo

```
git clone https://github.com/llooker/looker-datagenerator.git
```

2. Set up [Virtual Enviornment](https://docs.python.org/3/tutorial/venv.html)

```
python3 -m venv MY_ENV
```

3. Install dependencies

```
pip install -r requirements.txt
```

### Directory Structure

1. Create a directory for your dataset if it doesn't exist
2. Inside your dataset directory, create a `yaml`, `code`, `output` directory

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

| Folder   | Description                                                         |
| -------- | ------------------------------------------------------------------- |
| `$DATASET`   | contains your dataset files                 |
| `code`   | contains the python code used to generate your data                 |
| `yaml`   | contains your YAML file that defines your schema/data relationships |
| `output` | contains your raw genereated data output (csv)                 |
