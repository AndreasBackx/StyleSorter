import sublime
import sublime_plugin
from StyleSorter.Parser import Parser


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = sublime.load_settings('StyleSorter.sublime-settings')
		ordering = settings.get('ordering')

		self.view.set_status('StyleSorter', 'Parsing stylesheet')
		self.region = sublime.Region(0, self.view.size())
		text = self.view.substr(self.region)
		thread = Parser(text, ordering, self.updateFile)
		thread.start()

	def updateFile(self, formatted):
		pass

	def description(self):
		return 'Super CSS sorter.'
