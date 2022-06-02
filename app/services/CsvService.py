from django.shortcuts import get_object_or_404
# from catalogs.models import Csv
from app.commons.constant import TIME_ZONE_CSV
from app.services import BaseService, FileService

import csv
import os
from datetime import datetime
import pytz

class CsvService(BaseService):

    def __init__(self) -> None:
        self.csv = {}#Csv
        self.fs = FileService()

    def get_list(self, **filters):
        queryset = self.csv.objects.select_related('user')
        return self.build_query_set(queryset, **filters).all()

    def get_only(self, *fields, only_value=False):
        if only_value:
            return self.csv.objects.values_list(*fields).all()
        else:
            return self.csv.objects.values(*fields).all()

    def create(self, **params):
        return self.csv.objects.create(**params)

    def delete(self, id):
        record = get_object_or_404(id)
        if record:
            filename = record.name
            record.delete()
            self.fs.delete(filename)
            return True
        return False

    def updateDatetimeColumnFromTimestampCsv(self, csv_path, timestampCol=2, datetimeCol=3, has_head=False, datetime_format='%Y-%m-%d %H:%M:%S'):
        bk_csv_path = f'{csv_path}.bk'
        track = {
            'has_head': not has_head,
            'row': 0
        }
        tz = pytz.timezone(TIME_ZONE_CSV)

        # Rename filename berfore processing
        os.rename(csv_path, bk_csv_path)

        def transform_row(row):
            """Add datetime values to `datetime` column from `timestamp` column of csv file"""
            track['row'] += 1
            if track['has_head']:
                timestamp = row[timestampCol - 1]
                # Its value is bool
                if isinstance(timestamp, bool):
                    raise Exception('Timestamp at [row={0}, col={1}] in csv file is invalid.'.format(track['row'], timestampCol))
                # If its value is a string, throw error
                try:
                    timestamp = int(timestamp)
                except Exception as e:
                    raise Exception('Timestamp at [row={0}, col={1}] in csv file is invalid.'.format(track['row'], timestampCol))
                row[datetimeCol - 1] = datetime.strftime(datetime.fromtimestamp(timestamp, tz), datetime_format)
            else:
                track['has_head'] = True
            return row

        # Update values of datetime column & write them to new file
        try:
            with open(bk_csv_path, 'r') as csv_in, open(csv_path, 'w', newline='') as csv_out:
                writer = csv.writer(csv_out)
                writer.writerows(transform_row(row) for row in csv.reader(csv_in))
                # for row in csv.reader(csv_in):
                #     track['row'] += 1
                #     if not track['has_head']:
                #         track['has_head'] = True
                #         writer.writerow(row)
                #     else:
                #         timestamp = row[timestampCol - 1]
                #         # Its value is bool
                #         if isinstance(timestamp, bool):
                #             raise Exception('Timestamp at [row={0}, col={1}] in csv file is invalid.'.format(track['row'], timestampCol))
                #         # If its value is a string, throw error
                #         try:
                #             timestamp = int(timestamp)
                #         except Exception as e:
                #             raise Exception('Timestamp at [row={0}, col={1}] in csv file is invalid.'.format(track['row'], timestampCol))
                #         row[datetimeCol - 1] = datetime.strftime(datetime.fromtimestamp(timestamp, tz), datetime_format)
                #         writer.writerow(row)
            # Delete csv file (backup)
            if os.path.exists(bk_csv_path):
                os.remove(bk_csv_path)
        except Exception as e:
            # Delete the writing csv file
            if os.path.exists(csv_path):
                os.remove(csv_path)
            # Delete the uploaded csv file
            if os.path.exists(bk_csv_path):
                os.remove(bk_csv_path)
            # Throw error
            raise Exception(str(e))

    @property
    def _allowed_filters(self):
        """ @override
            Mapping keys to filters of model
        """
        return {
            **self.super()._allowed_filters,
        }
