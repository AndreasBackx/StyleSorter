import sublime
import sublime_plugin
from StyleSorter.Parser import Parser


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parser = Parser(lines)
		parsed = parser.parse()
		formatted = parser.format(parsed)

	def description(self):
		return 'Super CSS sorter.'
