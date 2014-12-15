import sublime
import sublime_plugin
from StyleSorter.Parser import Parser
import json


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parser = Parser(lines)
		parsed = parser.parse()
		ordered = parser.order(parsed)
		print(json.dumps(parsed, indent=4))
		print(json.dumps(ordered, indent=4))

	def description(self):
		return 'Super CSS sorter.'
