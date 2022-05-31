# Data Generator

### This repo contains a ficitious data-generator that handles relationships between tables and fields within table(s)

Steps to Generate Synthetic Data
1. Create **YAML** file ([example](https://github.com/llooker/looker-datagenerator/blob/main/datasets/ga4/yaml/ga4.yaml)) which specifies your data relationships and values
2. Run `scripts/generate_code.py` to create the **Python Script** based on YAML
3. Run the python script to produce ficitious output

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

### Set Up your Dataset and generate data

1. Within your `$DATASET/yaml` directory add your custom YAML file(s)
2. From the root directory, run `generate_code.py` to create the Python code for your YAML file(s)

```
python scripts/generate_code.py \
    --dataset $DATASET \
    --yaml_file $YAML_FILE \
    --num_of_records $NUM_OF_RECORDS 
```
This will create your `yaml.py` file within your dataset's YAML directory `$DATASET/yaml/`

3. Run your python code to generate the output(s) of your dataset. 

From the ***root directory*** (replace `$DATASET` with your dataset name, replace `MY_CUSTOM_CODE.py` with your dataset's `.py` file name)

```
python scripts/datasets/$DATASET/code/MY_CUSTOM_CODE.py`
```

Running your code will generate raw files for your schema into the `$DATASETS/output` directory
