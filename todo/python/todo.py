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
	parser.add_option('-c','--complete',
						type='string',
						action='callback',
						callback=complete_todo)
	parser.add_option('--all',
						type='string',
						action='callback', 
						callback=list_todos,
						help='list all open todos')
	parser.add_option('--add',
						type='string',
						action='callback', 
						callback=add_todo, 
						help='Add an item to the TODO list')

	(options, args) = parser.parse_args()

#=-=-=- end parsing

#=-=-=- operations
def add_todo(option, opt, value, parser):
	userID = 1
	print "adding a todo"
	setattr(parser.values, option.dest, value)
	con = DB_connect().__enter__()
	cursor = con.cursor()
	query = "INSERT INTO todo(desc, created, ownerid) "\
			"VALUES ('%(todo)s',date('now'),'%(id)d')"\
			%{"todo":value, "id":userID}
	cursor.execute(query)
	con.commit()
#	DB_connect().__exit__(con)

def complete_todo(option, opt, value, parser):
	print value
	print "that was the value"
	con = DB_connect().__enter__()
	cursor = con.cursor()
	query = "UPDATE todo "\
			"SET completed = (SELECT date('now')) "\
			"WHERE id='%(id)s'"\
			%{'id':value}
	print query
	if cursor.execute(query):
		con.commit()
	else:
		con.rollback()

def list_todos(option, opt, value, parser):
	setattr(parser.values, option.dest, value)
	#desc = option.value.asc_desc
	desc = False 
	print "option.values.asc_desc == %s" %desc
	sortDir = 'desc' if desc else 'asc'
	userID = 1
	print "listing todos"
	con = DB_connect().__enter__()
	cursor = con.cursor()
	query = "SELECT t.id, t.desc, t.created, o.uname, t.completed "\
			"FROM todo t LEFT OUTER JOIN owner o "\
			"WHERE ownerid='%(userID)d' "\
			"ORDER BY t.created, t.completed, t.id %(sortDir)s"\
			%{"userID":userID,"sortDir":sortDir}
	print "query is %s" %query
	cursor.execute(query)

	col_names = [cn[0] for cn in cursor.description]

	rows = cursor.fetchall()

	print "%s %-30s %-15s %-10s %-15s" %(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4])

	for row in rows:
		print "%2d %-30s %-15s %-10s %-15s" % row

#def add_todo():
	
#def del_todo():

#def list_todo_by_tag():

#def update_todo():

#=-=-=- begin DB stuff
class DB_connect:

	def __enter__(self):
		db = "../db/todo.db"
		try:
			con = lite.connect(db)
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
