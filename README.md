dotfiles
========

Personal dotfiles - created so I can set up a new computer quickly

Geared mostly towards ubuntu or ubuntu-based systems.

###bashrc/zshrc

Both of these import `.rc_common`.

Some bits and pieces pulled from various places around the web.

###scripts

Mostly in python3.

####pythonutils

A bunch of somewhat handy little scriptlets. Including:

- autorepr: writes `__repr__` by inspecting `__init__` (`autorepr.py`)
- context managers to redirect stdout and stderr to a file or a log, or tee them (`context.py`)
- `testing.py` - various things for testing, mostly decorators. (Although the combination decorator/context manager was really fun to write. I'm not even being sarcastic)

###biologyutilis

Uh, calculates two generations of punnett squares?

###zim

These scripts help me manage my zimwiki diary.

###License

MIT License unless attributed otherwise.
