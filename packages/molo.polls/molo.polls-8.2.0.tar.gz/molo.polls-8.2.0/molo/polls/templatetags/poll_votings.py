
from copy import copy

from django import template

from molo.polls.models import Question, Choice, PollsIndexPage

from molo.core.templatetags.core_tags import get_pages

register = template.Library()


@register.inclusion_tag('polls/poll_page.html',
                        takes_context=True)
def poll_page(context, pk=None):
    context = copy(context)
    locale_code = context.get('locale_code')
    main = context['request'].site.root_page
    page = PollsIndexPage.objects.child_of(main).live().first()
    if page:
        questions = (
            Question.objects.child_of(page).filter(
                language__is_main_language=True).specific())
    else:
        questions = Question.objects.none()

    context.update({
        'questions': get_pages(context, questions, locale_code)
    })
    return context


@register.assignment_tag(takes_context=True)
def load_polls(context):
    context = copy(context)
    locale_code = context.get('locale_code')
    main = context['request'].site.root_page
    page = PollsIndexPage.objects.child_of(main).live().first()

    if page:
        questions = (
            Question.objects.child_of(page).filter(
                language__is_main_language=True).specific())
    else:
        questions = Question.objects.none()
    return get_pages(context, questions, locale_code)


@register.inclusion_tag('polls/poll_page_in_section.html',
                        takes_context=True)
def poll_page_in_section(context, pk=None, page=None):
    context = copy(context)
    locale_code = context.get('locale_code')
    if page:
        questions = (
            Question.objects.child_of(page).filter(
                language__is_main_language=True).specific())
    else:
        questions = Question.objects.none()

    context.update({
        'questions': get_pages(context, questions, locale_code)
    })
    return context


@register.assignment_tag(takes_context=True)
def load_choices_for_poll_page(context, question):
    page = question.get_main_language_page()
    locale = context.get('locale_code')
    qs = Choice.objects.child_of(page).filter(
        language__is_main_language=True)

    if not locale:
        return qs

    return get_pages(context, qs, locale)


@register.assignment_tag(takes_context=True)
def has_questions(context, page):
    return Question.objects.live().child_of(page).exists()


@register.assignment_tag(takes_context=True)
def can_vote(context, question):
    request = context['request']
    if hasattr(question, 'freetextquestion'):
        return question.freetextquestion.can_vote(request.user)
    return question.can_vote(request.user)


@register.assignment_tag(takes_context=True)
def user_choice(context, question):
    request = context['request']
    choices = question.get_main_language_page().specific.user_choice(
        request.user)
    if choices.all().count() == 1:
        return choices.first().title
    else:
        choice_titles = [c.title for c in choices.all()]

        return ", ".join(choice_titles)
