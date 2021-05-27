from django.db import models


# Create your models here.
class post_habr(models.Model):
    post_title = models.CharField('Заголовок статьи', max_length=300, unique=True, null=True)
    post_source = models.URLField('Ссылка на источник', max_length=500, unique=True, null=True)
    pub_date = models.DateTimeField('Дата', null=True)


class post_tproger(models.Model):
    post_title = models.CharField('Заголовок статьи', max_length=300, unique=True, null=True)
    post_source = models.URLField('Ссылка на источник', max_length=500, unique=True, null=True)
    pub_date = models.DateTimeField('Дата', null=True)


class post_dnews(models.Model):
    post_title = models.CharField('Заголовок статьи', max_length=300, unique=True, null=True)
    post_source = models.URLField('Ссылка на источник', max_length=500, unique=True, null=True)
    pub_date = models.DateTimeField('Дата', null=True)
