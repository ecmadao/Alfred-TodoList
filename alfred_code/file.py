# -*- coding: UTF-8 -*-
import os
import re
import sys
from random import randrange

reload(sys)
sys.setdefaultencoding('utf-8')

#FILES= ('learn', 'work', 'life', 'others')

SPLIT = '//'

#ACTIONS = ('complete', 'delete')

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
	def write_todos(filename, todos):
		with open('todos/{}.md'.format(filename), 'w') as f:
			f.writelines(todos)

	@staticmethod
	def new_todo(filename, todo):
		with open('todos/{}.md'.format(filename), 'a') as f:
			f.write('- {}\n'.format(todo))

	@staticmethod
	def delete_todo(filename, todo):
		with open('todos/{}.md'.format(filename), 'r') as f:
			todo_lines = [line for line in f.readlines() if line.split('- ')[1].strip() != todo]
		TodoActions.deal_todo_file(filename, todo_lines)

	@staticmethod
	def complete_todo(filename, todo):
		with open('todos/{}.md'.format(filename), 'r') as f:
			todo_lines = []
			for line in f.readlines():
				line_todo = line.split('- ')[1].strip()
				if line_todo == todo:
					line = '- ~~{}~~\n'.format(line_todo)
				todo_lines.append(line)
		TodoActions.deal_todo_file(filename, todo_lines)
	
	@staticmethod
	def deal_todo_file(filename, todo_lines):
		TodoActions.rename_file(filename)
		TodoActions.write_todos(filename, todo_lines)
		TodoActions.remove_file(filename)

	@staticmethod
	def todo_actions():
		return {
			'complete': TodoActions.complete_todo,
			'delete': TodoActions.delete_todo,
			'add': TodoActions.new_todo
		}
		
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
#		self.all_actions = None
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
	
#	@property
#	def actions(self):
#		if self.all_actions is None:
#			self.all_actions = self.get_todo_actions()
#		return self.all_actions
	
	@staticmethod
	def get_todo_files():
		all_files = {}
		for filename in TodoFiles.get_all_files():
			file_todos = TodoFiles.read_file(filename)
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
	
#	@staticmethod
#	def get_todo_actions():
#		all_actions = {}
#		for action in ACTIONS:
#			icon_path = 'icons/todo_{}.png'.format(action)
#			action_icon = icon_path if os.path.isfile(icon_path) else TodoFiles.get_default_icon()
#			all_actions[action] = action_icon
#		return all_actions
		
	@staticmethod
	def get_default_icon():
		default_icons = os.listdir('icons/default')
		return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])
	
	@staticmethod
	def filter_uncomplete_todos(todo):
		re_result = re.search(r'- ~~(.*)~~', todo)
		result = True if not re_result else False
		return result
	
	@staticmethod
	def filter_target_todo(todo):
		target_result = re.search(r'{}'.format(TodoFiles.argument), todo)
		uncomplete_result = TodoFiles.filter_uncomplete_todos(todo)
		result = True if target_result and uncomplete_result else False
		return result

	@staticmethod
	def read_file(filename):
		items = []
		with open('todos/{}'.format(filename), 'r') as f:
			for line in filter(TodoFiles.filter_target_todo, f.readlines()):
				if line.strip():
					items.append(line.strip().split('- ')[1])
		return items
	


#def get_default_icon():
#	default_icons = os.listdir('icons/default')
#	return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])
#
#
#def get_todo_files():
#	return [x for x in os.listdir('todos') if os.path.splitext(x)[1] == '.md']
#
#
## TODO get_files should combine with read_files
#def get_files():
#	all_files = {}
#	for filename in get_todo_files():
#		filename = filename.split('.')[0]
#		icon_path = 'icons/file_{}.png'.format(filename)
#		file_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
#		all_files[filename] = file_icon
#	return all_files
##	return {key: 'icons/file_{}.png'.format(key) for key in FILES if os.path.isfile(path)}
#
#
#def get_actions():
#	all_actions = {}
#	for action in ACTIONS:
#		icon_path = 'icons/todo_{}.png'.format(action)
#		action_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
#		all_actions[action] = action_icon
#	return all_actions
##	return {key: 'icons/todo_{}.png'.format(key) for key in ACTIONS}
#
#
#def read_files():
#	all_items = {}
#	for filename in get_todo_files():
#		all_items[filename.split('.')[0]] = read_file(filename)
#	return all_items
#	
#
#def filter_uncomplete_todos(todo):
#	re_result = re.search(r'- ~~(.*)~~', todo)
#	result = False if re_result else True
#	return result
#
#
#def read_file(filename):
#	items = []
#	with open('todos/{}'.format(filename), 'r') as f:
#		for line in filter(filter_uncomplete_todos, f.readlines()):
#			if line.strip():
#				items.append(line.strip().split('- ')[1])
#	return items
#
#
#def write_todos(filename, todos):
#	with open('todos/{}.md'.format(filename), 'w') as f:
#		f.writelines(todos)
#
#
#def new_todo(filename, todo):
#	with open('todos/{}.md'.format(filename), 'a') as f:
#		f.write('- {}\n'.format(todo))
#
#
#def delete_todo(filename, todo):
#	with open('todos/{}.md'.format(filename), 'r') as f:
#		todo_lines = [line for line in f.readlines() if line.split('- ')[1].strip() != todo]
#	rename_file(filename)
#	write_todos(filename, todo_lines)
#	remove_file(filename)
#
#
#def complete_todo(filename, todo):
#	with open('todos/{}.md'.format(filename), 'r') as f:
#		todo_lines = []
#		for line in f.readlines():
#			line_todo = line.split('- ')[1].strip()
#			if line_todo == todo:
#				line = '- ~~{}~~\n'.format(line_todo)
#			todo_lines.append(line)
#	rename_file(filename)
#	write_todos(filename, todo_lines)
#	remove_file(filename)
#
#
#def todo_actions():
#	return {
#		'complete': complete_todo,
#		'delete': delete_todo,
#		'add': new_todo
#	}
#	
#
#def rename_file(filename):
#	os.rename('todos/{}.md'.format(filename), 'todos/{}_temp.md'.format(filename))
#
#
#def remove_file(filename):
#	os.remove('todos/{}_temp.md'.format(filename))
#	
