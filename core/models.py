from os import path
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Tutorial(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    app_name = models.CharField(_('Django Application Name'), max_length=255, default='hellodjango')

    def __unicode__(self):
        return u'%s' % unicode(self.title)

    def steps_count(self):
        return self.step_set.all().count()


class Step(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    num = models.SmallIntegerField(_('Number in Order'))
    tutorial = models.ForeignKey(Tutorial)
    description = models.TextField(_('Description'))
    file_path = models.CharField(_('File Path'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % unicode(self.title)

    def get_code(self):
        code_path = path.join(settings.TUTORIALS_PATH,
            str(self.tutorial.pk),
            self.tutorial.app_name,
            self.file_path)
        code = open(code_path, 'r').read()
        return code


class OurUser(models.Model):
    def __unicode__(self):
        return unicode(self.id)

STATUS_CHOICES = (
    ('new', _('New')),
    ('created', _('Created')),
    ('destroyed', _('Destroyed')),
)


class Inst(models.Model):
    ouruser = models.ForeignKey(OurUser, verbose_name=_('User'), null=True)
    app = models.CharField(_('Heroku app id'), max_length=255, blank=True)
    status = models.CharField(_('Status'), max_length=10, default='new', choices=STATUS_CHOICES)
    url = models.CharField(_('URL'), max_length=255, blank=True)
