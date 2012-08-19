import os
import time
import logging

import heroku
from celery import task
from celery.result import AsyncResult

from models import Instance
from django.conf import settings

# connect to heroku
cloud = heroku.from_key(settings.HEROKU_KEY)

def ex(call, ignore_error=False):
    logging.info('Exec: %s' % str(call))
    num = os.system(call)
    if num and not ignore_error:
        raise Exception('Error code: ' + str(num))

@task.task()
def setup_enviroment(session_key, tutorial_id):
    # try to find env by session id,
    # if not - setup new
    logger = setup_enviroment.get_logger()
    logger.info('Setup enviroment for %s session_key: %s' % (tutorial_id, session_key))
    inst = get_instance(session_key)
    init_tutorial(inst, tutorial_id)

@task.task()
def run_step(session_key, step, code):
    '''
    Run step tutorial code
    '''
    file_path = os.path.join(step.tutorial.app_name, step.file_path)
    inst = Instance.objects.get(session_key=session_key)
    # inst.write_file(file_path, code)
    write_file(inst, file_path, code)
    commit_instance(inst, 'Commit tutorial %s, step num %s' % (step.tutorial.pk, step.num), True)
    # return inst.get_logs()
    app = cloud.apps.get(inst.app)
    return app.logs(num=10)

def get_task(id):
    '''
    Return task by id
    TODO: define task structure in abstract class
    '''
    return AsyncResult(id)


def write_file(inst, file_path, code):
    path = os.path.join(settings.REPOS_PATH, inst.app, file_path)
    open(path, 'w').write(code)

@task.task()
def get_instance(session_key):
    '''
    Return instance for session_key
    '''
    logger = create_instance.get_logger()
    logger.info('Find heroku instance for session_key: %s' % session_key)

    try:
        inst = Instance.objects.get(session_key=session_key)
        app = cloud.apps.get(inst.app)
        if not app:
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

    ex('mkdir -p %(rp)s; mkdir -p %(ap)s' % locals()) # create repo dir
    ex('cd %(ap)s; git init;' % locals()) # remove all old files and init repo
    ex('cd %(ap)s; git rm -r *' % locals(), ignore_error=True)
    try:
        commit_instance(inst, 'empty')
    except Exception, e:
        logging.exception(e)
    ex('cp -r %(bp)s/* %(ap)s;' % locals()) # copy base tutorial
    ex('cd %(ap)s; git remote add heroku git@heroku.com:%(name)s.git' % locals(), ignore_error=True) # add remote heroku repos
    ex('cd %(ap)s; git add .;' % locals()) # commit base tutorial files
    commit_instance(inst, 'base tutorial files')

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
    ex('cp -r %(bp)s/* %(ap)s' % locals()) # copy tutorial files to the repo
    commit_instance(inst, 'Copy tutorial files %s' % tutid, True)

def commit_instance(inst, msg, push=False):
    ap = os.path.join(settings.REPOS_PATH, inst.app)
    ex('cd %(ap)s; git add .; git commit -m "%(msg)s" -a' % locals()) # commit init tutorial files
    logging.info('Deploy on heroku instance %s...' % inst.app)
    if push:
        ex('cd %(ap)s; git push heroku master' % locals())
