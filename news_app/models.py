from django.db import models


class Posts(models.Model):
    title = models.CharField('Заголовок статьи', max_length=300, unique=True, null=True)
    source = models.URLField('Ссылка на источник', max_length=500, unique=True, null=True)
    date = models.DateTimeField('Дата', null=True)
    img = models.URLField('favicon', max_length=500, null=True)

    def __str__(self):
        return self.title
