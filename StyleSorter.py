import sublime, sublime_plugin

class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		print(lines)


	def description(self):
		return 'Super CSS sorter.'
