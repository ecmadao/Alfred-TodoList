"""
file helpers
"""
# -*- coding: UTF-8 -*-
import sys
import os
import re
from .const_value import TODO_HEADER

reload(sys)
sys.setdefaultencoding('utf-8')


def get_file_path(filename, temp=None):
	temp = '' if temp is None else '_temp'
	return 'todos/{filename}{temp}.md'.format(filename=filename, temp=temp)


def create_new_archive(filename):
	file_path = get_file_path(filename)
	if not os.path.isfile(file_path):
		with open(file_path, 'w') as f:
			pass


def deal_todo_file(filename, todo_lines):
	rename_file(filename)
	write_file(filename, todo_lines)
	remove_file(filename)


def write_file(filename, todos):
	with open(get_file_path(filename), 'w') as f:
		f.writelines(todos)


def rename_file(filename):
	os.rename(get_file_path(filename), get_file_path(filename, temp=True))


def remove_file(filename):
	os.remove(get_file_path(filename, temp=True))


def get_all_files():
	return [x for x in os.listdir('todos') if os.path.splitext(x)[1] == '.md']


def delete_todo(filename, todo):
	with open(get_file_path(filename), 'r') as f:
		todo_lines = [line for line in f.readlines() if re.match(r'^- (.*)\n$', line) and not re.match(r'^- ~~(.*)~~\n$', line)]
	deal_todo_file(filename, todo_lines)


def complete_todo(filename, todo):
	with open(get_file_path(filename), 'r') as f:
		todo_lines = []
		for line in f.readlines():
			line_todo = re.findall(r'^- (.*)\n$', line)[0]
			if line_todo:
				if re.match(r'{todo}\[?@?'.format(todo=todo), line_todo):
					line = '{}~~{}~~\n'.format(TODO_HEADER, line_todo)
				todo_lines.append(line)
	deal_todo_file(filename, todo_lines)
