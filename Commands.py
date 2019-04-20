from Main.models import Account, Course, Section, AccountSection, AccountCourse
import CurrentUserHelper
import re
from itertools import chain


class Command():

    def __init__(self, opcode, arguments, function):
        self.opcode = opcode
        self.arguments = arguments
        self.function = function


def login(userName, password):

    try:
        CurrentUser = Account.objects.get(userName=userName)
        if CurrentUser.password != password:
            raise Exception("Incorrect password")

    except Account.DoesNotExist:
        raise Exception("Account Not Found")

    return CurrentUser


def logout():
    try:
        CurrentUser = Account.objects.get(currentUser=True)
        CurrentUser.currentUser = False
        CurrentUser.save()
        return "Successfully logged out"
    except Account.DoesNotExist:
        return "Please log in First"
    except Account.MultipleObjectsReturned:
        return "Multiple account Logged in, Something went terribly wrong"


def createAccount(firstName, lastName, userName, title, email):

    # Check that the account trying to be created does not already exist
    if Account.objects.filter(userName=userName).exists():
        return "Account already exists"

    # Make sure the account is trying to be created with a UWM email address
    str = email.split('@', 1)
    if len(str) == 1:
        return "The email address you have entered in not valid.  " \
               "Please make sure you are using a uwm email address in the correct format."
    if str[1] != "uwm.edu":
        return "The email address you have entered in not valid.  " \
               "Please make sure you are using a uwm email address in the correct format."

    # If we get here the account is safe to be created.
    else:
        A = Account()
        A.userName = userName
        A.email = email
        if title.lower() == "ta":
            A.title = 1
        elif title.lower() == "instructor":
            A.title = 2
        else:
            return "Invalid title, account not created"
        A.firstName = firstName
        A.lastName = lastName
        # Make a temporary password for the newly created user
        A.password = A.userName + "456"
        A.save()

        return "Account successfully created.  Temporary password is: " + A.userName + "456"


def deleteAccount(userName):
    if not Account.objects.get(userName=userName).exists():
        return "Account does not exist"
    Account.objects.filter(userName=userName).delete()
    return "Account successfully deleted"


def createCourse(name, number, online, days, start, end):
    # Check that the command has the appropriate number of arguments

    # Course number checks
    if not re.match('^[0-9]*$', number):
        return "Course number must be numeric and three digits long"
    if len(number) != 3:
        return "Course number must be numeric and three digits long"
    # Check that the course does not already exist
    if Course.objects.filter(number=number).exists():
        return "Course already exists"
    # Location checks
    if online.lower() != "online" and online.lower() != "campus":
        return "Location is invalid, please enter campus or online."
    # Days check
    for i in days:
        if i not in 'MTWRFN':
            return "Invalid days of the week, please enter days in the format: MWTRF or NN for online"
    # Check times
    startTime = start
    endTime = end
    if len(startTime) != 4 or len(endTime) != 4:
        return "Invalid start or end time, please use a 4 digit military time representation"
    if not re.match('^[0-2]*$', startTime[0]) or not re.match('^[0-1]*$', endTime[0]):
        return "Invalid start or end time, please use a 4 digit military time representation"
    for i in range(1, 3):
        if not (re.match('^[0-9]*$', startTime[i])) or not (re.match('^[0-9]*$', endTime[i])):
            return "Invalid start or end time, please use a 4 digit military time representation"

    # Else the course is ok to be created
    else:
        c = Course(name=name, number=number)
        if online.lower() == "online":
            c.onCampus = False
        else:
            c.onCampus = True
            c.classDays = days
            c.classHoursStart = start
            c.classHoursEnd = end
        c.save()
        return "Course successfully created"


def createSection(courseNumber, type, sectionNumber, days, start, end):
    # Course number checks
    if not re.match('^[0-9]*$', courseNumber):
        return "Course number must be numeric and three digits long"
    if len(courseNumber) > 3 or len(courseNumber) < 3:
        return "Course number must be numeric and three digits long"

    # Make sure course that the lab is being created for exists ok
    try:
        c = Course.objects.get(number=courseNumber)
    except Course.DoesNotExist:
        return "The Course you are trying to create a lab for does not exist"

    # Make sure the course is not online
    if c.onCampus == False:
        return "You cannot create a lab for an online course"

    # Section number checks
    if not re.match('^[0-9]*$', sectionNumber):
        return "Section number must be numeric and three digits long"
    if len(sectionNumber) > 3 or len(sectionNumber) < 3:
        return "Section number must be numeric and three digits long"

    # Days check
    for i in days:
        if i not in 'MTWRFN':
            return "Invalid days of the week, please enter days in the format: MWTRF"

    # Time checks
    if len(start) != 4 or len(end) != 4:
        return "Invalid start or end time, please use a 4 digit military time representation"
    if not re.match('^[0-2]*$', start[0]) or not re.match('^[0-2]*$', end[0]):
        return "Invalid start or end time, please use a 4 digit military time representation"
    for i in range(1, 3):
        if not (re.match('^[0-9]*$', start[i])) or not (re.match('^[0-9]*$', end[i])):
            return "Invalid start or end time, please use a 4 digit military time representation"

    # Make sure the lab does not already exist
    if Section.objects.filter(course=c, number=sectionNumber).exists():
        return "Lab already exists, lab not added"
    else:
        l = Section.objects.create(course=c)
        l.type = type
        l.sectionNumber = sectionNumber
        l.meetingDays = days
        l.startTime = start
        l.endTime = end
        l.save()
        return "Lab successfully created"


def assignAccCourse(userName, courseNumber):
    # Check if the course is valid
    if not Course.objects.filter(number=courseNumber).exists():
        return "Invalid course number"
    # Check if the user name is valid
    if not Account.objects.filter(userName=userName).exists():
        return "Invalid user name"

    instructor = Account.objects.get(userName=userName)
    course = Course.objects.get(number=courseNumber)
    # title represented as an integer where 4=supervisor 3=administrator
    # 2=Instructor 1=TA. 0=No current User
    # Check if the account is an instructor
    # Check if the course is already assigned
    # Otherwise(if there are no errors found), an instructor can be assigned to a course
    a = AccountCourse()
    a.Account = instructor
    a.Course = course
    a.save()
    return "Instructor was successfully assigned to class"


def assignAccSection(userName, courseNumber, sectionNumber):
    if not Account.objects.filter(userName=userName).exists():
        return "Invalid account name"

    if not Course.objects.filter(number=courseNumber).exists():
        return "Invalid course number"

    course = Course.objects.get(number=courseNumber)

    if not Section.objects.filter(number=sectionNumber, course=course).exists():
        return "Invalid lab section"

    ta = Account.objects.get(userName=userName)

    if not AccountCourse.objects.filter(Account=ta, Course=Course.objects.get(number=courseNumber)).exists():
        return "TA must be assigned to the Course first"

    lab = Section.objects.get(number=sectionNumber, course=course)

    if AccountSection.objects.filter(Section=lab).exists():
        return "Lab section already assigned"

    p = AccountSection()
    p.Account = ta
    p.Section = lab
    p.save()

    return "TA successfully assigned"


def displayAllCourseAssign():
    lst = Course.objects.all()
    courseList = []

    for a in lst:
        courseList.append(displayCourseAssign(a.number))

    return courseList


def displayCourseAssign(courseNumber):
    course = Course.objects.get(number=courseNumber)

    response = course.name + " CS" + str(course.number) + "\n"

    lst = AccountCourse.objects.filter(Course=course)
    instructorList = []

    for a in lst:
        if a.Account.title == 2:
            instructorList.append(str(a.Account))

    response += "Instructors: "
    if not instructorList:
        response += "None"
    else:
        response += ", ".join(instructorList)
        #for a in instructorList:
            #response += a + " "

    response += "\nTeaching Assistants: "

    taList = []

    for a in lst:
        if a.Account.title == 1:
            taList.append(str(a.Account))

    if not taList:
        response += "None"
    else:
        response += ", ".join(taList)
        #for a in taList:
            #response += a + " "
    response += "\n"
    lecSectionList = Section.objects.filter(course=course, type=1)
    labSectionList = Section.objects.filter(course=course, type=0)
    if not lecSectionList and not labSectionList:
        response += "No sections found"
        return response
    else:
        for a in lecSectionList:
            p = AccountSection.objects.filter(Section=a)
            if not p:
                response += str(a) + ": None\n"
            else:
                for q in p:
                    response += str(q.Section) + ": " + str(q.Account) + "\n"
        for a in labSectionList:
            p = AccountSection.objects.filter(Section=a)
            if not p:
                response += str(a) + ": None\n"
            else:
                for q in p:
                    response += str(q.Section) + ": " + str(q.Account) + "\n"

    return response


def viewCourseAssign(userName): # secret message
    if not Account.objects.filter(userName=userName).exists():
        return "Account not found"

    account = Account.objects.get(userName=userName)

    if not AccountCourse.objects.filter(Account=account).exists():
        return str(account) + " does not have any assignments"

    labAssignments = AccountSection.objects.filter(Account=account)

    response = str(account) + " is assigned to: "
    labList = []
    checkList = []
    for a in labAssignments:
        labList.append(str(a.Section))
        checkList.append(a.Section.course)

    response += ", ".join(labList)

    courseAssignments = AccountCourse.objects.filter(Account=account)

    courseList = []
    first = True
    for a in courseAssignments:
        if a.Course not in checkList:
            if first and len(labAssignments) != 0:# all this does is puts a comma after lab sections if present
                response += ", "
                first = False
            courseList.append(str(a.Course))

    response += ", ".join(courseList)

    return response


def getPublicDataList():
    instructorList = Account.objects.filter(title=2)
    taList = Account.objects.filter(title=1)
    # staffList = list(chain(instructorList, taList))
    staffList = instructorList | taList
    directory = []

    for i in staffList:
        directory.append(i.displayPublic())

    directory.sort()
    return directory


def getPrivateDataList():
    instructorList = Account.objects.filter(title=2)
    taList = Account.objects.filter(title='1')
    # staffList = list(chain(instructorList, taList))
    staffList = instructorList | taList
    directory = []

    for i in staffList:
        directory.append(i.displayPrivate())

    directory.sort()
    return directory


def editPubInfo(userName, dict):
    user = Account.objects.get(userName=userName)
    user.firstName = dict["firstname"]



def getCommands():
    return [Command("login", 2, login), Command("logout", 0, logout),
            Command("createaccount", 5, createAccount), Command("deleteaccount", 1, deleteAccount),
            Command("createcourse", 6, createCourse), Command("createsection", 6, createSection),
            Command("assignacccourse", 2, assignAccCourse),
            Command("assignaccsection", 3, assignAccSection),
            Command("viewcourseassign", 1, viewCourseAssign)]

