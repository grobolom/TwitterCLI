import copy
import asyncio

class RootReducer:
    def __init__(self, middlewares=None):
        self.middlewares = []
        if middlewares:
            self.middlewares = middlewares

    def reduce(self, state, action):
        s = copy.deepcopy(state)
        s = self._callMiddlewares(s, action)

        name = action['name']
        if name == 'CURSOR_MOVE':
            return self._cursorMove(s, action)
        elif name == 'SWITCH_TAB':
            return self._switchTab(s, action)
        elif name == 'SWITCH_VIEW':
            return self._switchView(s, action)
        elif name == 'NEW_TWEETS':
            return self._addTweets(s, action)
        elif name == 'DONE_LOADING_TWEETS':
            return self._finishLoadingTweets(s, action)

        return s

    def _callMiddlewares(self, state, action):
        ns = state
        for middleware in self.middlewares:
            asyncio.async(middleware.handleAction(ns, action))
        return ns

    def _finishLoadingTweets(self, state, action):
        if state['view'] == 'splash':
            state['view'] = 'default'
        return state;

    def _switchView(self, state, action):
        state['view'] = action['target']
        return state

    def _cursorMove(self, state, action):
        """
        we use a 'fancy' method to contrain the cursor here - by taking the
        mean of the sorted [0, cursor, cursor_max] we always get the right
        amount. If cursor < 0 or cursor > cursor_max, it moves to the
        extremes of the list and thus we select the correct limit instead
        """

        amount     = action['amount']
        c_list     = state['lists'][ state['selected_list'] ]
        cursor     = c_list['cursor'] + amount
        cursor_max = c_list['cursor_max']

        state['lists'][ state['selected_list'] ]['cursor'] = \
            sorted([0, cursor, cursor_max])[1]

        return state

    def _switchTab(self, state, action):
        """
        we also use a fancy method here to find the next tab to switch to
        since we don't want to run off the end, so we stick the zero
        index onto the end and use that to roll back to the start if we
        need to
        """
        current = state['selected_list']
        lists   = self._listOrder(state)

        if current in lists:
            index      = lists.index(current)
            indices    = list(range(0, len(lists))) + [ 0 ]
            next_index = indices[ index + 1 ]

            state['selected_list'] = lists[next_index]
        else:
            state['selected_list'] = lists[0]

        return state

    def _addTweets(self, state, action):
        list_name = action['list']
        tweets = action['tweets']

        if list_name not in state['lists']:
            state['lists'][ list_name ] = {
                'tweets': [],
                'cursor': 0,
                'cursor_max': len(tweets)
            }

        current_tweets = state['lists'][ list_name ]['tweets']
        state['lists'][ list_name ]['tweets'] = \
            tweets + current_tweets

        return state

    def _listOrder(self, state):
        keys = state['lists'].keys()

        order = []
        if 'home_timeline' in keys:
            order += [ 'home_timeline' ]
        if 'tweets' in keys:
            order += [ 'tweets' ]

        other_lists = []
        for key in keys:
            if key not in other_lists and key not in order:
                other_lists += [ key ]
        return order + sorted(other_lists)

class TerminalReducer:
    """
    maybe this should be a middleware? anyway, we need to get the terminal
    size somehow
    """
    def __init__(self, terminal):
        self.terminal = terminal

    def reduce(self, state, action):
        state['screen_width'] = self.terminal.width
        state['screen_height'] = self.terminal.height
        return state
