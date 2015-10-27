Include GoTo
============

This plugin for Sublime Text 2/3 opens include files if invoked when the cursor is on a line with an
include in C/C++ files. This is based on the include paths given by -I command line arguments in
some setting (configurable). It is recommended to use this plugin in combination with Clang-Complete
or SublimeClang, though not required. If these are used, it is convenient to use their goto command
as a fallback (configurable).

Keymap:
---

By default, the keymap uses F12 and thereby overwrites the default goto definition command.


Installation:
---

Just clone this git repo into your Packages folder.
