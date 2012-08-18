from django.db import models


class Tutorial(models.Model):
    title = models.CharField('Title', max_length=255)

    def __unicode__(self):
        return u'%s' % unicode(self.title)

class Step(models.Model):
    title = models.CharField('Title', max_length=255)
    tutorial = models.ForeignKey(Tutorial)
    description = models.TextField('Description')

    def __unicode__(self):
        return u'%s' % unicode(self.title)