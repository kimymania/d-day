import sys
from datetime import date
from time import sleep

import database


def main():
    print("D-Day Calculator")
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

    index = 1  # change this index to auto-generated event key in sqlite - but can keys be modified??
    for event in events:
        print(f"{index}\t{event[0]}\t{event[1]}\t{event[2]}")
        index += 1

    return events_count


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
    print(events_count)
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
    id = input("Which event would you like to delete(event number, or 0 for all): ")

    database.delete_event(id)


if __name__ == "__main__":
    main()
