import sqlite3
conn = sqlite3.connect('ac_states.db', check_same_thread=False)

def create_db():
	c = conn.cursor()
	c.execute('create table ac_states ( id integer primary key autoincrement, time text, room_temp real, is_running int, state_num int, goal_temp text)')
	conn.commit()

def add_ac_state(ac_state):
	c = conn.cursor()
	# change to ? format or named format
	c.execute('insert into ac_states (time, room_temp, is_running, state_num, goal_temp) values ("%s",%f,%d,%d,"%s")'%ac_state)
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