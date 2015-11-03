import sublime, sublime_plugin
import re, os

class include_goto(sublime_plugin.TextCommand):
    def __init__(self, arg):
        super(include_goto, self).__init__(arg)
        self.incl_regex = re.compile(r'^\s*#\s*include\s+(<|")(.*?)(>|")$')

    def is_source_file(self, name):
        return name.endswith(".c") or name.endswith(".cpp") or name.endswith(".cxx") or \
               name.endswith(".cc") or name.endswith(".S")

    def is_include_file(self, name):
        return name.endswith(".h") or name.endswith(".hpp") or name.endswith(".hh") or \
               name.endswith(".hxx")

    def get_include_paths(self, view):
        settings = sublime.load_settings("IncludeGoTo.sublime-settings")
        options = settings.get("include_options", [])
        paths = []
        for o in options:
            paths += self.get_include_paths_in(view.settings().get(o))
        return paths

    def get_include_paths_in(self, options):
        res = []
        if options:
            for opt in options:
                if opt[0:2] == "-I":
                    res.append(opt[2:])
        return res

    def goto_include(self):
        if self.is_source_file(self.view.file_name()) or self.is_include_file(self.view.file_name()):
            line = self.view.line(self.view.sel()[0])
            linetext = self.view.substr(line)
            res = self.incl_regex.match(linetext)
            if res:
                paths = self.get_include_paths(self.view)
                for p in paths:
                    abs = os.path.join(p, res.group(2))
                    if os.path.isfile(abs):
                        sublime.active_window().open_file(abs, 0)
                        return True
        return False

    # note the underscore
    def run_(self, id, args):
        # if this is called due a mouse event, put the cursor to the mouse position
        if args != None and 'event' in args:
            self.view.run_command("drag_select", args)

        if self.goto_include() == False:
            settings = sublime.load_settings("IncludeGoTo.sublime-settings")
            fallback = settings.get("fallback_command", "")
            if fallback != "":
                self.view.run_command(fallback, args)
