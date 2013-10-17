import sublime, sublime_plugin

SETTING_FILE_NAME = "SimpleMarker.sublime-settings"

class SimpleMarkerSetting:
    def load_markers(self):
        settings = self.load_settings()
        markers = settings.get('markers')
        if markers == None:
            markers = []
        return markers

    def save_markers(self, markers):
        self.load_settings().set('markers', markers)
        self.save_settings()

    def load_settings(self):
        return sublime.load_settings(SETTING_FILE_NAME)

    def save_settings(self):
        sublime.save_settings(SETTING_FILE_NAME)

class SimpleMarkerListener(sublime_plugin.EventListener, SimpleMarkerSetting):
    def __init__(self):
        self.refresh(sublime.active_window().active_view())

    def on_load(self, view):
        self.refresh(view)

    def on_activated(self, view):
        self.refresh(view)

    def on_modified(self, view):
        self.refresh(view)

    def refresh(self, view):
        markers = self.load_markers()
        regions = []
        for marker in markers:
            regions += view.find_all(marker)

        view.add_regions("SimpleMarker", regions, "mark", "dot", sublime.DRAW_EMPTY)

class SimpleMarkerCommand(sublime_plugin.TextCommand, SimpleMarkerSetting):
    def run(self, edit, mode):
        self.window = self.view.window()

        if mode == "add":
            self.add()
        elif mode == "list":
            self.list()

    def add(self):
        self.new_marker()

    def add_marker(self, text):
        markers = self.load_markers()
        markers.insert(0, text)
        self.save_markers(list(set(markers)))
        self.list()

    def new_marker(self):
        initial_text = self.view.substr(self.view.sel()[0]).strip()
        self.window.show_input_panel('New marker', initial_text, self.add_marker, None, None)

    def list(self):
        markers = self.load_markers()

        def on_done(index):
            if index == 0:
                self.new_marker()
            elif index >= 1:
                self.actions(markers[index - 1])

        items = ["+ New"] + markers

        sublime.set_timeout(lambda: self.window.show_quick_panel(items, on_done), 0)

    def actions(self, item):
        def on_done(index):
            if index == 0:
                self.list()
            elif index == 1:
                markers = self.load_markers()
                markers.remove(item)
                self.save_markers(markers)
                self.list()

        items = ['< Back', '- Delete (%s)' % item]
        sublime.set_timeout(lambda: self.window.show_quick_panel(items, on_done), 0)
