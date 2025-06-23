import sqlite3

# autocommit False for manual commits and retrievals - using local cache data
cx = sqlite3.connect("events.db", detect_types=sqlite3.PARSE_DECLTYPES)
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
        print(f"Error! {e}")
        raise


def get_events():
    events = cu.execute("SELECT name, date, grp FROM events ORDER BY date DESC")
    result = events.fetchall()
    return result


def close():
    cu.close()
    cx.close()
