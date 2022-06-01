import os
import shutil
from datetime import datetime
from urllib.parse import unquote
from django.core.files.storage import FileSystemStorage
from django.core.files import File, locks
from django.core.files.move import file_move_safe
from app.services.Log import Log

from app.settings.base import BASE_DIR, MEDIA_ROOT, MEDIA_URL

class FileService:
    """ @var FileSystemStorage """
    __fs = None

    @classmethod
    def fs(cls):
        if not cls.__fs:
            cls.__fs = FileSystemStorage(location=cls.__upload_root_path(), base_url=cls.__upload_base_url())
        return cls.__fs

    @classmethod
    def upload(cls, file):
        filename = cls.fs().save(file.name, file)
        return unquote(cls.fs().url(filename))

    @classmethod
    def exists(cls, url):
        url = cls.get_absolute_url(url)
        return os.path.exists(url)

    @classmethod
    def delete(cls, url):
        url = cls.get_absolute_url(url)
        if os.path.exists(url):
            os.remove(url)
        else:
            Log.warning(f'[Warning][FileService][File Not Exists] => {url}')

    @classmethod
    def readline(cls, name, mode='rb'):
        return cls.fs().readline(name, mode)

    @classmethod
    def from_resource(cls, content, name=None):
        if name is None:
            name = content.name
        return File(content, name)

    @classmethod
    def get_absolute_url(cls, url):
        url = "%s/%s" % (str(BASE_DIR), url.strip("/"))
        return url

    @classmethod
    def copy(cls, src_file, dest_file, follow_symlinks=True, preserved=True):
        if preserved == True:
            shutil.copy2(src_file, dest_file, follow_symlinks=follow_symlinks)
        else:
            shutil.copy(src_file, dest_file, follow_symlinks=follow_symlinks)

    @classmethod
    def copyfileobj(cls, src_file_object, dest_file_object, length=0):
        shutil.copyfileobj(src_file_object, dest_file_object, length=length)

    @staticmethod
    def __upload_path():
        now = datetime.now()
        return "uploads/%s/%s/%s" % (now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'))

    @classmethod
    def __upload_root_path(cls):
        return f"{MEDIA_ROOT}/{cls.__upload_path()}"

    @classmethod
    def __upload_base_url(cls):
        return "%s%s" % (MEDIA_URL, cls.__upload_path())
