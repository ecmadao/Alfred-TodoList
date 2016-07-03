# -*- coding: UTF-8 -*-
import os
import re
import sys
from random import randrange

reload(sys)
sys.setdefaultencoding('utf-8')

FILES= ('learn', 'work', 'life', 'others')

SPLIT = '//'

ACTIONS = ('complete', 'delete')



def get_default_icon():
	default_icons = os.listdir('icons/default')
	return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])


def get_files():
	all_files = {}
	for filename in FILES:
		icon_path = 'icons/file_{}.png'.format(filename)
		file_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
		all_files[filename] = file_icon
	return all_files
#	return {key: 'icons/file_{}.png'.format(key) for key in FILES if os.path.isfile(path)}


def get_actions():
	all_actions = {}
	for action in ACTIONS:
		icon_path = 'icons/todo_{}.png'.format(action)
		action_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
		all_actions[action] = action_icon
	return all_actions
#	return {key: 'icons/todo_{}.png'.format(key) for key in ACTIONS}


def read_files():
	all_items = {}
	files = [x for x in os.listdir('todos') if os.path.splitext(x)[1] == '.md']
	for file in files:
		all_items[file.split('.')[0]] = read_file(file)
	return all_items
	

def filter_uncomplete_todos(todo):
	re_result = re.search(r'- ~~(.*)~~', todo)
	result = False if re_result else True
	return result


def read_file(filename):
	items = []
	with open('todos/{}'.format(filename), 'r') as f:
		for line in filter(filter_uncomplete_todos, f.readlines()):
			items.append(line.split('- ')[1].strip().decode("utf-8"))
	return items


def write_todos(filename, todos):
	with open('todos/{}.md'.format(filename), 'w') as f:
		f.writelines(todos)


def new_todo(filename, todo):
	with open('todos/{}.md'.format(filename), 'a') as f:
		f.write('- {}\n'.format(todo).decode("utf-8"))


def delete_todo(filename, todo):
	with open('todos/{}.md'.format(filename), 'r') as f:
		todo_lines = [line for line in f.readlines() if line.split('- ')[1].strip() != todo]
	rename_file(filename)
	write_todos(filename, todo_lines)
	remove_file(filename)


def complete_todo(filename, todo):
	with open('todos/{}.md'.format(filename), 'r') as f:
		todo_lines = []
		for line in f.readlines():
			line_todo = line.split('- ')[1].strip()
			if line_todo == todo:
				line = '- ~~{}~~\n'.format(line_todo)
			todo_lines.append(line)
	rename_file(filename)
	write_todos(filename, todo_lines)
	remove_file(filename)


def todo_actions():
	return {
		'complete': complete_todo,
		'delete': delete_todo,
		'add': new_todo
	}
	

def rename_file(filename):
	os.rename('todos/{}.md'.format(filename), 'todos/{}_temp.md'.format(filename))


def remove_file(filename):
	os.remove('todos/{}_temp.md'.format(filename))
