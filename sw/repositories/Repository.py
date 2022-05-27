from django.db import IntegrityError, transaction

class Repository:
    model = None
    # Model.objects.raw('SELECT * FROM myapp_person')
    # Model.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', ['lname'])

    def find(self, id):
        # return Model.objects.in_bulk([id])
        pass

    def insert(data):
        pass

    def insert_many(rows):
        # Model.objects.bulk_create([
        #     Entry(headline='This is a test'),
        #     Entry(headline='This is only a test'),
        # ])
        pass

    def update(self):
        pass

    def update_many(self, **kwargs):
        # return Model.objects.all().update(**kwargs)

        # Trigger atomic transaction so loop is executed in a single transaction
        # with transaction.atomic():
        #     store_list = Model.objects.select_for_update().filter(state='CA')
        #     # Loop over each store to update and invoke save() on each entry
        #     for store in store_list:
        #         # Add complex update logic here for each store
        #         # save() method called on each member to update
        #         store.save()
        pass

    def delete(self, id):
        return self.delete_many([id])

    def delete_many(self, ids):
        if isinstance(ids, str):
            ids = ids.split(',')
        # return Model.objects.filter(id__in=ids).delete()
        pass
