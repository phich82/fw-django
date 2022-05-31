def echo(inserted_pks=None):
    for model in inserted_pks:
        total = len(inserted_pks[model])
        print(f'{model.__name__}: inserted {total} record{"s" if total > 0 else ""}')
