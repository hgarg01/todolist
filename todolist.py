# Write your code here

from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
import datetime

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.datetime.today())

    def __repr__(self):
        return self.task

#create table in database
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def printrows(rows,msg):
    if not rows:
            print("\nNothing to do!")
    else:
            print("\n{} tasks:".format(msg))
            i = 1
            for r in rows:
                print(str(i) + ". " + r.task + ". " + r.deadline.strftime("%#d %b"))
                i += 1

answer = 1
while answer != 0:
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    answer = int(input())

    if answer == 1:
        today = datetime.datetime.today()
        print("\nToday {} {}".format(str(today.day), today.strftime('%b')))
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print("Nothing to do!")
        else:
            i = 1
            for r in rows:
                print(str(i)+". "+r.task)
                i += 1

    elif answer == 2:
        day = datetime.datetime.today()
        for _i in range(7):
            print("\n{} {} {}".format(day.strftime('%A'), str(day.day), day.strftime('%b')))
            rows = session.query(Table).filter(Table.deadline == day.date()).all()
            if not rows:
                print("Nothing to do!")
            else:
                i = 1
                for r in rows:
                    print(str(i)+". "+r.task)
                    i += 1
            day += datetime.timedelta(days = 1)

    elif answer == 3:
        rows = session.query(Table).order_by(Table.deadline).all()
        printrows(rows, "All")


    elif answer == 4:
        rows = session.query(Table).filter(Table.deadline < datetime.datetime.today().date()).all()
        if not rows:
            print("Missed taks:\nNothing is missed")
        else:
            printrows(rows, "Missed")

    elif answer == 5:
        t = input("\nEnter task\n")
        d = datetime.datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
        new_row = Table(task=t, deadline = d)
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    elif answer == 6:
        rows = session.query(Table).order_by(Table.deadline).all()
        printrows(rows, "All")
        if not rows:
            print("\nNothing to delete!")
        else:
            print("Choose the number of the task you want to delete:")
            i = 1
            for r in rows:
                print(str(i) + ". " + r.task + ". " + r.deadline.strftime("%#d %b"))
                i += 1
        choice = int(input())
        session.delete(rows[choice-1])
        session.commit()
        print("The task has been deleted!")

print("Bye!")


