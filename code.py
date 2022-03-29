from jinja2 import Template, Environment, FileSystemLoader
from jinja2.ext import Extension
import yaml
file_loader = FileSystemLoader("templates")


env = Environment(loader=file_loader, extensions=['jinja2.ext.do'])

# template = env.get_template("template.py.jinja2")
template = env.get_template("ecomm_template.py.jinja2")

#read yaml file
# with open("values.yaml", "r") as val:
with open("ecomm.yaml", "r") as val:
    values = yaml.safe_load(val)
    output = template.render(tables=values)
    #write python file
    with open("fake.py", "w") as out:
        out.write(output)
