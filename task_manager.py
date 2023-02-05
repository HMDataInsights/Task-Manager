import os
from sys import exit
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d %b %Y"


class Task:
    def __init__(self, username=None, title=None, description=None,
                 due_date=None, assigned_date=None, completed=None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(",")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3].strip(), DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4].strip(),
                                          DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date,
                      assigned_date, completed)

    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ",".join(str_attrs)

    def display(self, task_counter):
        '''
        Display object in readable format
        '''
        disp_str = f"Task {task_counter}: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += (f"Date Assigned: \t "
                     f"{self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += (f"Due Date: \t "
                     f"{self.due_date.strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str


def login():
    """ function to allow a user login. This will Keep trying until a
    successful login and will return current user's login and password on
    sucessful login.
    """
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        # if-elif-else loop to check if inout username exists in the users
        # login data stored in username_password dictionary.
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
    return curr_user, curr_pass


def tasks():
    """function to read and parse tasks.txt and returns ""task_list" containing
    task objects.
    """
    # Create tasks.txt file if one does not exist in the directory.
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as task_file:
            pass
    # Read "tasks.txt" file contents and store each task as a seperate element
    # in "task_data" list if line is not an empty string.
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        # Create an instance of "Task" for each task in "task_data.
        curr_t = Task()
        # Convert task string in to object.
        curr_t.from_string(t_str)
        # Store task object in "task_list"
        task_list.append(curr_t)
    return task_list


def user():
    """ function to read and parse user.txt. If no user.txt file, write one
    with a default account.
    """
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as user_file:
            user_file.write("admin,password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(',')
        username_password[username] = password.strip()
    return username_password


def reg_user():
    """ Function to regiater a new user. Only an admin can register a new user.
    """
    if curr_user != 'admin':
        print("Registering new users requires admin privileges")
    else:
        # Request input of a new username
        new_username = input("New Username: ")
        # Keep on asking for a new username until input username is unique.
        while new_username in username_password.keys():
            new_username = input("Username already exists. Enter new "
                                 "Username: ")
        new_password = input("New Password: ")
        # Repeat the above steps of requesting username and password until
        # username and password pass check process carrid out by
        # "check_username_and_password" function.
        while not check_username_and_password(new_username, new_password):
            new_username = input("New Username: ")
            while new_username in username_password.keys():
                new_username = input("Username already exists. Enter new "
                                     "Username: ")
            new_password = input("New Password: ")
            continue

        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added")
            # add new username and passwords as kay and value respectively in
            # username_password dictionary.
            username_password[new_username] = new_password
            write_usernames_to_file(username_password)
        else:
            print("Passwords do no match")


def add_task():
    """ Function to add a new task.
    """
    # Request name of the person assigned to task
    task_username = input("Name of person assigned to task: ")
    # Keep on asking for a "task_username" until inout username matched with
    # one of the existing usernames.
    while True:
        if task_username not in username_password.keys():
            task_username = input("User does not exist. Please enter a "
                                  "valid username: ")
            continue
        else:
            break
    while True:
        # Request title of the task
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break
    while True:
        # Request description of the task
        task_description = input("Description of Task: ")
        # Check if the "task_description" input is safe to store.
        if validate_string(task_description):
            break
    while True:
        try:
            # Request task duie date.
            task_due_date = input("Due date of task (DD MMM YYYY): ")
            due_date_time = datetime.strptime(task_due_date,
                                              DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    # Create an instance of Task object for the new task.
    new_task = Task(task_username, task_title, task_description, due_date_time,
                    curr_date, False)
    # Append the instance of Task in "task_list".
    task_list.append(new_task)
    # Write the new task details in "tasks.txt" file.
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")


def view_all():
    """ Function to view all tasks.
    """
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")
    # Print all task_list elements with index numbers using "display()"
    # function.
    for idx, t in enumerate(task_list):
        print(t.display(idx+1))
        print("-----------------------------------")


def view_mine():
    """ Function to view the tasks assigned to user and to mark task as
    complete, modify completion date and reassign task to other user.
    """
    print("-----------------------------------")
    has_task = False
    # Print a task from the "task_list" if the task username matched with the
    # current user.
    for idx, t in enumerate(task_list):
        if t.username == curr_user:
            has_task = True
            print(t.display(idx+1))
            print("-----------------------------------")
    task_select = 0
    # Enter a task number to edit the task and -1 to go to the main menu.
    while task_select != -1:
        task_select = int(input("Enter the task number to edit (select -1 to "
                                "go to main menu):"))
        # Keep on requesting a valid task number if user enters a task number
        # for the task assigned to another user.
        while task_list[task_select-1].username != curr_user:
            if task_select != -1:
                task_select = int(input("Invalid task selection. Enter the "
                                        "task number for the task assigned to "
                                        "you to edit (select -1 to go to main "
                                        "menu):"))
            else:
                break
        if task_select == -1:
            continue
        print("Selected Task:", task_list[task_select-1].title)
        # Edit the selected task if not already completed.
        if task_list[task_select-1].completed:
            print("Task already completed and can not be edited.")
            continue
        else:
            task_complete = input("Mark task as complete (Yes/No):")
            if task_complete == "Yes":
                task_list[task_select-1].completed = "Yes"
            elif task_complete == "No":
                # Select task edit option from reassign or duedate if the task
                # is not complete.
                edit_select = input("Select Task edit option "
                                    "(reassign/duedate):")
                if edit_select == "reassign":
                    # To reassign task, request a value of the new username and
                    # update the vaue in the relevent instance of the Task.
                    # Keep on asking for a username until a username from the
                    # existing users is selected.
                    username = ""
                    while username not in username_password.keys():
                        username = input("Enter the username of the new person"
                                         " to whom the task is assigned: ")
                    task_list[task_select-1].username = username
                elif edit_select == "duedate":
                    # To edit due date, request a value of the new due date and
                    # update the vaue in the relevent instance of the Task.
                    new_due_date = input("Enter the new due date:")
                    task_list[task_select-1].due_date = datetime.strptime(
                        new_due_date, DATETIME_STRING_FORMAT)
                else:
                    print("Invalid selection. Please start again.")
                    continue
            else:
                print("Invalid selection. Please start again.")
                continue
        # Write the updated tasks info in tasks.txt file.
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully updated.")
    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")


def generate_reports():
    """Functin to generate task overview and user overview reports and write in
    txt. files.
    """
    # Create variables to store various tasks and users data.
    tasks_no = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    user_tasks = 0
    user_completed = 0
    user_overdue = 0
    # for loop to count total tasks, total completed tasks and total overdue
    # tasks.
    for t in task_list:
        tasks_no += 1
        if t.completed:
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            if t.due_date > datetime.now():
                overdue_tasks += 1
    # Write various tasks overview info from the for loop above in
    # "task_overview.txt" file.
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write("Task Overview\n"
                            "-------------\n"
                            f"{'The total number of tasks that have been generated and tracked':65}: {tasks_no}\n"
                            f"{'The total number of completed tasks':65}: {completed_tasks}\n"
                            f"{'The total number of uncompleted tasks':65}: {uncompleted_tasks}\n"
                            f"{'The total number of overdue tasks':65}: {overdue_tasks}\n"
                            f"{'The percentage of tasks that are incomplete':65}: {uncompleted_tasks/tasks_no * 100}%\n"
                            f"{'The percentage of tasks that are overdue':65}: {overdue_tasks/tasks_no * 100}%\n\n") 
    # Write various user overview info in "user_overview.txt" file.
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write("Users Overview\n"
                            "-------------\n"
                            f"{'The total number of users registered':82}: {len(username_password.keys())}\n"
                            f"{'The total number of tasks that have been generated and tracked':82}: {tasks_no}\n")
        # for loop to count tasks assigned to a user and total completed, 
        # uncomplete and overdue tasks by a user.
        for user in username_password.keys():
            for t in task_list:
                if t.username == user:
                    user_tasks += 1
                    if t.completed:
                        user_completed += 1
                    if t.due_date > datetime.now():
                        user_overdue += 1
            (user_overview.write(f"\n\n{user} Tasks Overview:\n"
                                f"{'The number of tasks assigned':82}: {user_tasks}\n"
                                f"{'The percentage of the total number of tasks assigned':82}: {round(user_tasks/tasks_no*100,0)}%\n"
                                f"{'The percentage of the tasks that have been assigned that have been completed':82}: {round(user_completed/user_tasks*100, 0)}%\n"
                                f"{'The percentage of the tasks that have been assigned that must still be completed':82}: {round((user_tasks-user_completed)/user_tasks*100, 0)}%\n"
                                f"{'The number of overdue tasks':82}: {user_overdue}"))


def validate_string(input_str):
    """ Function for ensuring that string is safe to store.
    """
    if "," in input_str:
        print("Your input cannot contain a ',' character")
        return False
    return True


def check_username_and_password(username, password):
    """ Ensures that usernames and passwords can't break the system.
    """
    if "," in username or "," in password:
        print("Username or password cannot contain ','.")
        return False
    return True


def write_usernames_to_file(username_dict):
    """Function to write username to file
    Input: dictionary of username-password key-value pairs
    """
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k},{username_dict[k]}")
        out_file.write("\n".join(user_data))


#########################
# Main Program
#########################


# load tasks list
task_list = tasks()

# Load username and password data
username_password = user()

# User login
curr_user, curr_pass = login()

while True:
    print()
    # Get input from user
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    a - Add a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    e - Exit
    : ''').lower()

    if menu == 'r':  # Register new user (if admin)
        reg_user()

    elif menu == 'a':  # Add a new task
        add_task()

    elif menu == 'va':  # View all tasks
        view_all()

    elif menu == 'vm':  # View my tasks
        view_mine()

    elif menu == 'gr':  # Generate reports
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':  # If admin, display statistics
        if not (os.path.exists("task_overview.txt") or
                os.path.exists("user_overview.txt")):
            generate_reports()
        with open("task_overview.txt") as task_overview:
            print(task_overview.read())
        with open("user_overview.txt") as user_overview:
            print(user_overview.read())

    elif menu == 'e':  # Exit program
        print('Goodbye!!!')
        exit()

    else:  # Default case
        print("You have made a wrong choice, Please Try again")
