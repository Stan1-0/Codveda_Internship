import os, json
from datetime import datetime

#specify file path for tasks.json
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

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
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' added successfully.")

def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    print("\nTasks:")
    for task in tasks:
        status = "Good Job, You did it" if task["completed"] else "Task is still pending"
        print(f"{task['id']}. {status} '{task['description']}'(Created: {task['created_at']})")
        
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

def main():
    tasks = load_tasks()
    while True:
        print("\nTo-Do List Application")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            description = input("Enter the task description: ")
            add_task(tasks, description)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            task_id = int(input("Enter the task ID to mark as completed: "))
            mark_task_completed(tasks, task_id)
        elif choice == "4":
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(tasks, task_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()