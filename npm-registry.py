import os
import shutil
from sys import platform

packages_dir = ""
if platform == "linux" or platform == "linux2":
    packages_dir = "/home/runner/.local/share/verdaccio/"
elif platform == "darwin":
    packages_dir = "/home/runner/.local/share/verdaccio/"
elif platform == "win32":
    packages_dir = "C:/Users/runneradmin/AppData/Roaming/verdaccio" #C:\Users\Administrator\AppData\Roaming\verdaccio

print('platform', platform, packages_dir)

original_list = {}
try:
    with open("npm-packages.list", "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
        for line in lines:
            if line.strip() != '':
                g, sz = line.split(" ")
                g = g.replace('\\', '/')
                original_list[g] = sz
except Exception as e:
    print('no packages list found', e)
    pass

new_list = {}
for (dirpath, dirnames, filenames) in os.walk(packages_dir):
    for f in filenames:
        if f == 'package.json':
            continue
        relpath = os.path.relpath(dirpath, packages_dir)
        g = os.path.join(relpath, f)
        g = g.replace('\\', '/')
        sz = os.path.getsize(os.path.join(packages_dir, g))
        if not (g in original_list) or (str(original_list[g]) != str(sz)):
            new_list[g] = sz
            original_list[g] = sz


to_write = []            
for (g, sz) in original_list.items():
    to_write.append(f"{g} {sz}\n")
to_write.sort()

with open("npm-packages.list", "w", encoding='utf-8') as f:
    for t in to_write:
        f.write(t)

out_dir = 'packages'

os.makedirs(out_dir, exist_ok=True)
for (f, sz) in new_list.items():
    g = os.path.join(out_dir, f)
    d = os.path.dirname(g)
    os.makedirs(d, exist_ok=True)
    shutil.copyfile(os.path.join(packages_dir, f), g)

with open(os.path.join(out_dir, "new_packages.list"), "w", encoding="utf-8") as f:
    for (g, sz) in new_list.items():
        f.write(f"{g} {sz}\n")
        
if os.path.exists('package.json'):
    shutil.copyfile('package.json', f'{out_dir}/package.json')

if os.path.exists('package-lock.json'):
    shutil.copyfile('package-lock.json', f'{out_dir}/package-lock.json')

if os.path.exists('yarn.lock'):
    shutil.copyfile('yarn.lock', f'{out_dir}/yarn.lock')

if os.path.exists('pnpm-lock.yaml'):
    shutil.copyfile('pnpm-lock.yaml', f'{out_dir}/pnpm-lock.yaml')

shutil.copyfile('npm-packages.list', f'{out_dir}/npm-packages.list')
