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


class Subscription(models.Model):
    name = models.CharField(max_length=64)
    describe = models.TextField()
    account = models.CharField(max_length=64)
    origin_id = models.CharField(max_length=32)
    app_id = models.CharField(max_length=32)
    app_secret = models.CharField(max_length=64)
    token = models.CharField(max_length=32)
    encodingaesKey = models.CharField(max_length=43)
    head_img = models.CharField(max_length=32)
    qrcode_img = models.CharField(max_length=32)
    access_token = models.CharField(max_length=128)
    last_date = models.DateTimeField()
    type = TinyIntField()
    status = TinyIntField()
    group_id = TinyIntField()
    date_added = models.DateTimeField()
