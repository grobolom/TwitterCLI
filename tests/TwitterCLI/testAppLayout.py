from TwitterCLI.layout import AppLayout
import unittest
from mock import MagicMock as Mock

class TestAppLayout(unittest.TestCase):
    def setUp(self):
        self.screen = Mock()
        self.term = Mock()
        self.al = AppLayout(screen=self.screen)

    def test_it_should_default_to_the_main_view(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'selected_list': 'tweets',
            'lists': { 'tweets': [] },
            'view': 'random',
        }
        self.al.splashView = Mock()
        self.al.mainView   = Mock()
        self.al.render(self.term, state)

        assert self.al.mainView.call_count   == 1
        assert self.al.splashView.call_count == 0

    def test_it_should_show_the_splash_screen(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'selected_list': 'tweets',
            'lists': { 'tweets': [] },
            'view': 'splash',
        }
        self.al.splashView = Mock()
        self.al.mainView   = Mock()
        self.al.render(self.term, state)

        assert self.al.mainView.call_count   == 0
        assert self.al.splashView.call_count == 1

    def test_it_should_render_the_splash_view(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'lists': { 'tweets': [] },
            'view': 'splash',
        }
        assert len(self.al.splashView(state)) == 1

    def test_it_should_render_the_main_view(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'selected_list': 'tweets',
            'lists': {
                'tweets': {
                    'tweets': [],
                    'cursor': 0,
                    'cursor_max': 20,
                },
            },
            'view': 'splash',
        }
        assert len(self.al.mainView(state)) == 3

    def test_it_should_display_the_splash_screen_if_tweets_not_loaded(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'selected_list': '',
            'lists': {},
            'cursor': 0,
            'cursor_max': 20,
            'view': 'list',
        }
        self.al.splashView = Mock()
        self.al.mainView   = Mock()
        self.al.render(self.term, state)

        assert self.al.mainView.call_count   == 0
        assert self.al.splashView.call_count == 1

    def test_it_should_display_splash_if_selected_list_does_not_exist(self):
        state = {
            'screen_width': 40,
            'screen_height': 20,
            'selected_list': 'home_timeline',
            'lists': { 'tweets': [] },
            'cursor': 0,
            'cursor_max': 20,
            'view': 'list',
        }
        self.al.splashView = Mock()
        self.al.mainView   = Mock()
        self.al.render(self.term, state)

        assert self.al.mainView.call_count   == 0
        assert self.al.splashView.call_count == 1

