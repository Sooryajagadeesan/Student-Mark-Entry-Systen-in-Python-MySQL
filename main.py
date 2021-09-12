# package to connect python with MySQL database
import mysql.connector

# all student details are collected and stored here as list of objects
student_list = []

# class for student
class Student:
    def __init__(self,name,marks,department_code):
        self.name = name
        self.marks = marks
        self.department_code = department_code
        self.total = self.find_total()
        self.average = self.find_average()
        self.grade = self.find_grade()

    def find_total(self):
        total = sum(self.marks)
        return total

    def find_average(self):
        average = (self.total)/(len(self.marks))
        return average

    def find_grade(self):
        grade = ""
        avg = int(self.average)
        if avg >90:
            grade = 'O'
        elif avg >80:
            grade = 'A+'
        elif avg >70:
            grade = 'A'
        elif avg >60:
            grade = 'B+'
        elif avg >50:
            grade = 'B'
        else:
            grade = 'U'
        return grade
        
    # def __str__(self):
    #     return f"( name : {self.name}\nmarks : {self.marks}\ntotal : {self.total}\naverage :{self.average}\ngrade : {self.grade} )"
        
        
# this function creates objects and stores it in the student_list list
def create_object(student_name,student_marks,dept_code):
    student_details = Student(student_name,student_marks,dept_code)
    global student_list
    student_list.append(student_details)

# this function gets input from user and call the create_object() function to create the objects
def get_input(count):
    for i in range(count):
        marks = []
        print(f"\nSTUDENT {i+1} DETAILS")
        name = input("Enter name : ")
        while len(name.replace(" ","")) == 0:
            print("\n.....INVALID DATA.....\nPlease Re-enter the data")
            name = input("Enter name : ")
        
        department_codes = [106,104,205]
        student_department_code = int(input("\nChoose your department ID :\nECE  -  106\nCSE  -  104\nIT   -  205\nYour Department ID : "))
        while student_department_code not in department_codes:
            print("\n.....INVALID DEPARTMENT CODE.....CHOOSE AGAIN")
            student_department_code = int(input("Choose your department ID :\nECE  -  106\nCSE  -  104\nIT   -  205\nYour Department ID : "))
        print("\nPLEASE ENTER YOUR MARKS  (out of 100)")
        for j in range(5):
            m = int(input(f"Enter mark {j+1} : "))
            marks.append(m)
    
        create_object(name,marks,student_department_code)

# this function gets the count of students
def count_of_students():
    student_count = int(input("Enter the number of students : "))
    return student_count




#test connecting db
connection = mysql.connector.connect(host ="localhost",user="root",password="!@sooryaMYSQL18#$",database = "guvitask")
# print(connection)
cur = connection.cursor()




# EXECUTION STARTS HERE
count = count_of_students()
get_input(count)
# for i in student_list:
#     print(i)


#function to fill the department table, one time execution is enough !
def fill_department_table():
    record = {
        "ECE" : 106,
        "CSE" : 104,
        "IT" : 205
    }
    for i in record:
        global cur
        cur.execute(f"""INSERT INTO DEPARTMENT (ID,Dept_name)
        VALUES ({record[i]},'{i}');
        """)

# function to fill the student table, executed for every student entry
def fill_student_table():
    global cur
    for i in student_list:
        cur.execute(f"INSERT INTO STUDENT(Name,M1,M2,M3,M4,M5,Dept_id,Total,Average,Grade) VALUES ('{i.name}',{i.marks[0]},{i.marks[1]},{i.marks[2]},{i.marks[3]},{i.marks[4]},'{i.department_code}',{i.total},{i.average},'{i.grade}');")


#fill_department_table() # this line populatesdepartment table, its enough to run that once
fill_student_table() # this line populates the student table

# commit is used to store the changes we made in database
connection.commit()

# finally we have to close the connection to the database
connection.close()
