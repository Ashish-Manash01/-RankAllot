# Integration of code

''' # Dashboard implementation 

# Run:

# Login/Register '''

# Preset preferences including slide/withdraw/accept 

# Two rounds of allotment (withdrawal/accept/slide - after showing first round result) - basically remove students
# from the queue who ever accepted/withdrew the seat. Proceeds to second round(last round)

# stats for institute and admin

# Take roles, if Admin-display the entire contents, if student, display his/her 
# hashmap content, school-display their seat allocations.

# Round 1 - preinitialise choices and everything. Rank in a priority queue. Either entire data is in 
# priority queue or the ID and rank. So when Allotment Function runs, prioirity queue gives the ID to be 
# allotted, ptr goes to hash map, checks choices, if valid, increments or allots it to him/her.

# Then withdraw/slide/accept is called, and then process is repeated, again dash board roles,
# admin sees data + seats allotted, student - his data + seat - no priority, and institute - students admitted.



'''
User Interface Window 
'''

# Defining varoius possible roles of the user.

class Role:
    ADMIN = "admin"
    INSTITUTE = "institute"
    STUDENT = "student"

class User:
    def __init__(self, username="", password="", role=""):
        self.username = username
        self.password = password
        self.role = role

# User database (in-memory for simplicity)
users = {
    "admin": User("admin", "DSAPROJECTCS202M", Role.ADMIN),
    "NITK": User("NITK", "NITK", Role.INSTITUTE),
    "NITT": User("NITT", "NITT", Role.INSTITUTE),
    "NITC": User("NITC", "NITC", Role.INSTITUTE),
    "IITB": User("IITB", "IITB", Role.INSTITUTE),
    "IITM": User("IITM", "IITM", Role.INSTITUTE),
}

# Student database - currently initialised for simplicity in a python dictionary,but it can 
# be taken as input from  the user during registration and can be stored in a database, as in a .csv file.

# Currently, the username and the password of the student is initialised to their registration number,
# starting from 24101 upto 24199. Also we have assumed 300 students took up the common entrance examination.
import random
# Define the Student class
class Student:
    def __init__(self, username, password, rank, preferences, role):
        self.username = username
        self.password = password
        self.rank = rank
        self.preferences = preferences  # List of tuples like [(institute, branch), ...]
        self.allocated = None  # To store allocated seat as (institute, branch)
        self.role = role
    
    def __repr__(self):
        return f"{self.username},{self.password},{self.rank},{self.preferences},{self.role}"

import random # We are using the random command to generate random ranks and preferences.
ranks = []
def generate_ranks():
    while(len(ranks) != 300):
        for i in range(1, 301):
            rank = random.randint(1,300)
            if rank in ranks: # Ensuring all elements of 'ranks' are unique.
                continue
            else: 
                ranks.append(rank)
    #print(ranks)
    #print(len(ranks))
    #print(len(set(ranks))) # Cross-checking if all elements of 'ranks' are unique.
    return ranks
ranks = generate_ranks()

def generate_realistic_preferences():
    institutes = ["NITK", "NITT", "NITC", "IITB", "IITM"]
    branches = ["EC", "ME"]  # EC: Electronics, ME: Mechanical
    preferences = []
    no_of_preferences = random.randint(3,5)
    for _ in range(no_of_preferences): # We are allowing a minimum of 3 & a maximum of 5 preferences to each student.
        # Randomly select an institute and a branch
        institute = random.choice(institutes)
        branch = random.choice(branches)
        preferences.append((institute, branch))
    return preferences
    

students = {}
def generate_student_data(): 
    
    for i in range(24101, 24200):
        j = i - 24101
        preferences=generate_realistic_preferences()
        students[i] = Student(i, i, ranks[j], preferences, role=Role.STUDENT)
        
    return students
students = generate_student_data()

#print(students)


'''User Interface Window - Backend'''

def login(username, password, role):
    if role == Role.STUDENT:
        user = students.get(username)
        if user and user.password == password:
            print("Login Successful!")
            return True
        print("Invalid username or password!! Please try again.")
        return False
    else:
        user = users.get(username)
        if user and user.password == password and user.role == role:
            print("Login successful!")
            return True
        print("Invalid username or password!! Please try again.")
        return False

def register_user(username, password, role):
    if username not in students:
        rank = int(input("Please enter your rank: "))
        preferences = input("Please enter your preferences! ")
        students[username] = Student(username, password, rank, preferences, role=Role.STUDENT)
        print("Registration successful!")
    else:
        print("Username already exists.")


'''Priority Queue to sort students based on ascending order of ranks'''

# Priority Queue implementation
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, student_id, rank):
        # Insert student based on rank to maintain sorted order
        index = 0
        while index < len(self.queue) and self.queue[index][1] <= rank:
            index += 1
        self.queue.insert(index, (student_id, rank))

    def dequeue(self):
        # Remove the student with the highest priority (lowest rank)
        if not self.is_empty():
            return self.queue.pop(0)
        return None


'''Seat Allocation System'''
# # Define the seats for each institute and branch.We have taken 5 Engineering institutions
# # and have assumed 2 branches per institute and 10 seats per branch.

# # EC - Electronics and Communication Engineering, ME - Mechanical Engineering

# Define seat capacities for institutes
seat_capacity = 10
institutes = {
    "NITK": {"EC": seat_capacity, "ME": seat_capacity},
    "NITT": {"EC": seat_capacity, "ME": seat_capacity},
    "NITC": {"EC": seat_capacity, "ME": seat_capacity},
    "IITB": {"EC": seat_capacity, "ME": seat_capacity},
    "IITM": {"EC": seat_capacity, "ME": seat_capacity}
}

# Initialize the priority queue and populate it with students based on their rank
priority_queue = PriorityQueue()
for student_id, student in students.items():
    priority_queue.enqueue(student_id, student.rank)

# Dictionary to store final seat allotments for each student
seat_allotments = {student_id: None for student_id in students}

# Seat allocation process
while not priority_queue.is_empty():
    student_id, _ = priority_queue.dequeue()
    student = students[student_id]
    preferences = student.preferences

    # Allocate seat based on preferences
    for institute, branch in preferences:
        if institutes[institute][branch] > 0:  # Check seat availability
            seat_allotments[student_id] = (institute, branch)
            students[student_id].allocated = (institute, branch)
            institutes[institute][branch] -= 1  # Reduce seat count
            break  # Stop after assigning the first available preference


#main()
def main():
    # We want our project interaction window to run till the user wants to exit the window.
    # Using while loop for that.
    flag = True  # As long as flag is True, the loop runs, thus the project window is active.
    while flag:
        print("\n1. Admin Login (A)")
        print("2. Institute Login (I)")
        print("3. Student Register/Login (S)")
        print("4. Exit (E)")
        choice = input("\nChoose an option: ")

        if choice in ['A', 'a']:
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")
            if login(admin_username, admin_password, Role.ADMIN):
                print("Admin dashboard")
                # Admin dashboard - Can view the whole data stored in the system including Student passwords.
                print(f"{students}")
        elif choice in ['I', 'i']:
            institute_username = input("Enter institute username: ")
            institute_password = input("Enter institute password: ")
            if login(institute_username, institute_password, Role.INSTITUTE):
                print("Institute dashboard")
                # Institute dashboard contains the students admitted into the respective institute, under each branch and rank of the student.
                
        elif choice in ['S', 's']:
            student_username = int(input("Enter student username: "))
            if student_username in students:
                student_password = int(input("Enter student password: "))
                if login(student_username, student_password, Role.STUDENT):
                    print("Student dashboard")
                    print(f"Student ID: {student_username},\n Student Rank: {students[student_username].rank},\n Student Preferences: {students[student_username].preferences},\n Allocated Seat: {students[student_username].allocated}")
            else:
                print("Welcome Student! Create a new password for your account!")
                student_password = int(input("Enter student password: "))
                register_user(student_username, student_password, Role.STUDENT)
                print("\nKindly re-login to access your account!\n")

        elif choice in ['E', 'e']:
            print("Exiting...")
            flag = False

        else:
            print("Invalid choice.")


# Calling the main function to run the project code.
main()
