from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from sw.commons.constant import PER_PAGE

from sw.services.FileService import FileService
from sw.services.Log import Log

class Core:

    request = {}

    @staticmethod
    def paginate(queryset, per_page=PER_PAGE, request=None):
        if isinstance(queryset, ModelBase):
            queryset = queryset.objects.all()
        elif not isinstance(queryset, QuerySet):
            raise Exception(f"Argument must be a Model or QuerySet.")

        page_number = 1

        if request:
            page_number = request.GET.get('page', 1)
        elif Core.request:
            page_number = Core.request.GET.get('page', 1)

        paginator = Paginator(queryset, per_page)

        return paginator.get_page(page_number)

        # try:
        #     paginator = paginator.page(page_number)
        # except PageNotAnInteger:
        #     paginator = paginator.page(1)
        # except EmptyPage:
        #     paginator = paginator.page(paginator.num_pages)

        # return paginator

    @staticmethod
    def fs():
        return FileService

    @staticmethod
    def log():
        return Log
