import sqlite3 as sqlt

db_name = 'groups_database.db'


def start_db():
    base = sqlt.connect(db_name)
    base.execute('CREATE TABLE IF NOT EXISTS "tg_group" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"group_id"            INTEGER,'
                 '"message_id"          INTEGER,'
                 '"message_chat_id"     INTEGER,'
                 '"time_interval"       INTEGER,'
                 '"next_send"           INTEGER,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.commit()


def add_pattern(data):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    group_id = int(data[3])
    message_id = 0
    message_chat_id = 0
    time_interval = data[6]
    next_send = 0
    cur.execute('INSERT INTO tg_group VALUES (null, ?, ?, ?, ?, ?)', (group_id,
                                                                      message_id,
                                                                      message_chat_id,
                                                                      time_interval,
                                                                      next_send))
    base.commit()
    base.close()


def get_my_channel():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    channels = cur.execute('SELECT * from tg_group').fetchall()
    base.close()
    return channels


def add_message_db(message_id, message_chat_id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    # cur.execute('INSERT INTO tg_group(message_id, message_chat_id) VALUES (?, ?)', [message_id, message_chat_id])
    cur.execute('UPDATE tg_group SET message_id = ? WHERE message_id = ?', (message_id, 0))
    cur.execute('UPDATE tg_group SET message_chat_id = ? WHERE message_chat_id = ?', (message_chat_id, 0))
    base.commit()
    base.close()


def update_message(id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('UPDATE tg_group SET message_id = ? WHERE id = ?', (0, id))
    cur.execute('UPDATE tg_group SET message_chat_id = ? WHERE id = ?', (0, id))
    base.commit()
    base.close()


def add_send_time(send_time, id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    # cur.execute('INSERT INTO tg_group(message_id, message_chat_id) VALUES (?, ?)', [message_id, message_chat_id])
    cur.execute('UPDATE tg_group SET next_send = ? WHERE id = ?', (send_time, id))
    base.commit()
    base.close()


def delete(id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('DELETE FROM tg_group WHERE id = ?', (id,))
    base.commit()
    base.close()


def view_all_pattern():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    all = cur.execute('SELECT id, group_id, time_interval from tg_group').fetchall()
    base.close()
    return all