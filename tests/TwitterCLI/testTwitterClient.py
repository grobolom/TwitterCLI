import unittest
import time

from mock import MagicMock as Mock, patch
from queue import Queue
from TwitterCLI.app import TwitterClient

class TestTwitterClient(unittest.TestCase):
    def setUp(self):
        self.q = Queue()
        self.s = Mock()
        l = Mock()
        t = Mock()
        self.tc = TwitterClient(self.q, store=self.s, layout=l, terminal=t)

    def test_it_should_process_an_action_from_the_queue(self):
        self.q.put({ 'name': 'SWITCH_TAB' })
        self.tc._handleState(None)

        self.s.dispatch.assert_called_once_with({ 'name': 'SWITCH_TAB' })

    def test_it_should_prioritize_keyboard_actions(self):
        self.q.put({ 'name': 'SOMETHING' })
        self.tc._handleState('KEY_TAB')

        self.s.dispatch.assert_called_once_with({ 'name': 'SWITCH_TAB' })

    def test_it_should_not_render_when_state_is_the_same(self):
        state = {}
        actual = self.tc._handleState(None)
        self.tc.layout.render.assert_not_called()

    def test_it_should_render_the_layout(self):
        self.tc.render({ 'baconus': 'bacon' })
        self.tc.layout.render.assert_called_once_with(
            self.tc.terminal, { 'baconus': 'bacon' })

    def test_it_should_get_a_key_input(self):
        self.tc._handleKey(self.tc.terminal)
        self.tc.terminal.inkey.assert_called_once_with(timeout = 0.1)

    def test_it_should_convert_complex_key_inputs(self):
        keypress = Mock()
        keypress.is_sequence = True
        keypress.name = 'Mock Keypress'

        self.tc.terminal.inkey = Mock(return_value=keypress)
        result = self.tc._handleKey(self.tc.terminal)

        assert result == 'Mock Keypress'
