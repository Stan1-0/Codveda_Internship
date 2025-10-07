import os, json
from datetime import datetime

#specify file path for tasks.json
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

# priority handling dictionary
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

def normalize_priority(priority_str):
    if not isinstance(priority_str, str):
        return "medium"
    value = priority_str.strip().lower()
    if value in PRIORITY_ORDER:
        return value
    if value in ("h", "hi", "high priority"):
        return "high"
    if value in ("m", "med", "medium priority"):
        return "medium"
    if value in ("l", "lo", "low priority"):
        return "low"
    return "medium"

#load tasks from file or return empty list if file doesn't exist
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print("Sorryy!, Couldn't load tasks. Starting with empty list.")
        return []
    except Exception as e:
        print(f"Sorryy!, Couldn't load tasks. {e}")
        return []

#save tasks to file
def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"Sorryy!, Couldn't save tasks. {e}")

#add a new task
def add_task(tasks, description):
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "priority": "medium"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' added successfully.")

def view_tasks(tasks, status_filter="all"):
    if not tasks:
        print("No tasks found.")
        return
    allowed = {"pending", "done", "all"}
    status = status_filter.strip().lower()
    if status not in allowed:
        status = "all"
    if status == "pending":
        filtered = [t for t in tasks if not t.get("completed", False)]
    elif status == "done":
        filtered = [t for t in tasks if t.get("completed", False)]
    else:
        filtered = list(tasks)

    # ensure missing priority defaults to medium for old entries
    for t in filtered:
        if "priority" not in t or t["priority"] not in PRIORITY_ORDER:
            t["priority"] = "medium"

    # sort by priority (high -> low), then by created_at ascending
    def sort_key(t):
        return (
            PRIORITY_ORDER.get(t.get("priority", "medium"), PRIORITY_ORDER["medium"]),
            t.get("created_at", "")
        )

    filtered.sort(key=sort_key)

    if not filtered:
        print("No tasks match the selected filter.")
        return

    print("\nTasks:")
    for task in filtered:
        status_text = "Good Job, You did it" if task.get("completed", False) else "Task is still pending"
        priority_text = task.get("priority", "medium")
        print(f"{task['id']}. [{priority_text}] {status_text} '{task['description']}' (Created: {task['created_at']})")
        
def mark_task_completed(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} '{task['description']}' marked as completed.")
            return
    print(f"Task {task_id} not found.")

def delete_task(tasks, task_id):
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

def edit_task_description(tasks, task_id, new_description):
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            save_tasks(tasks)
            print(f"Task {task_id} renamed to '{new_description}'.")
            return
    print(f"Task {task_id} not found.")

def main():
    tasks = load_tasks()
    while True:
        print("\nTo-Do List Application")
        print("1. Add a new task")
        print("2. View tasks (with filter)")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Edit a task description")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            description = input("Enter the task description: ")
            priority_input = input("Enter priority (high|medium|low) [default: medium]: ")
            priority_value = normalize_priority(priority_input)
            # add with description first, then set priority to ensure backward compatibility
            add_task(tasks, description)
            tasks[-1]["priority"] = priority_value
            save_tasks(tasks)
        elif choice == "2":
            status_filter = input("Filter by --status pending|done|all [default: all]: ")
            view_tasks(tasks, status_filter or "all")
        elif choice == "3":
            task_id = int(input("Enter the task ID to mark as completed: "))
            mark_task_completed(tasks, task_id)
        elif choice == "4":
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(tasks, task_id)
        elif choice == "5":
            task_id = int(input("Enter the task ID to edit: "))
            new_description = input("Enter the new description: ")
            edit_task_description(tasks, task_id, new_description)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()