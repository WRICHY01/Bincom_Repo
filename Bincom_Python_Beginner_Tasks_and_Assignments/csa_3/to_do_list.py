import psycopg2

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="my_secret_password",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

def view_tasks(task_rows):
    for i, task_row in enumerate(task_rows):
        print(f"task {i + 1}.: {task_row}")
        print("*" * 100)

while True:
    cursor.execute("SELECT * FROM todo_list;")
    task_rows = cursor.fetchall()

    print("1. add tasks") # CREATE
    print("2. view tasks") # READ
    print("3. edit tasks") # UPDATE
    print("4. remove tasks") # DELETE
    print("5. exit/end")
    
    action = input("What action would you like to perform?: ")
    

    if action == '1':
        print("\n\nADD TASK TAB...")
        print("*" * 100)
        print("when done with adding tasks, input the keyword 'done' to exit and go to the main menu ")
        while True:
            task_name = input("what would you like to add: ").lower()
            if task_name == "done":
                break
            elif task_name == "view_tasks":
                cursor.execute("SELECT * FROM todo_list;")
                task_rows = cursor.fetchall()
                view_tasks(task_rows)
            else:
                print("*" * 100)
                print(f"Checking to see if {task_name} exist in the Database...")
                cursor.execute("SELECT * FROM todo_list WHERE task ILIKE %s", (task_name,))
                if cursor.rowcount > 0:
                    print("*" * 100)
                    print(f"task: '{task_name}' already exist, you can input 'view_tasks' to view list of available tasks.")
                    print("*" * 100)
                else:
                    print("*" * 100)
                    cursor.execute("INSERT INTO todo_list(task) VALUES (%s);", (task_name,))
                    print(f"Adding {task_name} to the to do list...")
                    connection.commit()
                    print(f"Successfully added task: {task_name}")
                    print("*" * 100)

    
    elif action == '2':
        # print("*" * 100)
        print("\n\nVIEW TASKS TAB...")
        print("*" * 100)
        if not task_rows:
            print(task_rows)
            print("*" * 100)
            print("No task present yet!")
            print("*" * 100)
        else:
            view_tasks(task_rows)


    elif action == '3':
        print("\n\nRENAME TAB...")
        print("*" * 100)
        print("You can rename a task, if action is successful the task will not longer be known by its 'old name' but its 'new name' it was recently renamed as")
        print("CAUTION: The action made in this tab is PERMANENT!")
        
        print("1. update a task as 'completed'")
        print("2. rename a task")

        update_action = input("What update action would you like to do?: ")
        if update_action == '1':
            task_name = input("which task would you want to mark as 'completed': ")
            if len(task_name) < 1:
                print("It appears you havent inputted any value, You can input 'view_tasks' to view list of available tasks.")
            elif task_name == "view_tasks":
                view_tasks(task_rows)
            elif task_name == "done":
                break
            else:
                print(f"Checking to see if '{task_name}' is in the Database...")
                cursor.execute("SELECT * FROM todo_list WHERE task = %s", (task_name,))
                print(f"Found '{cursor.rowcount}' occurence of '{task_name}'")
                if cursor.rowcount < 1:
                    print(f"The task: '{task_name}' doesnt exist! You can input 'view_tasks' to view list of available tasks.")
                else:
                    cursor.execute("SELECT is_completed FROM todo_list WHERE task = %s", (task_name,))
                    cursor.execute("UPDATE todo_list SET is_completed = %s WHERE task = %s", (True, task_name))
                    print("Marking {task_name} as completed")
                    print("cursor entails: ", dir(cursor))
                    print("cursor.description entails: ", cursor.description)
                    print("cursor.statusmessage entails: ", cursor.statusmessage)
                    print("cursor.name entails: ", cursor.name)
                    print("cursor.pgresult_ptr entails: ", cursor.pgresult_ptr)
                    print("cursor.query entails: ", cursor.query)
                    print("cursor.row_factory entails: ", cursor.row_factory)
                    connection.commit()
                    print(f"'{task_name}' marked as Completed!")
                    print(f"Good job! on completing '{task_name}', Keep that Fire Burninig!")


        elif update_action == '2':
            is_old_name_empty = True

            while is_old_name_empty:
                old_name = input("what task would you like to edit/rename: ")

                if len(old_name) < 1:
                    print("It appears you havent inputted any value, You can input 'view_tasks' to view list of available tasks.")

                elif old_name == "view_tasks":
                    view_tasks(task_rows)

                elif old_name == "done":
                    break

                else:
                    print(f"Checking to see if '{old_name}' is in Database...")
                    cursor.execute("SELECT * FROM todo_list WHERE task ILIKE %s;", (old_name, ))
                    print(f"Found '{cursor.rowcount}' occurence of '{old_name}'")
                    if cursor.rowcount < 1:
                        print(f"The task: '{old_name}' doesnt exist! You can input 'view_tasks' to view list of available tasks.")
                    else:
                        is_old_name_empty = False
            
            is_new_name_empty = True
            while is_new_name_empty:
                new_name = input("what would you like to edit/rename it as: ")
                if new_name == "view_tasks":
                    view_tasks(task_rows)
                elif new_name == "done":
                    confirmation = input(f"are you sure you no longer want to rename '{old_name}': SELECT 'yes' to cancel or 'no' to rename: ")
                    if confirmation == "yes":
                        print(f"renaming of '{old_name}' has been cancelled")
                        break
                elif len(new_name) < 1:
                    print(f"You need to input the new name you want '{old_name}' to be renamed as.")
                else:
                    is_new_name_empty = False

            if cursor.rowcount > 0:
                while True:
                    confirmation = input(f"are you sure you want to rename '{old_name}' to '{new_name}': ").lower()
                    if confirmation == "yes":
                        cursor.execute("UPDATE todo_list SET task = %s WHERE task = %s;", (new_name, old_name))
                        print(f"Successfully renamed the task: '{old_name}' to '{new_name}'")
                        connection.commit()
                        print("*" * 100)
                        break
                    elif confirmation == "no":
                        print("*" * 100)
                        print(f"renaming of '{old_name}' has been cancelled.")
                        print("*" * 100)
                        break
                    else:
                        print("*" * 100)
                        print("Wrong input, you can either choose 'Yes' or 'No'.")
                        print("*" * 100)

        else:
            print("*" * 100)
            print("Wrong Input! You can only select either 1 or 2")
            print("*" * 100)



    elif action == '4':
        print("\n\nDELETE TAB...")
        print("*" * 100)
        print("You can either clear a particular task by inputting the specific task or clear all task by using the special keyword: 'delete all tasks'")
        print("CAUTION: The action made in this tab is PERMANENT!")
        task = input("what task would you like to delete: ").lower()
        
        if task == "view_tasks":
            view_tasks(task_rows)
        elif task == "delete all tasks":
            while True:
                confirmation = input("CAUTION: This will clear all task that has been set, are you sure you want perform this action: ").lower()
                if confirmation == "yes":
                    cursor.execute("DELETE from todo_list;")
                    print("*" * 100)
                    print("Standby! Clearing all tasks..")
                    connection.commit()
                    print("All tasks successfully cleared!")
                    print("*" * 100)
                    break
                elif confirmation == "no":
                    print("*" * 100)
                    print(f"action: '{action}' has been cancelled!")
                    print("*" * 100)
                    break
                else:
                    print("*" * 100)
                    print("Wrong input, you can either choose 'Yes' or 'No'.")
                    print("*" * 100) 
        else:
            if not task_rows:
                print("*" * 100)
                print("NO TASK PRESENT: cant delete an item from an empty list")
                print("*" * 100)
            else:
                # Check if the inputted value is in the Database before taking DELETE action
                cursor.execute("SELECT * FROM todo_list WHERE task ILIKE %s", (task,))
                print(f"Checking to see if '{task}' is in Database...")
                print(f"Found '{cursor.rowcount}' occurence of '{task}'")
                if cursor.rowcount > 0:
                    while True:
                        # DELETE action confirmation before finally deleting task
                        confirmation = input(f"are you sure you want to delete {task}: ").lower()
                        if confirmation == "yes":
                            cursor.execute("DELETE FROM todo_list WHERE task = %s;", (task,))
                            print(f"Successfully deleted task: '{task}'")
                            connection.commit()
                            print("*" * 100)
                            break
                        elif confirmation == "no":
                            print(f"Deleting of '{task}' has been cancelled!")
                            break
                        else:
                            print("*" * 100)
                            print("Wrong input, you can either choose 'Yes' or 'No'.")
                            print("*" * 100)
                        
                else:
                    print("*" * 100)
                    print(f"The task: '{task}' doesnt exist, you can input 'view_tasks' to view list of available tasks.")
                    print("*" * 100)


    elif action == '5':
        print("*" * 100)
        print("\nGoodbye\n")
        print("*" * 100)
        break


    else:
        print("*" * 100)
        print("\nSorry! Invalid input\n")
        print("*" * 100)