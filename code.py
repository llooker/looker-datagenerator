from jinja2 import Template, Environment, FileSystemLoader
import yaml
file_loader = FileSystemLoader("templates")

env = Environment(loader=file_loader)

template = env.get_template("template.py.jinja2")

#read yaml file
with open("values.yaml", "r") as val:
    values = yaml.safe_load(val)
    output = template.render(tables=values)
    #write python file
    with open("fake.py", "w") as out:
        out.write(output)
