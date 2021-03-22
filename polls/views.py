from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from celery.result import AsyncResult
from gyoiboard.tasks import add, executation
from .models import Question, Choice


def celery_test(request):
    task_id = add.delay(5, 5)
    result = AsyncResult(task_id)
    print('result:', result, ' : ', result.state, ' : ', result.ready())
    context = {'result': result}
    return render(request, 'polls/celery_test.html', context)


def celery_test2(request):
    task_id = executation.delay('python3 /home/itakaesu/PycharmProjects/GyoiThon/gyoithon.py -h')
    result = AsyncResult(task_id)
    print('result:', result, ' : ', result.state, ' : ', result.ready())
    context = {'result': result}
    return render(request, 'polls/celery_test.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
