from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language_from_request
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from molo.core.utils import get_locale_code
from molo.core.models import get_translation_for
from molo.polls.forms import TextVoteForm, VoteForm, NumericalTextVoteForm
from molo.polls.models import (
    Choice, Question, FreeTextVote, ChoiceVote, FreeTextQuestion)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class PollsDetailsView(TemplateView):
    template_name = 'polls/polls_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            PollsDetailsView, self).get_context_data(*args, **kwargs)
        context.update({
            'question': Question.objects.get(pk=kwargs.get('question_id'))
        })
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def poll_results(request, poll_id):
    question = get_object_or_404(Question, pk=poll_id)
    page = question.get_main_language_page()
    qs = Choice.objects.live().child_of(page).filter(
        language__is_main_language=True)
    locale = get_locale_code(get_language_from_request(request))

    choices = []
    for c in qs:
        translations = get_translation_for([c], locale, request.site)
        if translations:
            choices.append((translations[0].specific, c.specific))

    total_votes = sum(c.votes for c in qs)
    choice_color = ['orange', 'purple', 'turq']
    index = 0
    for choice, main_choice in choices:
        vote_percentage = 0
        if index >= len(choice_color):
            index = 0
        if main_choice.votes > 0:
            vote_percentage = int(main_choice.votes * 100.0 / total_votes)
        choice.percentage = vote_percentage
        choice.color = choice_color[index]
        index += 1

    context = {
        'question': question,
        'total': total_votes,
        'choices': sorted(
            [c for c, m in choices], key=lambda x: x.percentage, reverse=True)
    }
    return render(request, 'polls/results.html', context,)


class VoteView(FormView):
    form_class = VoteForm
    template_name = 'polls/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            VoteView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')

        question = get_object_or_404(Question, pk=question_id)
        context.update({'question': question})
        return context

    def form_valid(self, form, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        question = question.get_main_language_page().specific
        obj, created = ChoiceVote.objects.get_or_create(
            user=self.request.user,
            question=question,)

        if created:
            selected_choice = form.cleaned_data['choice']
            for choice_pk in selected_choice:
                Choice.objects.filter(
                    pk=choice_pk).update(votes=F('votes') + 1)
                choice = Choice.objects.get(pk=choice_pk)
                obj.choice.add(choice)
                choice.choice_votes.add(obj)
                choice.save()
        return HttpResponseRedirect(
            reverse('molo.polls:results', args=(question_id,)))


class FreeTextVoteView(FormView):
    template_name = 'polls/free_text_detail.html'

    def dispatch(self, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        if question.numerical:
            self.form_class = NumericalTextVoteForm
        else:
            self.form_class = TextVoteForm
        return super(FreeTextVoteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            FreeTextVoteView, self).get_context_data(*args, **kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        context.update({'question': question})
        return context

    def form_valid(self, form, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FreeTextQuestion, pk=question_id)
        question = question.get_main_language_page().specific
        FreeTextVote.objects.get_or_create(
            user=self.request.user,
            question=question,
            defaults={
                'answer': form.cleaned_data['answer']
            })
        return HttpResponseRedirect(reverse('molo.polls:results',
                                            args=(question.id,)))
