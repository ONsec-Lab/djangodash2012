import os
import time

import heroku
from celery import task
from celery.result import AsyncResult

from models import Inst
from django.conf import settings


def ex(call):
    num = os.system(call)
    if num:
        raise Exception('!!!!!!!!!')

@task.task()
def setup_enviroment(session_key):
    # try to find env by session id,
    # if not - setup new
    pass

@task.task()
def run_step(step, code):
    for x in range(0, 10):
        print 'Run code...'
        time.sleep(1)
    return 'successfuly finished\n'

def get_task(id):
    return AsyncResult(id)

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
    '''
    init empty git repository for new tutorial
    '''
    name = inst.app
    rp = settings.REPOS_PATH
    tp = settings.TUTORIALS_PATH
    ap = os.path.join(rp, inst.app)
    bp = os.path.join(tp, 'base')

    ex('mkdir -p %(rp)s; rm -rf %(ap)s; mkdir -p %(ap)s' % locals())
    ex('cp -r %(bp)s/* %(ap)s' % locals())
    ex('cd %(ap)s; git init; git add .; git commit -m "base"' % locals())
    ex('echo \'[remote "heroku"]\n\turl = git@heroku.com:%(name)s.git\n\tfetch = +refs/heads/*:refs/remotes/heroku/*\' >> %(ap)s/.git/config' % locals())


def init_tutorial(inst, tutid):
    '''
    rewrite tutorial specific files in repo,
    push changes to heroku
    '''
    init_git(inst)
    tp = settings.TUTORIALS_PATH
    ap = os.path.join(settings.REPOS_PATH, inst.app)
    bp = os.path.join(tp, str(tutid))
    ex('cp -r %(bp)s/* %(ap)s' % locals())
    ex('cd %(ap)s; git add .; git commit -m "%(tutid)s"' % locals())
    ex('cd %(ap)s; git push heroku master' % locals())

