import sqlite3


def init_db():
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
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
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
        try:
            cu.execute(
                "INSERT INTO events (name, date, grp) VALUES (?, ?, ?)",
                (name, date, group),
            )
            cx.commit()
        except sqlite3.Error as e:
            cx.rollback()
            print(f"Error writing to db: {e}")


def get_events():
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
        try:
            events = cu.execute(
                "SELECT id, name, date, grp FROM events ORDER BY date ASC"
            )
        except sqlite3.Error as e:
            print(f"Error reading from db: {e}")
        result = events.fetchall()
        return result


def edit_event(id, name=None, date=None, grp=None):
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if date:
            updates.append("date = ?")
            params.append(date)
        if grp:
            updates.append("grp = ?")
            params.append(grp)
        if not updates:
            return

        query = f"UPDATE events SET {', '.join(updates)} WHERE id = ?"
        params.append(id)
        try:
            cu.execute(query, tuple(params))
            cx.commit()
        except sqlite3.Error as e:
            print(f"Error updating group tag: {e}")
            cx.rollback()


def delete_event(id):
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
        if id == 0:
            try:
                cu.execute("DELETE FROM events")  # remove all data
                cx.commit()
            except sqlite3.Error as e:
                print(f"Error clearing db: {e}")
                cx.rollback()
        else:
            try:
                cu.execute("DELETE FROM events WHERE id = ?", (id,))
                cx.commit()
            except sqlite3.Error as e:
                print(f"Error deleting data from db: {e}")
                cx.rollback()


def close():
    with sqlite3.connect(
        "events.db", detect_types=sqlite3.PARSE_DECLTYPES, autocommit=False
    ) as cx:
        cu = cx.cursor()
        cu.close()
        cx.close()
