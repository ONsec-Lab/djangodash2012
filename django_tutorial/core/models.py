from django.db import models


class Tutorial(models.Model):
    title = models.CharField('Title', max_length=255)

    def __unicode__(self):
        return u'%s' % unicode(self.title)

    def steps_count(self):
        return self.step_set.all().count()

class Step(models.Model):
    title = models.CharField('Title', max_length=255)
    num = models.SmallIntegerField('Number in Order')
    tutorial = models.ForeignKey(Tutorial)
    description = models.TextField('Description')

    def __unicode__(self):
        return u'%s' % unicode(self.title)