from django.template import RequestContext
from django.shortcuts import render_to_response

from forms import EditorForm

def index(request):
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))


def tutorial_start(request):
    return render_to_response('tutorial.html', {
            'editor_form': EditorForm()
        },
        context_instance=RequestContext(request))