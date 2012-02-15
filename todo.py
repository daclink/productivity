#!/usr/bin/python
from optparse import OptionParser
import sqlite3 as lite
import sys

def main():
	usage = 'Usage: %prog [option]'
	parser = OptionParser(usage)

	parser.set_defaults(asc_desc=True)
	
	parser.add_option('-t', '--todo', dest='insTodo', help='Add an item to the TODO list')
	parser.add_option('--desc', action='store_true', dest='asc_desc', help='Sort in descending order (DEFAULT)')
	parser.add_option('--asc', action='store_false', dest='asc_desc', help='Sort in ascending order.')
	parser.add_option('-f', '--find', dest='tag', help='find by tag')
	parser.add_option('--all',
						type='string',
						action='callback', 
						callback=list_todos)
	parser.add_option('--add',
						type='string',
						action='callback', 
						callback=add_todo, 
						help='Add an item to the TODO list')

	(options, args) = parser.parse_args()

	print "%i is the length of args" %len(args)

	print "Todo == %s" %options.asc_desc

#=-=-=- end parsing


#=-=-=- operations
def add_todo(option, opt, value, parser):
	userID = 1
	print "adding a todo"
	setattr(parser.values, option.dest, value)
	foo = value
	con = DB_connect().__enter__()
	cursor = con.cursor()
	s = "insert into todo(desc, created, ownerid) values ('%(todo)s',date('now'),'%(id)d')" %{"todo":value, "id":userID}
	print s
	cursor.execute(s)
	con.commit()
#	DB_connect().__exit__(con)

def list_todos(option, opt, value, parser):
	setattr(parser.values, option.dest, value)
	print "Here we go!"
	#desc = option.value.asc_desc
	desc = True
	print "option.values.asc_desc == %s" %desc
	sortDir = 'desc' if desc else 'asc'
	userID = 1
	print "listing todos"
	con = DB_connect().__enter__()
	cursor = con.cursor()
	query = "select * from todo where ownerid='%(userID)d' order by created %(sortDir)s"\
			%{"userID":userID,"sortDir":sortDir}
	print "query is %s" %query
	cursor.execute(query)

	col_names = [cn[0] for cn in cursor.description]

	rows = cursor.fetchall()

	print "%s %-10s %s %s" %(col_names[0], col_names[1], col_names[2], col_names[3])

	for row in rows:
		print "%2d %-10s %s %d" % row

#def add_todo():
	
#def del_todo():

#def list_todo_by_tag():

#def update_todo():

#=-=-=- begin DB stuff
class DB_connect:

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
