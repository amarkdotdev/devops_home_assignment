import sys
from home_assignment import grant_permission, get_items_by_year

def main():
    if len(sys.argv) < 2:
        print("Please provide a command: grant_permission OR get_items_by_year")
        return

    command = sys.argv[1]

    if command == "grant_permission":
        if len(sys.argv) != 5:
            print("Usage: grant_permission <username> <group_or_project> <role>")
            return
        username = sys.argv[2]
        target = sys.argv[3]
        role = sys.argv[4]
        result = grant_permission(username, target, role)
        print(result)

    elif command == "get_items_by_year":
        if len(sys.argv) != 4:
            print("Usage: get_items_by_year <issues|mr> <year>")
            return
        item_type = sys.argv[2]
        year = int(sys.argv[3])
        items = get_items_by_year(item_type, year)
        print(f"Returned {len(items)} {item_type}")
        for i in items:
            print(f"#{i['id']}: {i['title']} (created at {i['created_at']})")

    else:
        print(f"Unknown command '{command}'")

if __name__ == "__main__":
    main()
