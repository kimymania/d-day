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
            delete_event()
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

    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 9, "+", "-" * 9, "+")
    print(f"| No | {'Event'.ljust(19)} | {'D-day'.ljust(9)}| {'Group'.ljust(10)}|")
    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 9, "+", "-" * 9, "+")
    for event in events:
        col1 = str(event[0]).zfill(2).ljust(3)
        col2 = event[1].ljust(20)
        col3 = calculate(event[2]).ljust(5)
        days = "days".ljust(5)
        col4 = event[3].ljust(10)
        print(f"| {col1}| {col2}| {col3}{days}| {col4}|")
    print("+", "-" * 2, "+", "-" * 19, "+", "-" * 9, "+", "-" * 9, "+")

    return events_count


def calculate(event: date) -> str:
    today = date.today()
    days_to: timedelta = today - event
    if days_to.days > 0:
        return f"+{days_to.days}"
    else:
        return f"{abs(days_to.days)}"


def add_event():
    name = input("Event name: ")
    event_date = get_date()
    group = input("Event type: ").title()
    database.add_event(name, event_date, group)


def get_date() -> date:
    while True:
        date_raw = input("Date(YYYY-MM-DD): ")
        try:
            return date.fromisoformat(date_raw)
        except ValueError as e:
            print(f"{e}: Date format should be (YYYY-MM-DD)")


def edit_event(events_count):
    while True:
        id = input("Which event would you like to edit(event number): ")
        if not id.isdigit():
            print("Type in a number")
            continue
        if int(id) > events_count:
            print("Selection out of range. Try again")
        else:
            break
    new_name = input("Enter new name (Leave empty to skip): ").strip()
    new_date = input("Enter new date (Leave empty to skip): ").strip()
    new_group = input("Enter new group tag (Leave empty to skip): ").strip()
    # skip calling database if all fields are empty
    if not new_name and not new_date and not new_group:
        return
    database.edit_event(id, new_name, new_date, new_group)


def delete_event():
    id = int(
        input("Which event would you like to delete(event number, or 0 for all): ")
    )

    database.delete_event(id)


if __name__ == "__main__":
    main()
