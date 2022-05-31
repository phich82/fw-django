from django.db import IntegrityError, transaction
from datetime import datetime

class Repository:

    def find(self, id):
        return self.objects.in_bulk([id])

    def insert(self, data):
        return self.objects.create(**data)

    def insert_many(self, rows):
        return self.objects.bulk_create(rows)

    def update(self):
        pass

    def update_many(self, conditions, **params):
        return self.objects.filter(**conditions).update(**params)

        # Trigger atomic transaction so loop is executed in a single transaction
        # with transaction.atomic():
        #     store_list = self.objects.select_for_update().filter(state='CA')
        #     # Loop over each store to update and invoke save() on each entry
        #     for store in store_list:
        #         # Add complex update logic here for each store
        #         # save() method called on each member to update
        #         store.save()
        pass

    def destroy(self, id):
        return self.delete_many([id])

    def delete_many(self, ids):
        if isinstance(ids, str):
            ids = ids.split(',')
        return self.objects.filter(id__in=ids).delete()

    def formated_created_at(self):
        # return self.created_at.strftime('%d/%m/%Y')
        return datetime.strftime(self.created_at, '%d/%m/%Y')

    def formated_updated_at(self):
        # return self.updated_at.strftime('%d/%m/%Y')
        return datetime.strftime(self.updated_at, '%d/%m/%Y')
