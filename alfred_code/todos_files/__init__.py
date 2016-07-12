# -*- coding: UTF-8 -*-
import sys
import re
import os
from datetime import datetime
import todos_helper
import files_helper
from .const_value import TIME_SPLIT, TODO_HEADER

reload(sys)
sys.setdefaultencoding('utf-8')
files_obj = None


def todo_files(arg=""):
	global files_obj
	if files_obj is None:
		files_obj = TodoFiles(arg)
	else:
		files_obj.argument = arg
	return files_obj


def get_time_now():
	return str(datetime.now()).split('.')[0]


class TodoFiles(object):

	__slots__ = ['all_todos', 'all_actions', '_argument', 'all_files']

	def __init__(self, arg):
		self.all_todos = None
		self.all_actions = None
		self._argument = arg
		self.all_files = None

	@property
	def argument(self):
		return self._argument

	@argument.setter
	def argument(self, arg):
		self._argument = arg

	@property
	def todos(self):
		if self.all_todos is None:
			self.all_todos = self.get_todos()
		return self.all_todos

	@property
	def actions(self):
		if self.all_actions is None:
			self.all_actions = todos_helper.get_todo_actions()
		return self.all_actions

	@property
	def files(self):
		if self.all_files is None:
			self.all_files = self.get_files()
		return self.all_files

	@property
	def todo_actions(self):
		return {
			'complete': files_helper.complete_todo,
			'delete': files_helper.delete_todo,
			'add': self.new_todo
		}

	def get_todos(self, complete=None):
		complete = False if complete is None else True
		all_todos = {}
		for filename in files_helper.get_all_files():
			file_todos = self.read_file(filename, complete)
			filename = filename.split('.')[0]
			icon_path = 'icons/file_{}.png'.format(filename)
			file_icon = icon_path if os.path.isfile(icon_path) else todos_helper.get_default_icon()
			all_todos[filename] = {
				'icon': file_icon,
				'todos': file_todos
			}
		return all_todos

	def get_files(self):
		all_files = {}
		for filename in files_helper.get_all_files():
			filename = filename.split('.')[0]
			icon_path = 'icons/file_{}.png'.format(filename)
			all_files[filename] = icon_path if os.path.isfile(icon_path) else todos_helper.get_default_icon()
		return all_files

	def read_file(self, filename, complete):
		items = []
		filter_function = todos_helper.filter_complete_todos if complete else todos_helper.filter_target_todo(self.argument)
		with open('todos/{}'.format(filename), 'r') as f:
			for line in filter(filter_function, f.readlines()):
				if line.strip():
					filtered_item = re.findall(r'^- ~{0,2}(.*?)~{0,2}\n$', line)[0]
					items.append(filtered_item)
		return items

	def new_todo(self, filename, todo):
		with open(files_helper.get_file_path(filename), 'a') as f:
			if todo not in self.todos[filename]['todos']:
				f.write('{todo_header}{todo}[{time_spilt}{todo_time}]\n'.format(todo_header=TODO_HEADER,
				todo=todo,
				time_spilt=TIME_SPLIT,
				todo_time=get_time_now()))
