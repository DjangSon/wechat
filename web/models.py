from django.db import models

# Create your models here.


class TinyIntField(models.IntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'tinyint'
        else:
            return 'int'


class Users(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    group_id = TinyIntField()
    status = TinyIntField(default=1)
    remark = models.CharField(max_length=64)
    date_added = models.DateTimeField()
