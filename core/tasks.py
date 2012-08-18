import os
from os import system as ex

import heroku
from models import Inst
from django.conf import settings
import tutorials


def create_instance(user):
    inst = Inst()
    inst.save()
    cloud = heroku.from_key(settings.HEROKU_KEY)
    name = 'rocket-%s-%s' % (user.id, inst.id)
    cloud.apps.add(name)
    inst.app = name
    inst.save()
    return name


def init_git(inst):
    path = settings.TUTORIALS_PATH
    ex('cd ~/repos/')
    ex('rm -rf %s' % inst.app)
    ex('mkdir %s' % inst.app)
    ex('cd %s' % inst.app)
    ex('cp -r %s .' % os.path.join(path, 'base'))
    ex('git init')
    ex('git add .')
    ex('git commit -m "init"')

def init_tutorial(inst, tutid):
    init_git(inst)
