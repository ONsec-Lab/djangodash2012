import os
import time
import logging

import heroku
from celery import task
from celery.result import AsyncResult

from models import Instance
from django.conf import settings


def ex(call):
    num = os.system(call)
    if num:
        raise Exception('Error code: ' + num)

@task.task()
def setup_enviroment(session_key, tutorial_id):
    # try to find env by session id,
    # if not - setup new
    logger = setup_enviroment.get_logger()
    logger.info('Setup enviroment for %s session_key: %s' % (tutorial_id, session_key))
    inst = get_instance(session_key)
    # init_tutorial(inst, tutorial_id)

@task.task()
def run_step(step, code):
    for x in range(0, 10):
        print 'Run code...'
        time.sleep(1)
    return 'successfuly finished\n'

def get_task(id):
    '''
    Return task by id
    TODO: define task structure in abstract class
    '''
    return AsyncResult(id)

@task.task()
def get_instance(session_key):
    '''
    Return instance for session_key
    '''
    logger = create_instance.get_logger()
    logger.info('Find heroku instance for session_key: %s' % session_key)

    try:
        inst = Instance.objects.get(session_key=session_key)
        cloud = heroku.from_key(settings.HEROKU_KEY)
        if cloud.apps.get(inst.app).status == 'new':
            inst.delete()
            raise Instance.DoesNotExist()
    except Instance.DoesNotExist:
        inst = create_instance(session_key)
    return inst

@task.task()
def create_instance(session_key):
    '''
    Create heroku instance
    Returns instance
    '''
    logger = create_instance.get_logger()
    logger.info('Create heroku instance for session_key: %s' % session_key)
    cloud = heroku.from_key(settings.HEROKU_KEY)
    inst = Instance.objects.create(session_key=session_key)
    name = 'rocket-%s' % (inst.id)
    logger.info('Create heroku instance for session_key: %s, name: %s' % (session_key, name))
    cloud.apps.add(name)
    inst.app = name
    inst.save()
    return inst

@task.task()
def init_git(inst):
    '''
    init empty git repository for new tutorial
    '''
    logger = init_git.get_logger()
    logger.info('Init git repository...')
    name = inst.app
    rp = settings.REPOS_PATH
    tp = settings.TUTORIALS_PATH
    ap = os.path.join(rp, inst.app)
    bp = os.path.join(tp, 'base')

    ex('mkdir -p %(rp)s; rm -rf %(ap)s; mkdir -p %(ap)s' % locals())
    ex('cp -r %(bp)s/* %(ap)s' % locals())
    ex('cd %(ap)s; git init; git add .; git commit -m "base"' % locals())
    ex('echo \'[remote "heroku"]\n\turl = git@heroku.com:%(name)s.git\n\tfetch = +refs/heads/*:refs/remotes/heroku/*\' >> %(ap)s/.git/config' % locals())

@task.task()
def init_tutorial(inst, tutid):
    '''
    rewrite tutorial specific files in repo,
    push changes to heroku
    '''
    logger = init_tutorial.get_logger()
    logger.info('Init tutorial %s...' % tutid)
    init_git(inst)
    tp = settings.TUTORIALS_PATH
    ap = os.path.join(settings.REPOS_PATH, inst.app)
    bp = os.path.join(tp, str(tutid))
    ex('cp -r %(bp)s/* %(ap)s' % locals())
    ex('cd %(ap)s; git add .; git commit -m "%(tutid)s"' % locals())
    logger.info('Deploy on heroku instance %s...' % inst.app)
    ex('cd %(ap)s; git push heroku master' % locals())
