# -*- coding: UTF-8 -*-
import os
import re
import sys
from random import randrange

reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT = '->'

TODO_HEADER = '- '

files_obj = None

actions_obj = None

#ACTIONS = ('complete', 'delete')


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
			action_icon = icon_path if os.path.isfile(icon_path) else TodoActions.get_default_icon()
			all_actions[action] = action_icon
		return all_actions
	
	@staticmethod
	def get_default_icon():
		default_icons = os.listdir('icons/default')
		return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])

	@staticmethod
	def new_todo(filename, todo):
		# TODO 提高运行效率
		with open('todos/{}.md'.format(filename), 'a') as f:
			if todo not in todo_files('').files[filename]['todos']:
				f.write('{}{}\n'.format(TODO_HEADER, todo))

	@staticmethod
	def delete_todo(filename, todo):
		with open('todos/{}.md'.format(filename), 'r') as f:
			todo_lines = [line for line in f.readlines() if re.match(r'{}'.format(TODO_HEADER), line) and line.split(TODO_HEADER)[1].strip() != todo]
		TodoActions.deal_todo_file(filename, todo_lines)

	@staticmethod
	def complete_todo(filename, todo):
		with open('todos/{}.md'.format(filename), 'r') as f:
			todo_lines = []
			for line in f.readlines():
				if re.match(r'{}'.format(TODO_HEADER), line):
					line_todo = line.split(TODO_HEADER)[1].strip()
					if line_todo == todo:
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
		with open('todos/{}.md'.format(filename), 'w') as f:
			f.writelines(todos)
		
	@staticmethod
	def rename_file(filename):
		os.rename('todos/{}.md'.format(filename), 'todos/{}_temp.md'.format(filename))

	@staticmethod
	def remove_file(filename):
		os.remove('todos/{}_temp.md'.format(filename))


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
			file_icon = icon_path if os.path.isfile(icon_path) else TodoFiles.get_default_icon()
			all_files[filename] = {
				'icon': file_icon,
				'todos': file_todos
			}
		return all_files
	
	@staticmethod
	def get_all_files():
		return [x for x in os.listdir('todos') if os.path.splitext(x)[1] == '.md']
		
	@staticmethod
	def get_default_icon():
		default_icons = os.listdir('icons/default')
		return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])
	
	@staticmethod
	def filter_complete_todos(todo):
		re_result = re.search(r'{}~~(.*)~~'.format(TODO_HEADER), todo)
		result = True if re_result else False
		return result
	
	@staticmethod
	def filter_target_todo(todo):
		target_result = re.search(r'{}'.format(TodoFiles.argument), todo)
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
					items.append(line.strip().split(TODO_HEADER)[1])
		return items
