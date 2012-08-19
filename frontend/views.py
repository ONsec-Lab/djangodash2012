import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from core.tasks import setup_enviroment, run_step, get_task
from core.models import Tutorial, Step, Instance
from forms import EditorForm

def index(request):
    return render_to_response('index.html', {},
        context_instance=RequestContext(request))

@ensure_csrf_cookie
@csrf_protect
def tutorial_start(request):
    '''
    Redirect to the start tutorial page
        check is there tutorial id in user sessions
        if not - start from first tutorial
    '''
    tutorial_id = request.session.get('tutorial_id')
    if tutorial_id is None:
        tutorial_id = Tutorial.objects.filter()[0].pk
    res = setup_enviroment.delay(request.session.session_key, tutorial_id)
    response_data = {
        'task_id': res.id
    }
    request.session['task_id'] = res.id
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def tutorial(request, tutorial_id):
    '''
    Tutorial page
        check if user already run tutorial and stop on some task_id
        redirect to task page
    '''
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    # TODO: get tutorial
    request.session['tutorial_id'] = tutorial_id
    # store task id in sessions
    tutorial_step_num = request.session.get('tutorial_step_num')
    if tutorial_step_num is None:
        tutorial_step_num = 1 # first step in tutorial
    return redirect('tutorial_step', tutorial_id=tutorial_id, step_num=tutorial_step_num)

def tutorial_step(request, tutorial_id, step_num):
    '''
    Tutorial step
    '''
    request.session['tutorial_id'] = tutorial_id
    request.session['tutorial_step_num'] = step_num

    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    try:
        step = tutorial.step_set.get(num=step_num)
    except Step.DoesNotExist as e:
        raise Http404()

    try:
        inst = Instance.objects.get(session_key=request.session.session_key)
    except Instance.DoesNotExist as e:
        return redirect('index')

    results_url = 'http://%s.herokuapp.com/' % inst.app
    editor_form = None
    if step.enable_editor:
        initial = {
            'code': inst.get_code(step)
        }
        editor_form = EditorForm(initial=initial)

    next_num = step.get_next_num()
    if next_num is None:
        next_url = reverse('tutorial_finish', kwargs={
            'tutorial_id': tutorial_id
        })
    else:
        next_url = reverse('tutorial_step', kwargs={
            'tutorial_id': tutorial_id,
            'step_num': next_num
        })
    return render_to_response('tutorial.html', {
            'tutorial': tutorial,
            'step': step,
            'results_url': results_url,
            'next_url': next_url,
            'editor_form': editor_form
        },
        context_instance=RequestContext(request))

def tutorial_finish(request, tutorial_id):
    '''
    Display finish page for tutorial
    '''
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    return render_to_response('tutorial_finish.html', {
        'tutorial': tutorial
    }, context_instance=RequestContext(request))

@ensure_csrf_cookie
@csrf_protect
def tutorial_step_run(request, tutorial_id, step_num):
    '''
    Run user code
    Returns task id, that run user code
    '''
    if not request.is_ajax() or request.method != 'POST':
        raise Http404()
    tutorial = get_object_or_404(Tutorial, pk=tutorial_id)
    try:
        step = tutorial.step_set.get(num=step_num)
    except Step.DoesNotExist as e:
        raise Http404()
    try:
        data = json.loads(request.raw_post_data)
        code = data['code']
    except (KeyError, ValueError) as e:
        print e
        raise Http404()
    res = run_step.delay(request.session.session_key, step, code)
    request.session['task_id'] = res.id
    response_data = {
        'task_id': res.id
    }
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def task(request, task_id):
    '''
    Check runned task status
    '''
    # sequrity check
    if request.session.get('task_id') != task_id:
        raise Http404()
    task = get_task(task_id)
    # task = get by id
    task_json = {
        'running': not task.ready()
    }
    if task.ready():
        try:
            task_json['results'] = task.get()
        except:
            task_json['errors'] = True
    return HttpResponse(json.dumps(task_json), mimetype="application/json")