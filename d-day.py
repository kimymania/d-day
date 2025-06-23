import sys
from datetime import date
from time import sleep

import database


def display_menu() -> int:
    print("""
    -- Main Menu --
    1. View all events
    2. Add new events
    3. Delete event
    4. Exit""")
    while True:
        select = input("Select a menu to navigate to: ")
        if select == "1":
            return 1
        elif select == "2":
            return 2
        elif select == "3":
            return 3
        elif select == "4":
            return 4
        else:
            print("Please select a menu between 1 to 4")
            continue


def view_events():
    events = database.get_events()
    index = 1  # change this index to auto-generated event key in sqlite - but can keys be modified??
    for event in events:
        print(f"{index}\t{event[0]}\t{event[1]}\t{event[2]}")
        index += 1


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


def delete_event(events):
    view_events()
    while True:
        select = int(input("Event to delete (number): "))
        if select > len(events):
            print("Not a valid number key! Try again")
        else:
            break
    return events[select]


def main():
    print("D-Day Calculator")
    database.init_db()
    events_list = []
    while True:
        menu = display_menu()
        if not events_list and (menu == 1):
            print("No upcoming events!")
            continue

        if menu == 1:
            view_events()
        elif menu == 2:
            add_event()
        elif menu == 3:
            del_event = delete_event(events_list)
            events_list.remove(del_event)
        elif menu == 4:
            print("Bye!")
            sleep(0.5)
            sys.exit()


if __name__ == "__main__":
    main()
