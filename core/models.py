from os import path
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Tutorial(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    app_name = models.CharField(_('Django Application Name'),
        max_length=255,
        default='hellodjango')

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

    def get_results_url(self, request):
        '''
        Returl url to results for current user
        '''
        return 'http://172.16.240.130:8000/admin';

    def get_next_num(self):
        '''
        Returns url to the next step,
        if tutorial finished - return url to finish step
        '''
        next_num = self.num + 1
        if next_num > self.tutorial.steps_count():
            return None
        return next_num

STATUS_CHOICES = (
    ('new', _('New')),
    ('created', _('Created')),
    ('destroyed', _('Destroyed')),
)


class Instance(models.Model):
    session_key = models.CharField(_('User session key'), max_length=255)
    app = models.CharField(_('Heroku app id'), max_length=255, blank=True)
    status = models.CharField(_('Status'), max_length=10, default='new', choices=STATUS_CHOICES)
    url = models.CharField(_('URL'), max_length=255, blank=True)

    def __unicode__(self):
        return '%s' % self.app

    def get_code(self, step):
        code_path = path.join(settings.REPOS_PATH,
            self.app,
            step.tutorial.app_name,
            step.file_path)
        code = open(code_path, 'r').read()
        return code

