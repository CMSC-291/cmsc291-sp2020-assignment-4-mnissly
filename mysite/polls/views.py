from django.utils import timezone

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def add_question(request):
    new_question = Question(question_text=request.POST['new_question'], pub_date=timezone.now())
    new_question.save()
    return HttpResponseRedirect(reverse('polls:detail', args=(new_question.id,)))


def add_choice(request, question_id):
    associated_question = get_object_or_404(Question, pk=question_id)
    new_choice = Choice(choice_text=request.POST['new_choice'], votes=0, question=associated_question)
    new_choice.save()
    return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def remove_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(reverse('polls:index'))


def remove_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    question = choice.question
    choice.delete()
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
