# Creating Database

from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Creating the table interface class

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime


Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)  # Create the above table in DB

# Accessing the database


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


from datetime import datetime, timedelta


def addNewTask():
    print("Enter task\n")
    new_task = input()
    print("Enter deadline\n")
    new_task_deadline_str = input()
    new_task_deadline = datetime.strptime(new_task_deadline_str, "%Y-%m-%d")
    new_row = TaskTable(task=new_task, deadline=new_task_deadline.date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def print_all_tasks():
    table_data = session.query(TaskTable.task, TaskTable.deadline).order_by(TaskTable.deadline).all()
    tasks_count = 1
    if len(table_data) != 0:
        tasks_list = []
        for task, deadline in table_data:
            print(f"{tasks_count}. {task}. {deadline.day} {deadline.strftime('%b')}")
            tasks_count += 1
            tasks_list.append(task)
        return True, tasks_list
    return False


def display_all_tasks():
    print("All tasks:\n")
    if not print_all_tasks():
        print("Nothing to do!\n")


def sayGoodBye():
    print("Bye!")


def display_one_day_tasks(datetime_obj):
    days_table = session.query(TaskTable.task).filter(TaskTable.deadline == datetime_obj.date()).all()
    print(f"{datetime_obj.day} {datetime_obj.strftime('%b')}:")
    tasks_count = 1
    if len(days_table) != 0:
        for a_task in days_table:
            print(f"{tasks_count}. {a_task}")
            tasks_count += 1
    else:
        print("Nothing to do!")


int_weekday_to_string = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }


def str_week_day(int_weekday):
    return int_weekday_to_string[int_weekday]


def weekTasks():
    today = datetime.today()
    eighth_day = today + timedelta(days=8)
    while today < eighth_day:
        print(f"{str_week_day(today.weekday())} ", end='')
        display_one_day_tasks(today)
        today += timedelta(days=1)
        print()


def print_missed_tasks():
    print("Missed tasks:")
    todays_date = datetime.today().date()
    data_row = session.query(TaskTable.task, TaskTable.deadline).filter(TaskTable.deadline < todays_date).all()
    if data_row is not None:
        task_count = 1
        for a_task, deadline in data_row:
            print(f"{task_count}. {a_task}. {deadline.day} {deadline.strftime('%b')}")
            task_count += 1
    else:
        print("Nothing is missed!")


def delete_task():
    print("Choose the number of the task you want to delete:\n")
    results = print_all_tasks()
    if not results:
        print("Nothing to delete")
        return
    to_delete_index = int(input()) - 1  # Referring to the index position to delete
    session.query(TaskTable).filter(TaskTable.task == results[1][to_delete_index]).delete()
    session.commit()
    print("The task has been deleted!")


while True:
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    userInput = int(input())
    if userInput == 0:
        print()
        sayGoodBye()
        break
    elif userInput == 1:
        print()
        print("Today ", end='')
        today = datetime.today()
        display_one_day_tasks(today)
    elif userInput == 2:
        print()
        weekTasks()
    elif userInput == 3:
        print()
        display_all_tasks()
    elif userInput == 4:
        print()
        print_missed_tasks()
    elif userInput == 5:
        print()
        addNewTask()
    elif userInput == 6:
        print()
        delete_task()
