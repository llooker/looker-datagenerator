from jinja2 import Environment, FileSystemLoader

import click
import os
import yaml

file_loader = FileSystemLoader("./templates")

class Table:
    def table_name(self, table):
        return f"class { table }(DataUtil.DataUtil):"

    def init_fields(self, table, tables):
        output = ""
        for key, value in tables[table].items():
            if "primary_key" in value:
                output += f"\t{key}: {value['type']} = dataclasses.field(default_factory=itertools.count(start=1).__next__)\n"
            else:
                output += f"\t{key}: {value['type']} = dataclasses.field(init=False)\n"
        return output

    def parse_relationships(self, table, tables):
        output = ""
        foreign_key_list = []
        for key, value in tables[table].items():
            if "foreign_key" in value:
                foreign_key_value = value['foreign_key'].split('.')[0]
                foreign_key_list.append(foreign_key_value)
                output += f"\t{foreign_key_value}:dataclasses.InitVar[typing.Any] = None\n"

        if len(foreign_key_list) > 0:
            output += f"\tdef __post_init__(self, {self.helper_initialize_joins(foreign_key_list)}):"
        else:
            output += f"\tdef __post_init__(self):"
        return output

    def post_init(self, table, tables):
        output = ""
        dependents = dict()
        for key, value in tables[table].items():
            if "primary_key" not in value:
                if self.helper_parse_values(key, value, tables[table]) is not None:
                    output += self.helper_parse_values(key,
                                                       value, tables[table])
        return output

    def append_output(self, table, tables):
        return f"\t\t{table.lower() }_out.append(dataclasses.asdict(self))"

    def print_str(self, table, tables):
        output = "\tdef __str__(self):\n"
        tmp_out = "\t\treturn f'"
        keys = list(tables[table].keys())

        for key in keys[:-1]:
            tmp_out += f"{{self.{key}}},"
        tmp_out += f"{{self.{keys[-1]}}}'\n"  # lol
        output += tmp_out
        return output

    def helper_initialize_joins(self, foreign_keys):
        output = ""
        for key in foreign_keys[:-1]:
            output += f"{key}=None" + ", "
        output += foreign_keys[-1] + "=None"
        return output

    def helper_parse_values(self, key, value, table):
        output = ""
        if value["type"] == "datetime" and "min_date" in value:
            date = value["min_date"]
            return f"\t\tself.{key} = self.created_at(datetime.datetime({date['year']}, {date['month']}, {date['day']}))\n"
        elif all(k in value for k in ("values", "distribution")):
            return f"\t\tself.{key} = self.random_item(population={value['values']}, distribution={value['distribution']})\n"
        elif "values" in value:
            return f"\t\tself.{key} = self.random_item(population={value['values']})\n"
        elif key == "phone_number":
            return f"\t\tself.{key} = fake.phone_number()\n"
        elif key == "last_name":
            return f"\t\tself.{key} = fake.last_name_nonbinary()\n"
        elif key == "email" and "domain" in value:
            return f"\t\tself.{key} = f'{{self.first_name.lower()}}{{self.last_name.lower()}}@{value['domain']}'\n"
        elif key == "email" and "domain" not in value:
            return f"\t\tself.{key} = f'{{self.first_name.lower()}}{{self.last_name.lower()}}@{{fake.safe_domain_name()}}'\n"
        elif key == "user_name":
            return f"\t\tself.{key} = fake.user_name()"
        elif "path" in key:
            return f"\t\tself.{key} = fake.uri_path()"
        elif "random_digits" in value:
            return f"\t\tself.{key} = fake.bothify('#' * {value['random_digits']})\n"
        elif "depends_on" in value:
            # single dependency
            if len(value["depends_on"]) == 1 and value["depends_on"][0] == "gender":
                dependent_var = value["depends_on"][0]
                for i in table[dependent_var]["values"]:
                    output += f"\t\tif self.{dependent_var} == '{i}':\n"
                    output += f"\t\t\tself.{key} = fake.first_name_{i}()\n"
                return output
            elif len(value["depends_on"]) == 1 and "mapping" in value:
                dependent_var = value["depends_on"][0]
                for i in table[dependent_var]["values"]:
                    output += f"\t\tif self.{dependent_var} == '{i}':\n"
                    output += f"\t\t\tself.{key} = self.random_item(population={table[key]['mapping'][i]})\n"
                return output
        elif "foreign_key" in value:
            return f"\t\tself.{key} == {value['foreign_key']}\n"
        elif "dist" in value:
            num = value["dist"]
            return f"\t\tself.{key} = self.random_int({num['min']}, {num['max']})\n"
        elif "words" in value:
            max_words = value["words"]["max"]
            return f"\t\tself.{key} = fake.sentence(nb_words={max_words})\n"


env = Environment(loader=file_loader, extensions=['jinja2.ext.do'])
template = env.get_template("datagen_template.py.jinja2")
template.globals['Table'] = Table()

# read yaml file

@click.command()
@click.option('--dataset', prompt='Your dataset name',
              help='Name of your dataset')
@click.option('--yaml_file', prompt='Your YAML file',
              help='Name of your YAML file')
@click.option('--num_of_records', default=100, prompt='Number of rows to generate',
              help='Number of rows to generate')
def generate_code(dataset:str, yaml_file:str, num_of_records:int):
    with open(f"./datasets/{dataset}/yaml/{yaml_file}.yaml", "r") as val:
        values = yaml.safe_load(val)
        output = template.render(tables=values, yaml_file=yaml_file, num_of_records=num_of_records)
        # write python file
        with open(f"./datasets/{dataset}/code/{yaml_file}.py", "w") as out:
            out.write(output)


if __name__ == '__main__':
    generate_code()

def create_or_update_dir(dir_path: str):
    try:
        os.mkdir(dir_path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)