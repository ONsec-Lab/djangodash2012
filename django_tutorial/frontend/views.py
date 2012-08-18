from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from forms import EditorForm

def index(request):
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

def tutorial_start(request):
    tutorial_id = request.session.get('tutorial_id')
    if tutorial_id is None:
        tutorial_id = 1
    kwargs = {'tutorial_id': tutorial_id}
    return redirect('tutorial', **kwargs)

def tutorial(request, tutorial_id):
    return render_to_response('tutorial.html', {
            'editor_form': EditorForm()
        },
        context_instance=RequestContext(request))
