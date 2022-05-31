# !/bin/bash

# python manage.py shell < revert_seed.py
# sh revert_seed.py

import json
import glob

g = globals()
has_access = {}
fixtures = glob.glob("./app/migrations/seeds/jsons/*.json")
fixtures.sort(reverse=True)

def get_access(model):
    import importlib

    mod = importlib.import_module(model)
    names = getattr(mod, '__all__', [n for n in dir(mod) if not n.startswith('_')])

    global g
    for name in names:
        g[name.lower()] = {
            'var': getattr(mod, name),
            'name': name
        }

for fixture in fixtures:
    msg = 'Reverting '+fixture+'\n'
    with open(fixture) as json_file:
        datas = json.load(json_file)
        for data in datas:
            app_name = data['model'].split('.')[0]
            class_name = data['model'].split('.')[1]

            if app_name not in has_access.keys():
                get_access(f'{app_name}.models')
                has_access[app_name] = True

            class_model = g[class_name]['var']
            class_model_name = g[class_name]['name']
            pk = data['pk']

            msg += '{}(pk={}): '.format(class_model_name, pk)
            try:
                class_model.objects.get(pk=pk).delete()
                msg += 'deleted\n'
            except:
                msg += 'not deleted\n'
    print(msg)
