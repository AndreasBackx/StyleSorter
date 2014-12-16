import sublime
import sublime_plugin
from StyleSorter.Parser import Parser


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = sublime.load_settings('StyleSorter.sublime-settings')
		ordering = settings.get('ordering')
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parser = Parser(lines, ordering)
		parsed = parser.parse()
		formatted = parser.format(parsed)
		#print(formatted)

	def description(self):
		return 'Super CSS sorter.'
