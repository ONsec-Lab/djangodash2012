import heroku
from models import Inst
from django.conf import settings


def create_instance(user):
    inst = Inst()
    inst.save()
    cloud = heroku.from_key(settings.HEROKU_KEY)
    name = 'rocket-%s-%s' % (user.id, inst.id)
    cloud.apps.add(name)
    inst.app = name
    inst.save()
    return name
