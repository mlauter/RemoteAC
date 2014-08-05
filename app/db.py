import sqlite3
conn = sqlite3.connect('ac_states.db', check_same_thread=False)

def create_db():
	c = conn.cursor()
	c.execute('create table ac_states ( id integer primary key autoincrement, time text, temp real, is_running int)')
	conn.commit()

def add_ac_state(ac_state):
	c = conn.cursor()
	c.execute('insert into ac_states (time, temp, is_running) values ("%s",%f,%d)'%ac_state)
	conn.commit()

def get_last_ac_state():
	c = conn.cursor()
	c.execute('select * from ac_states order by id desc limit 1')
	data = c.fetchone()
	return data


try:
	create_db()
except sqlite3.OperationalError:
	pass