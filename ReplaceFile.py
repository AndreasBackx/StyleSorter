import sublime
import sublime_plugin


class ReplaceFileCommand(sublime_plugin.TextCommand):

	KEY_TEXT = 'text'

	def run(self, edit, **kwargs):
		if self.KEY_TEXT in kwargs:
			self.view.replace(edit, sublime.Region(0, self.view.size()), kwargs[self.KEY_TEXT])
			self.view.sel().clear()
