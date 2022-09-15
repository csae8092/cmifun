import glob
import jinja2
import os

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)

print('hallo, lets start building')

for x in glob.glob('./html/*.html'):
    os.unlink(x)

files = glob.glob('./templates/static/*.j2')
print('building static content')
for x in files:
    template = templateEnv.get_template(x)
    _, tail = os.path.split(x)
    with open(f'./html/{tail.replace(".j2", ".html")}', 'w') as f:
        f.write(template.render({"objects": {}}))