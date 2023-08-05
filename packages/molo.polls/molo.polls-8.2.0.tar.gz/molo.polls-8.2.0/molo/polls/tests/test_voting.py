from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.polls.tests.base import BasePollsTestCase
from molo.polls.models import (
    Question,
    ChoiceVote,
    FreeTextQuestion,
    FreeTextVote,
)

from molo.core.models import SiteSettings


class VotingTestCase(BasePollsTestCase):

    def test_voting_once_only(self):
        # make a question
        question = Question(title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        # make choices
        choice1 = self.make_choice(parent=question)
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')
        response = client.post(reverse('molo.polls:vote',
                               kwargs={'question_id': question.id}))
        self.assertContains(response, "select a choice")
        response = client.post(reverse('molo.polls:vote',
                               kwargs={'question_id': question.id}),
                               {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.all()[0].votes
        self.assertEquals(vote_count, 1)
        self.assertEquals(
            ChoiceVote.objects.all()[0].choice.all()[
                0].choice_votes.count(), 1)
        # vote again and test that it does not add to vote_count
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        # should automatically create the poll vote
        # test poll vote
        vote_count = ChoiceVote.objects.all()[0].choice.all()[0].votes
        self.assertEquals(vote_count, 1)
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))
        self.assertContains(response, '100%')

    def test_show_results_with_translated_choices(self):
        '''
        Test that only the translated choices are shown when
        show_only_translated_pages is true
        '''
        self.client.login(username='superuser', password='pass')
        setting = SiteSettings.objects.create(site=self.main.get_site())
        setting.show_only_translated_pages = True
        setting.save()

        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=True)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        self.client.post(reverse(
            'add_translation', args=[question.id, 'fr']))
        choice1 = self.make_choice(title='choice 1',
                                   parent=question, language=self.english)
        choice2 = self.make_choice(title='choice 2', parent=question,
                                   language=self.english)

        response = self.client.get('/')
        self.assertContains(response, question.title)
        self.assertContains(response, choice1.title)
        self.assertContains(response, choice2.title)

        self.client.post(reverse(
            'add_translation', args=[choice1.id, 'fr']))
        fr_question = Question.objects.get(
            title='French translation of is this a test')
        fr_question.save_revision().publish()
        fr_choice = choice1.translated_pages.first()
        fr_choice.save_revision().publish()
        response = self.client.get('/locale/fr/')
        response = self.client.get('/')

        # the french translation will only have the translated choice
        self.assertContains(response, fr_question.title)
        self.assertContains(response, fr_choice.title)
        self.assertNotContains(response, choice2.title)

        # vote for the translated option
        self.client.post(reverse('molo.polls:vote',
                         kwargs={'question_id': question.id}),
                         {'choice': [choice1.id, choice2.id]})
        response = self.client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))

        self.assertContains(response, fr_choice.title)
        # ensure that the untranslated choice is not displaying
        self.assertNotContains(response, choice2.title)

    def test_multiple_options(self):
        # make a question
        question = Question(
            title='is this a test',
            allow_multiple_choice=True, show_results=False)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        # make choices
        choice1 = self.make_choice(title='yes', parent=question)
        choice2 = self.make_choice(title='no', parent=question)
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': [choice1.id, choice2.id]})
        # should automatically create the poll vote
        # test poll vote
        vote_count1 = ChoiceVote.objects.all()[0].choice.all()[0].votes
        self.assertEquals(vote_count1, 1)
        vote_count2 = ChoiceVote.objects.all()[0].choice.all()[1].votes
        self.assertEquals(vote_count2, 1)
        response = client.get('/')
        self.assertContains(response, 'You voted: yes, no')

    def test_results_as_total(self):
        # make a question
        question = Question(
            title='is this a test', result_as_percentage=False)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        # make choices
        choice1 = self.make_choice(parent=question)
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})

        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))
        self.assertEquals(response.status_code, 200)
        print(response)
        self.assertContains(response, '1 vote')

    def test_show_results(self):
        # make a question
        question = Question(
            title='is this a test', show_results=False)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()
        # make choices
        choice1 = self.make_choice(parent=question)
        # make a vote
        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')
        client.post(reverse('molo.polls:vote',
                    kwargs={'question_id': question.id}),
                    {'choice': choice1.id})
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))
        self.assertContains(response, 'Thank you for voting!')
        response = client.get('/')
        self.assertContains(response, 'You voted')

    def test_free_text_vote_successful(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))

        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, 'this is an answer')
        self.assertContains(response, 'Thank you for voting!')

        response = client.get('/')
        self.assertContains(response, 'already been submitted.')

    def test_numerical_text_vote_successful(self):
        question = FreeTextQuestion(
            title='is this a test', numerical=True)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': '1234'})
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))

        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, '1234')
        self.assertContains(response, 'Thank you for voting!')

        response = client.get('/')
        self.assertContains(response, 'already been submitted.')

    def test_numerical_text_vote_unsuccessful(self):
        question = FreeTextQuestion(
            title='is this a test', numerical=True)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        response = client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': question.id}),
            {'answer': 'text answer'})
        self.assertEquals(FreeTextVote.objects.all().count(), 0)
        self.assertContains(response, 'You did not enter a numerical value')

        response = client.get('/')
        self.assertNotContains(response, 'already been submitted.')

    def test_free_text_vote_resubmission(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': 'this is an answer'})
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))
        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, 'this is an answer')

        response = client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': question.id}),
            {'answer': 'this is not an answer'})
        self.assertRedirects(response, reverse(
            'molo.polls:results', args=(question.id,)))
        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, 'this is an answer')

    def test_numerical_text_vote_resubmission(self):
        question = FreeTextQuestion(
            title='is this a test', language=self.english)
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        client.post(reverse('molo.polls:free_text_vote',
                    kwargs={'question_id': question.id}),
                    {'answer': '1234'})
        response = client.get(reverse(
            'molo.polls:results',
            kwargs={'poll_id': question.id}))
        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, '1234')

        response = client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': question.id}),
            {'answer': '2345'})
        self.assertRedirects(response, reverse(
            'molo.polls:results', args=(question.id,)))
        self.assertEquals(FreeTextVote.objects.all().count(), 1)
        self.assertEquals(
            FreeTextVote.objects.all()[0].answer, '1234')

    def test_free_text_vote_blank_answer(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        response = client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': question.id}))
        self.assertContains(response, 'field is required')
        self.assertEquals(FreeTextVote.objects.all().count(), 0)

        response = client.get('/')
        self.assertNotContains(response, 'already been submitted.')

    def test_numerical_text_vote_blank_answer(self):
        question = FreeTextQuestion(
            title='is this a test')
        self.polls_index.add_child(instance=question)
        question.save_revision().publish()

        client = Client()
        client.login(username='superuser', password='pass')
        response = client.get('/')
        self.assertContains(response, 'is this a test')

        response = client.post(reverse(
            'molo.polls:free_text_vote',
            kwargs={'question_id': question.id}))
        self.assertContains(response, 'field is required')
        self.assertEquals(FreeTextVote.objects.all().count(), 0)

        response = client.get('/')
        self.assertNotContains(response, 'already been submitted.')
