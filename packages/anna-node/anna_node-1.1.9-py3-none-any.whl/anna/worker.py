import sys, traceback
from pprint import pprint

import anna.colors as colors
from anna_lib.selenium import driver
from anna_lib.task.factory import load_task


class Worker:
	def __init__(self, options):
		self.tasks = []
		self.driver = None
		self.options = options
		if self.options['resolution'] is None:
			self.options['resolution'] = (1920, 1080)
		else:
			self.options['resolution'] = tuple(int(a) for a in self.options.split('x'))

	def close(self):
		self.driver.close()

	def run(self, url, tasks):
		self.driver = driver.create(driver=self.options['driver'], headless=self.options['headless'],
		                            resolution=self.options['resolution'])
		self.driver.get(url)
		for task in tasks:
			name, task = load_task(self.driver, task)
			self.execute_task(url, name, task)
			self.tasks.append(task)
		self.print_result()

	def execute_task(self, url, name, task):
		print('Running %s @ %s on %s' % (name, url, self.driver.name))
		try:
			task.execute()
		except KeyboardInterrupt:
			return
		except:
			self.handle_exception(task)
		if task.passed:
			print(colors.green + 'passed' + colors.white)
		else:
			print(colors.red + 'failed' + colors.white)

	def print_result(self):
		if self.options['verbose']:
			self.print_task_summary()
		passed = len([task for task in self.tasks if task.passed])
		print(str(passed) + '/' + str(len(self.tasks)))

	def print_task_summary(self):
		print(colors.red)
		for task in self.tasks:
			self.print_task_result(task)
		print(colors.white)

	@staticmethod
	def print_task_result(task):
		if not task.passed:
			pprint(task.result)

	def handle_exception(self, task):
		task.passed = False
		task.result = traceback.format_exc()
		if self.options['verbose']:
			traceback.print_exc(file=sys.stdout)
