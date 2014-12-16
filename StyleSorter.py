import sublime
import sublime_plugin
from StyleSorter.Parser import Parser
from time import sleep


class StyleSorterSortCommand(sublime_plugin.TextCommand):

	NAME = 'StyleSorter'

	def run(self, edit):
		settings = sublime.load_settings(self.NAME + '.sublime-settings')
		ordering = settings.get('ordering')

		self.view.set_status(self.NAME, 'Parsing stylesheet')
		region = sublime.Region(0, self.view.size())
		text = self.view.substr(region)
		thread = Parser(text, ordering)
		thread.start()
		self.handleThread(thread, edit, region)

	def handleThread(self, thread, edit, region):
		while thread.isAlive():
			sleep(0.0001)
		self.updateFile(thread.result, edit, region)

	def updateFile(self, formatted, edit, region):
		self.view.set_status(self.NAME, 'Updating stylesheet')
		self.view.replace(edit, region, formatted)
		self.view.erase_status(self.NAME)
		sublime.status_message(self.NAME + ' successfully sorted your stylesheet.')

	def description(self):
		return 'Super CSS sorter.'
