import sys
from datetime import date, timedelta
from time import sleep

import database


def main():
    database.init_db()
    while True:
        events_count = view_events()
        print(
            """
-- Actions --
1. Add new event
2. Edit events
3. Delete event
4. Exit"""
        )
        select = input("Select a menu to navigate to: ")
        if select == "1":
            add_event()
        elif select == "2":
            edit_event(events_count)
        elif select == "3":
            delete_event(events_count)
        elif select == "4":
            print("Bye!")
            sleep(0.5)
            sys.exit()
        else:
            print("Please choose a valid menu between 1 and 4")


def view_events():
    events = database.get_events()
    if not events:
        print("No upcoming events")
        events_count = 0
    else:
        events_count = len(events)

    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 6, "+", "-" * 9, "+")
    print(f"| No | {'Event'.ljust(19)} | {'D-day'.ljust(7)}| {'Group'.ljust(10)}|")
    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 6, "+", "-" * 9, "+")
    for event in events:
        col1 = str(event[0]).zfill(2).ljust(3)
        col2 = event[1].ljust(20)
        col3 = calculate(event[2]).ljust(7)
        col4 = event[3].ljust(10)
        print(f"| {col1}| {col2}| {col3}| {col4}|")
    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 6, "+", "-" * 9, "+")

    return events_count


def calculate(event: date) -> str:
    today = date.today()
    days_to: timedelta = today - event
    if days_to.days > 0:
        return f"D+{days_to.days}"
    elif days_to.days == 0:
        return "D-day"
    else:
        return f"D{days_to.days}"


def add_event():
    name = input("Event name: ")
    while True:
        event_date = get_date()
        if event_date:
            break
    group = input("Event type: ").title()
    database.add_event(name, event_date, group)


def get_date(string: str | None = None) -> date | None:
    """Parameter = string to display

    Returns None if enter is pressed without any input. Any other invalid inputs are rejected"""
    while True:
        date_raw = input(string if string else "Date(YYYY-MM-DD): ")
        try:
            return date.fromisoformat(date_raw)
        except ValueError as e:
            if date_raw == "":
                return None
            else:
                print(f"{e}: Date format should be (YYYY-MM-DD)")


def edit_event(events_count):
    while True:
        try:
            id = input("Which event would you like to edit(event number): ")
            id = int(id)
        except ValueError as e:
            print(f"{e}: Input has to be a number. Try again")
            continue
        if int(id) not in range(0, events_count + 1):
            print("Selection out of range. Try again")
            continue
        break
    new_name = input("Enter new name (Leave empty to skip): ").strip()
    new_date = get_date("Enter new date (Leave empty to skip): ")
    new_group = input("Enter new group tag (Leave empty to skip): ").strip()
    # skip calling database if all fields are empty
    if not new_name and not new_date and not new_group:
        return
    database.edit_event(id, new_name, new_date, new_group)


def delete_event(events_count):
    while True:
        try:
            id = input(
                "Which event would you like to delete(event number, or 0 to delete all events): "
            )
            id = int(id)
        except ValueError as e:
            print(f"{e}: Input has to be a number. Try again")
            continue
        if int(id) not in range(0, events_count + 1):
            print("Selection out of range. Try again")
            continue
        break
    database.delete_event(id)


if __name__ == "__main__":
    main()
