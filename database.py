import sqlite3

cx = sqlite3.connect("events.db")
cu = cx.cursor()


def init_db():
    pass


def close():
    cu.close()
