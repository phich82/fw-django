from django.db import IntegrityError, transaction

class DB:
    @staticmethod
    def beginTransaction():
        transaction.set_autocommit(False)

    @staticmethod
    def commit():
        transaction.commit()

    @staticmethod
    def rollback():
        transaction.rollback()

    def transaction(callback):
        with transaction.atomic():
            if callable(callback):
                callback()
