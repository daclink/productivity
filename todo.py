#!/usr/bin/python
from optparse import OptionParser
import sqlite3 as lite
import sys

def main():
	usage = "Usage: %prog [option]"
	parser = OptionParser(usage)
	parser.add_option("-t", "--todo", dest="insTodo", help="Add an item to the TODO list")
	parser.add_option("--asc", dest="sort",
					 action="store_const", const=1, help="Sort in ascending order.")
	parser.add_option("--desc", dest="sort",
					 action="store_const", const=0, help="Sort in descending order (DEFAULT)")
	parser.add_option("-f", "--find", dest="tag", help="find by tag")
	parser.add_option("-a", "--all", action="callback", callback=list_todos)

	(options, args) = parser.parse_args()

	print "%i is the length of args" %len(args)

	if options.sort:
		print "Todo == %s" %options.sort

	#=-=-=- end parsing


#=-=-=- operations
def list_todos(option, opt, value, parser):
	print "WOOOOO!"

"""
def add_todo():

def del_todo():

def list_todo_by_tag():

def update_todo():
"""
#=-=-=- begin DB stuff
class db_connect:

	def __enter__(self):
		try:
			con = lite.connect('todo.db')
			return con
		except lite.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)

	def __exit__(con):
		con.close()
"""		
with con:
			cur = con.cursor()
			cur.execute("CREATE TABLE todo(id INTEGER PRIMARY KEY, desc TEXT);")
			cur.execute("INSERT INTO todo(desc) VALUES('DBA Verification');")
"""
if __name__ == "__main__":
	main()
