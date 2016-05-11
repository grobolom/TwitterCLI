![TwitterCLI main screen](https://i.imgur.com/Rw9P4F7.png)

# TwitterCLI
[![codecov](https://codecov.io/gh/grobolom/TwitterCLI/branch/master/graph/badge.svg)](https://codecov.io/gh/grobolom/TwitterCLI)

an attempt to replicate Gary Bernhardt's functional twitter client in python
from memory

## Structure

Things are rendered by the Blessed library

Architecture is based on something of a react-style unidirectional flow - we
respond to keystrokes or events in a main loop, which modifies the state
and pushes it down into the lower-level components

## Design Decisions

We are caching things in files for now because it's simple and we don't want to
introduce additional dependencies like redis. If we need something more complex
we will switch ASAP
