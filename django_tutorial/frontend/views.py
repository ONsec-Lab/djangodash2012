import json

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from forms import EditorForm

def index(request):
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

def tutorial_start(request):
    '''
    Redirect to the start tutorial page
        check is there tutorial id in user sessions
        if not - start from first tutorial
    '''
    tutorial_id = request.session.get('tutorial_id')
    if tutorial_id is None:
        tutorial_id = 1
    return redirect('tutorial', tutorial_id=tutorial_id)

def tutorial(request, tutorial_id):
    '''
    Tutorial page
        check if user already run tutorial and stop on some task_id
        redirect to task page
    '''
    # TODO: get tutorial
    request.session['tutorial_id'] = tutorial_id
    # store task id in sessions
    tutorial_step = request.session.get('tutorial_step')
    if tutorial_step is None:
        tutorial_step = 1 # default task_id
    return redirect('tutorial_step', tutorial_id=tutorial_id, step=tutorial_step)

def tutorial_step(request, tutorial_id, step_id):
    request.session['tutorial_id'] = tutorial_id
    request.session['tutorial_step'] = step_id
    # tutorial = ...
    tutorial = {
        'id': 1
    }
    # step = ...
    step = {
        'id': 1
    }
    return render_to_response('tutorial.html', {
            'tutorial': tutorial,
            'step': step,
            'editor_form': EditorForm()
        },
        context_instance=RequestContext(request))

@ensure_csrf_cookie
@csrf_protect
def tutorial_step_run(request, tutorial_id, step_id):
    '''
    Run user code
    Returns task id, that run user code
    '''
    if not request.is_ajax() or request.method != 'POST':
        raise Http404()
    # task = TutorialStep.objects.get(tutorial_id=tutorial_id, step=step_id)
    try:
        data = json.loads(request.raw_post_data)
        code = data['code']
    except (KeyError, ValueError) as e:
        raise Http404()
    # task_id = step.run(code)
    task_id = 1
    request.sessions.get['task_id'] = task_id
    response_data = {
        'task_id': task_id
    }
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def check_task_status(request, task_id):
    '''
    Check runned task status
    '''
    # sequrity check
    if request.sessions.get('task_id') != task_id:
        raise Http404()
    # task = get by id
    task = {
        'status': 'running'
    }
    return HttpResponse(json.dumps(task), mimetype="application/json")