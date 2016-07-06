# -*- coding: UTF-8 -*-
import os
import re
import sys
from random import randrange
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT = '->'
TIME_SPLIT = '@'

TODO_HEADER = '- '
ARCHIVE_TITLE = 'new archive: '

files_obj = None

actions_obj = None


def todo_actions():
	global actions_obj
	if actions_obj is None:
		actions_obj = TodoActions()
	return actions_obj


def todo_files(arg):
	global files_obj
	if files_obj is None:
		files_obj = TodoFiles(arg)
	else:
		files_obj.argument = arg
	return files_obj
	

def get_file_path(filename, temp=None):
	temp = '' if temp is None else '_temp'
	return 'todos/{filename}{temp}.md'.format(filename=filename, temp=temp)
	
	
def get_default_icon():
	default_icons = os.listdir('icons/default')
	return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])
	

def get_time_now():
	return str(datetime.now()).split('.')[0]
	

def create_new_archive(filename):
	file_path = get_file_path(filename)
	if not os.path.isfile(file_path):
		with open(file_path, 'w') as f:
			pass


class TodoActions(object):
	
	ACTIONS = ('complete', 'delete')
	
	def __init__(self):
		self.all_actions = None
	
	@property
	def actions(self):
		if self.all_actions is None:
			self.all_actions = self.get_todo_actions()
		return self.all_actions
	
	@staticmethod
	def get_todo_actions():
		all_actions = {}
		for action in TodoActions.ACTIONS:
			icon_path = 'icons/todo_{}.png'.format(action)
			action_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
			all_actions[action] = action_icon
		return all_actions

	@staticmethod
	def new_todo(filename, todo):
		# TODO 提高运行效率
		with open(get_file_path(filename), 'a') as f:
			if todo not in todo_files('').files[filename]['todos']:
				f.write('{todo_header}{todo}[{time_spilt}{todo_time}]\n'.format(todo_header=TODO_HEADER, 
				todo=todo, 
				time_spilt=TIME_SPLIT,
				todo_time=get_time_now()))

	@staticmethod
	def delete_todo(filename, todo):
		with open(get_file_path(filename), 'r') as f:
			todo_lines = [line for line in f.readlines() if re.match(r'^- (.*)\n$', line) and not re.match(r'^- ~~(.*)~~\n$', line)]
		TodoActions.deal_todo_file(filename, todo_lines)

	@staticmethod
	def complete_todo(filename, todo):
		with open(get_file_path(filename), 'r') as f:
			todo_lines = []
			for line in f.readlines():
				
				line_todo = re.findall(r'^- (.*)\n$', line)[0]
				if line_todo and re.match(r'{todo}\[?@?'.format(todo=todo), line_todo):
					line = '{}~~{}~~\n'.format(TODO_HEADER, line_todo)
					todo_lines.append(line)

		TodoActions.deal_todo_file(filename, todo_lines)
	
	@staticmethod
	def deal_todo_file(filename, todo_lines):
		TodoActions.rename_file(filename)
		TodoActions.write_file(filename, todo_lines)
		TodoActions.remove_file(filename)

	@property
	def todo_actions(self):
		return {
			'complete': TodoActions.complete_todo,
			'delete': TodoActions.delete_todo,
			'add': TodoActions.new_todo
		}

	@staticmethod
	def write_file(filename, todos):
		with open(get_file_path(filename), 'w') as f:
			f.writelines(todos)
		
	@staticmethod
	def rename_file(filename):
		os.rename(get_file_path(filename), get_file_path(filename, temp=True))

	@staticmethod
	def remove_file(filename):
		os.remove(get_file_path(filename, temp=True))


class TodoFiles(object):
	
	argument = ''
	
	def __init__(self, arg):
		self.all_files = None
		TodoFiles.argument = arg
	
	@property
	def argument(self):
		return TodoFiles.argument
	
	@argument.setter
	def argument(self, arg):
		TodoFiles.argument = arg
	
	@property
	def files(self):
		if self.all_files is None:
			self.all_files = self.get_todo_files()
		return self.all_files
	
	@staticmethod
	def get_todo_files(complete=None):
		complete = False if complete is None else True
		all_files = {}
		for filename in TodoFiles.get_all_files():
			file_todos = TodoFiles.read_file(filename, complete)
			filename = filename.split('.')[0]
			icon_path = 'icons/file_{}.png'.format(filename)
			file_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
			all_files[filename] = {
				'icon': file_icon,
				'todos': file_todos
			}
		return all_files
	
	@staticmethod
	def get_all_files():
		return [x for x in os.listdir('todos') if os.path.splitext(x)[1] == '.md']
	
	@staticmethod
	def filter_complete_todos(todo):
		re_result = re.search(r'^{}~~(.*)~~\n$'.format(TODO_HEADER), todo)
		result = True if re_result else False
		return result
	
	@staticmethod
	def filter_target_todo(todo):
		target_result = re.search(r'^{todo_header}.*{argument}.*\n$'.format(todo_header=TODO_HEADER, argument=TodoFiles.argument), todo)
		complete_result = TodoFiles.filter_complete_todos(todo)
		result = True if target_result and not complete_result else False
		return result

	@staticmethod
	def read_file(filename, complete):
		items = []
		filter_function = TodoFiles.filter_complete_todos if complete else TodoFiles.filter_target_todo
		with open('todos/{}'.format(filename), 'r') as f:
			for line in filter(filter_function, f.readlines()):
				if line.strip():
					filtered_item = re.findall(r'^- ~{0,2}(.*?)~{0,2}\n$', line)[0]
					items.append(filtered_item)
		return items
