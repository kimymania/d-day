import sqlite3

# autocommit False for manual commits and retrievals - using local cache data
cx = sqlite3.connect(
    "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
)
cu = cx.cursor()


def init_db():
    # Check if table exists - create if not
    # group is reserved - will use grp instead
    cu.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date DATE NOT NULL,
            grp TEXT NOT NULL
        )
    """)
    cx.commit()


def add_event(name: str, date, group: str):
    """
    Args:
        name (str)
        date (datetime.date())
        group (str)
    """
    try:
        cu.execute(
            "INSERT INTO events (name, date, grp) VALUES (?, ?, ?)", (name, date, group)
        )
        cx.commit()
    except sqlite3.Error as e:
        cx.rollback()
        print(f"Error writing to db: {e}")


def get_events():
    # ORDER BY date DESC
    try:
        events = cu.execute("SELECT name, date, grp FROM events")
    except sqlite3.Error as e:
        print(f"Error reading from db: {e}")
    result = events.fetchall()
    return result


def edit_event(id, name=None, date=None, grp=None):
    error = 0
    if name:
        try:
            cu.execute(
                "UPDATE events SET name = ? WHERE id = ?",
                (name, id),
            )
        except sqlite3.Error as e:
            print(f"Error updating name: {e}")
            error = 1
    if date:
        try:
            cu.execute(
                "UPDATE events SET date = ? WHERE id = ?",
                (date, id),
            )
        except sqlite3.Error as e:
            print(f"Error updating date: {e}")
            error = 1
    if grp:
        try:
            cu.execute(
                "UPDATE events SET grp = ? WHERE id = ?",
                (grp, id),
            )
        except sqlite3.Error as e:
            print(f"Error updating group tag: {e}")
            error = 1

    if not error:
        cx.commit()
    else:
        cx.rollback()


def delete_event(id):
    if id == "0":
        try:
            cu.execute("DELETE FROM events")  # remove all data
            cx.commit()
        except sqlite3.Error as e:
            print(f"Error clearing db: {e}")
            cx.rollback()
    else:
        try:
            cu.execute("DELETE FROM events WHERE id = ?", (id))
        except sqlite3.Error as e:
            print(f"Error deleting data from db: {e}")
            cx.rollback()


def close():
    cu.close()
    cx.close()
