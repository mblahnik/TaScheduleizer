from django.test import TestCase
from UserInterface import UI
from Main.models import Account, Course, Section
from AccountCourse.models import AccountCourse


class TestUI(TestCase):

    def setUp(self):
        self.UI = UI()

        Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.edu", title=2,
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)

        Account.objects.create(userName="picard304", firstName="Jean Luc", lastName="Picard", password="90456",
                               email="picardj@uwm.edu", title=1, address="87 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="11111", officeNumber="54",
                               officePhone="777-777-7777", officeDays="W", officeHoursStart="0900",
                               officeHoursEnd="1000", currentUser=False)

        Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.edu", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)

        Account.objects.create(userName="taman", title=1)

        # Set up for Course testing
        Course.objects.create(name="DataStructures", number=351, onCampus=True, classDays="TR",
                              classHoursStart=1200, classHoursEnd=1300)

        Course.objects.create(name="ComputerArchitecture", number=458, onCampus=True, classDays="MW",
                              classHoursStart=1230, classHoursEnd=1345)

        Section.objects.create(course=Course.objects.get(number="351"), sectionNumber=804)

        Section.objects.create(course=Course.objects.get(number="458"), sectionNumber=804)

        # Set up for Labs testing
        Course.objects.create(name="TemporalMechanics", number=784, onCampus=True, classDays="MW",
                              classHoursStart=1000, classHoursEnd=1100)

        Course.objects.create(name="WarpTheory", number=633, onCampus=True, classDays="TR", classHoursStart=1200,
                              classHoursEnd=1250)

        Course.objects.create(name="QuantumMechanics", number=709, onCampus=True, classDays="MWF",
                              classHoursStart=1030, classHoursEnd=1145)

        Course.objects.create(name="Linguistics", number=564, onCampus=False, classDays="TR",
                              classHoursStart=1800, classHoursEnd=1930)

        self.c1 = Course.objects.get(name="TemporalMechanics")
        self.c2 = Course.objects.get(name="WarpTheory")
        self.c3 = Course.objects.get(name="QuantumMechanics")

        Section.objects.create(course=self.c1, sectionNumber=201, meetingDays="W", startTime=1000, endTime=1200)
        Section.objects.create(course=self.c1, sectionNumber=202, meetingDays="F", startTime=1400, endTime=1700)
        Section.objects.create(course=self.c1, sectionNumber=203, meetingDays="T", startTime=1000, endTime=1200)

        # set up for InstructorCourses testing
        self.cheng = Account.objects.create(userName="cheng41", title="2")
        Account.objects.create(userName="bob15", title="2")
        Course.objects.create(number="535", name="Algorithms")
        Course.objects.create(number="537")
        Course.objects.create(number="317", name="DiscreteMath")
        self.course1 = Course.objects.get(number="535")
        self.course2 = Course.objects.get(number="317")
        AccountCourse.objects.create(Course=self.course1, Instructor=self.cheng)

        AccountCourse.objects.create(TA=Account.objects.get(userName="taman"), Course=Course.objects.get(number="317"))

        # set up for assign TA to Lab
        self.datastructures = Course.objects.get(name="DataStructures")
        self.tamanAccount = Account.objects.get(userName="taman")


    """
        login command
        When the login command is entered, it takes two arguments
        -user name
        -password

        If the account does not exist, an error message will be displayed.  If the password it incorrect, 
        an error message will be displayed.  If the command is missing arguments, an error message will be 
        displayed. 

    """

    def test_login_success(self):
        self.assertEqual(self.UI.command("login janewayk123 123456"), "Logged in as janewayk123")

    def test_command_login_success_whitespace(self):
        self.assertEqual(self.UI.command("  login     janewayk123   123456     "), "Logged in as janewayk123")

    def test_command_login_incorrect_password(self):
        self.assertEqual(self.UI.command("login janewayk123 aaaaaaa"), "Incorrect password")

    def test_command_login_account_does_not_exist(self):
        self.assertEqual(self.UI.command("login neelix45 123456"), "Account Not Found")

    def test_command_login_missing_args(self):
        self.assertEqual(self.UI.command("login janewayk123"), "login requires 2 arguments")

    """ 
        createAccount command
        When the createAccount command is entered, it takes 3 arguments:
        -User name 
        -Title
        -Email     
        If arguments are missing from the command, an error message is displayed and the command is not executed.  
    """

    def test_command_createAccount_permission_denied(self):
        self.assertEqual(self.UI.command("createAccount neelix45 TA neelix45@uwm.edu"),
                         "You do not have the credentials to create an account. Permission denied")

    def test_command_createAccount_success(self):
        self.assertEqual(self.UI.command("createAccount neelix45 TA neelix45@uwm.edu"),
                         "Account successfully created.  Temporary password is: neelix45456")

    def test_command_createAccount_missingArguments(self):
        self.assertEqual(self.UI.command("createAccount laForge88"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createAccount username title email")

    def test_command_createAccount_missingArguments2(self):
        self.assertEqual(self.UI.command("createAccount laForge88 instructor"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createAccount username title email")

    def test_command_createAccount_invalidTitle(self):
        self.assertEqual(self.UI.command("createAccount laForge88 engineer laForge88@uwm.edu"),
                         "Invalid title, account not created")

    def test_command_createAccount_no_args(self):
        self.assertEqual(self.UI.command("createAccount"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createAccount username title email")

    def test_command_createAccount_already_exists(self):
        self.assertEqual(self.UI.command("createAccount janewayk123 instructor janewayk@uwm.edu"),
                         "Account already exists")

    def test_command_createAccount_invalid_email(self):
        self.assertEqual(self.UI.command("createAccount crusherw31 TA crusherw31@hotmail.com"),
                         "The email address you have entered in not valid.  Please make sure you are using a uwm email "
                         "address in the correct format.")
        self.assertEqual(self.UI.command("createAccount crusherw31 TA crusherw31"),
                         "The email address you have entered in not valid.  Please make sure you are using a uwm email "
                         "address in the correct format.")

    """
        createCourse command 
        When the createCourse command is entered, it takes six arguments:
        -Course Name 
        -Course Number 
        -Campus or online
        -Meetings days (if online, enter NN)  
        -Start time (if online, enter 0000)
        -End time (if online, enter 0000)

        If the course name matches a database entry a then the course is not created 
        and an error message is displayed and some other stuff

        If a command argument is missing, an error message is displayed. 

        """

    def test_command_createCourse_permission_denied(self):
        self.assertEqual(self.UI.command("createCourse SoftwareEngineering 361 Campus TR 1000 1050"),
                         "You do not have the credentials to create a course. Permission denied")

    def test_command_createCourse_success(self):
        self.assertEqual(self.UI.command("createCourse SoftwareEngineering 361 Campus TR 1000 1050"),
                         "Course successfully created")

    def test_command_createCourse_missingArguments(self):
        self.assertEqual(self.UI.command("createCourse 431 T 1400 1500"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_missingArguments2(self):
        self.assertEqual(self.UI.command("createCourse Dance T 1400 1500"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_missingArguments3(self):
        self.assertEqual(self.UI.command("createCourse Dance 431 1400 1500"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_missingArguments4(self):
        self.assertEqual(self.UI.command("createCourse Dance 431 T 1500"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_missingArguments5(self):
        self.assertEqual(self.UI.command("createCourse Dance 431 Campus T 1400"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_no_args(self):
        self.assertEqual(self.UI.command("createCourse"),
                         "Your command is missing arguments, please enter your command in the following form: "
                         "createCourse courseName courseNumber onCampus daysOfWeek start end")

    def test_command_createCourse_course_exists(self):
        self.assertEqual(self.UI.command("createCourse DataStructures 351 Campus TR 0900 0950"),
                         "Course already exists")

    def test_command_createCourse_invalid_courseNum(self):
        self.assertEqual(self.UI.command("createCourse StellarCartography t67 Campus TR 1650 1830"),
                         "Course number must be numeric and three digits long")

    def test_command_createCourse_invalid_location(self):
        self.assertEqual(self.UI.command("createCourse StellarCartography 456 Enterprise TR 1650 1830"),
                         "Location is invalid, please enter campus or online.")

    def test_command_createCourse_invalid_days(self):
        self.assertEqual(self.UI.command("createCourse StellarCartography 456 Campus Wg7 1650 1830"),
                         "Invalid days of the week, please enter days in the format: MWTRF or NN for online")

    def test_command_createCourse_invalid_times(self):
        self.assertEqual(self.UI.command("createCourse StellarCartography 456 Campus MW 9800 1830"),
                         "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(self.UI.command("createCourse StellarCartography 456 Campus MW 1830 4444"),
                         "Invalid start or end time, please use a 4 digit military time representation")

    """
        When the createSection command is entered, it takes the following arguments:
        -Course number associated with the lab 
        -Lab section number
        -Day(s) of week
        -Begin time
        -End time
        If the lab already exists, a new lab is not created. If arguments are missing, return error. If the 
        associated course is online, a lab cannot be created for it.
    """

    def test_command_createLab_permission_denied(self):
        self.assertEqual(self.UI.command("createSection courseNumber labSection day begin end"),
                         "You do not have the credentials to create a lab. Permission denied")

    def test_command_createLab_success(self):
        self.assertEqual(self.UI.command("createSection 784 101 T 1300 1445"),
                         "Lab successfully created")

    def test_command_createLab_no_args(self):
        self.assertEqual(self.UI.command("createSection"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_lab_exists(self):
        self.assertEqual(self.UI.command("createSection 784 201 W 1000 1200"),
                         "Lab already exists, lab not added")

    def test_command_createLab_missing_course(self):
        self.assertEqual(self.UI.command("createSection labSection day begin end"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_missing_section(self):
        self.assertEqual(self.UI.command("createSection courseNumber day begin end"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_missing_day(self):
        self.assertEqual(self.UI.command("createSection courseNumber labSection begin end"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_missing_begin(self):
        self.assertEqual(self.UI.command("createSection courseNumber labSection day end"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_missing_end(self):
        self.assertEqual(self.UI.command("createSection courseNumber labSection day begin"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "createLab courseNumber labSectionNumber daysOfWeek beginTime endTime")

    def test_command_createLab_course_does_not_exist(self):
        self.assertEqual(self.UI.command("createSection 999 201 M 1400 1500"),
                         "The Course you are trying to create a lab for does not exist")

    def test_command_createLab_invalid_courseNum(self):
        self.assertEqual(self.UI.command("createSection 7aa 204 M 1600 1700"),
                         "Course number must be numeric and three digits long")
        self.assertEqual(self.UI.command("createSection 90872 204 M 1600 1700"),
                         "Course number must be numeric and three digits long")
        self.assertEqual(self.UI.command("createSection tro 204 M 1600 1700"),
                         "Course number must be numeric and three digits long")

    def test_command_createLab_invalid_sectNum(self):
        self.assertEqual(self.UI.command("createSection 784 909089 M 1600 1700"),
                         "Section number must be numeric and three digits long")
        self.assertEqual(self.UI.command("createSection 784 rug M 1600 1700"),
                         "Section number must be numeric and three digits long")
        self.assertEqual(self.UI.command("createSection 784 kku23k M 1600 1700"),
                         "Section number must be numeric and three digits long")

    def test_command_createLab_invalid_days(self):
        self.assertEqual(self.UI.command("createSection 784 204 qrs 1600 1700"),
                         "Invalid days of the week, please enter days in the format: MWTRF")
        self.assertEqual(self.UI.command("createSection 784 204 89TR 1600 1700"),
                         "Invalid days of the week, please enter days in the format: MWTRF")
        self.assertEqual(self.UI.command("createSection 784 204 JHG 1600 1700"),
                         "Invalid days of the week, please enter days in the format: MWTRF")

    def test_command_createLab_invalid_times(self):
        self.assertEqual(self.UI.command("createSection 784 204 M kalj 1700"),
                         "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(self.UI.command("createSection 784 204 M 8909 1700"),
                         "Invalid start or end time, please use a 4 digit military time representation")
        self.assertEqual(self.UI.command("createSection 784 204 M 1400 17"),
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_command_createLab_online(self):
        self.assertEqual(self.UI.command("createSection 564 203 W 1300 1400"),
                         "You cannot create a lab for an online course")

    """
        When the edit command is entered, it takes 4 arguments.
        Only supervisors and administrators can utilize this command
        -Username
        -Field that needs editing 
            - Home phone
            - Email 
            - Office hours (a start time, an end time and days of office hours) 
            - Address 
            - Office Number
            - Office phone Number
            - Password 
        -The new information to replace the current information 

        If the user does not exist, an error message is displayed.
        If command arguments are missing, an error message is displayed. 

    """

    def test_command_edit_permission_denied(self):
        self.assertEqual(self.UI.command("edit username email timmy89@uwm.edu"),
                         "You do not have the credentials to edit this information. Permission denied")

    def test_command_edit_homePhone_success(self):
        self.assertEqual(self.UI.command("edit username homephone 262-555-7134"), "Home phone successfully updated")

    def test_command_edit_email_success(self):
        self.assertEqual(self.UI.command("edit username email timmy345@uwm.edu"), "Email successfully updated")

    def test_command_edit_office_hours_success(self):
        self.assertEqual(self.UI.command("edit username officehours 1500 1600 MW"), "Office hours successfully updated")

    def test_command_edit_address_success(self):
        self.assertEqual(self.UI.command("edit username address 6789 Hilly Avenue Milwaukee WI 53218"),
                         "Address successfully updated")

    def test_command_edit_officeNumber_success(self):
        self.assertEqual(self.UI.command("edit username officeNumber 5679"), "Office number successfully updated")

    def test_command_edit_officePhone_success(self):
        self.assertEqual(self.UI.command("edit username officePhone 262-789-5476"), "Office phone successfully updated")

    def test_command_edit_password_success(self):
        self.assertEqual(self.UI.command("edit username password newPassword"), "Password successfully changed")

    def test_command_edit_error_missing_args1(self):
        self.assertEqual(self.UI.command("edit"), "There are missing arguments in your command. Please enter your "
                                                  "command in the following format: edit username field newInformation")

    def test_command_edit_error_missing_args2(self):
        self.assertEqual(self.UI.command("edit username"), "There are missing arguments in your command, Please enter "
                                                           "your command in the following format: edit username field "
                                                           "newInformation")

    def test_command_edit_error_missing_args3(self):
        self.assertEqual(self.UI.command("edit username homePhone"),"There are missing arguments in your command, Please"
                                                                    " enter you command in the following format: edit "
                                                                    "username field newInformation")

    def test_command_edit_error_user_does_not_exist(self):
        self.assertEqual(self.UI.command("edit username homePhone 262-555-7134"),
                         "The user you specified does not exist in the system, please try again")

    """
        send command 
        Only supervisors and administrators can utilize this command 
        When the sendOutNotification command is entered it takes 2-many arguments: 

        -send -a
        To send notification to all users.

        -send accountName(s) -s
        To send notification to specific users.

        -send accountName
        to send notification to one person
    """

    def test_command_send_permission_denied(self):
        self.assertEqual(self.UI.command("send -a"),
                         "You do not have the credentials to send notifications. Permission denied")

    def test_command_send_specific_success(self):
        self.assertEqual(self.UI.command("send accountName"), "Notification was sent successfully")

    def test_command_send_all_success(self):
        self.assertEqual(self.UI.command("send -a"),
                         "Notification was sent to all users successfully")

    def test_command_send_specific_multiple_success(self):
        self.assertEqual(self.UI.command("send accountName accountName accountName -s"),
                         "Notification was sent to specific people successfully")

    def test_command_send_error(self):
        self.assertEqual(self.UI.command("send accountName"),
                         "We weren't able to send a notification")

    def test_command_send_all_error(self):
        self.assertEqual(self.UI.command("send accountName -a"),
                         "There was an error, notification not sent")

    def test_command_send_specific_error(self):
        self.assertEqual(self.UI.command("send accountNames -s"),
                         "There was an error, notification not sent")

    """
        sendTA command
        The sendTA command takes one argument 
        -classNumber
    """

    def test_command_sendTA_success(self):
        self.assertEqual(self.UI.command("sendTA courseNumber"),
                         "Email sent successfully to all TAs associated with the specified course")

    def test_command_sendTA_error_course_does_not_exist(self):
        self.assertEqual(self.UI.command("sendTA courseNumber"), "Error, course does not exist, email not sent")

    def test_command_sendTA_missingArguments(self):
        self.assertEqual(self.UI.command("sendTA"),
                         "Your command is missing arguments, please enter the command in the following format: "
                         "sendTA courseNumber")

    """
        When the deleteAccount command is entered, it takes two arguments, 
        -name 
        -title
        If a name or title is missing, an error message is displayed
        If the account that the user is trying to delete does not exist, an error 
           message is displayed.          
    """

    def test_command_deleteAccount_permission_denied(self):
        self.assertEqual(self.UI.command("deleteAccount neelix45 TA"),
                         "You do not have the credentials to delete an account. Permission denied")

    def test_command_deleteAccount(self):
        self.assertEqual(self.UI.command("deleteaccount neelix45 TA"), "Account successfully deleted")

    def test_command_deleteAccount_no_name(self):
        self.assertEqual(self.UI.command("deleteAccount TA"),
                         "There are arguments missing, please enter your command in the following format: "
                         "deleteaccount userName title")

    def test_command_deleteAccount_no_argument(self):
        self.assertEqual(self.UI.command("deleteAccount"),
                         "There are arguments missing, please enter your command in the following format: "
                         "deleteaccount userName title")

    def test_command_deleteAccount_doesNotExist(self):
        self.assertEqual(self.UI.command("deleteaccount neelix45 TA"), "Error, Account does not exist")

    """
        When the assignInstructorCourse command is entered it takes 2 arguments: 
        - Instructor user Name
        - class Number
    """

    def test_command_assignInstructorCourse_permission_denied(self):
        self.assertEqual(self.UI.command("assignAccountcourse cheng41 535"),
                         "You do not have the credentials to assign an instructor to a course. Permission denied")

    def test_command_assignInstructorCourse_missingArguments(self):
        self.assertEqual(self.UI.command("assignAccountcourse cheng41"),
                         "There are arguments missing, Please enter your command in the following format: "
                         "assigninstructorcourse userName courseNumber")

    def test_command_assignInstructorCourse_missingArguments2(self):
        self.assertEqual(self.UI.command("assignAccountcourse 535"),
                         "There are arguments missing, Please enter your command in the following format: "
                         "assigninstructorcourse userName courseNumber")

    def test_command_assignInstructorCourse_no_args(self):
        self.assertEqual(self.UI.command("assignAccountcourse"),
                         "There are arguments missing, Please enter your command in the following format: "
                         "assigninstructorcourse userName courseNumber")

    def test_command_assignInstructorCourse_conflict(self):
        self.assertEqual(self.UI.command("assignAccountcourse bob15 535"),
                         "This class is already assigned")

    def test_command_assignInstructorCourse_success(self):
        self.assertEqual(self.UI.command("assignAccountcourse cheng41 537"),
                         "Instructor was successfully assigned to class")

    def test_command_assignInstructorCourse_notInstructor(self):
        self.assertEqual(self.UI.command("assignAccountcourse kirkj22 535"), "Account is not an instructor")

    def test_command_assignInstructorCourse_bad_username(self):
        self.assertEqual(self.UI.command("assignAccountcourse userName 535"), "Invalid user name")

    def test_command_assingInstructorCourse_course_doesNotExist(self):
        self.assertEqual(self.UI.command("assignAccountcourse bob15 999"), "Invalid course number")

    """
        assignTALab
        -When the assignTALab command is entered, it takes three arguments
        -userName of TA to be assigned
        -classNumber
        -Lab section number 
    """

    def test_command_assignTALab_noLogin(self):
        self.assertEqual(self.UI.command("assignAccountSection taman 351 804"),
                         "You do not have the credentials to assign a ta to a lab. Permission denied")

    def test_command_assignTALab_success(self):
        self.assertEqual(self.UI.command("assignAccountSection taman 351 804"), "TA successfully assigned")

    def test_command_assignTALab_tooFew(self):
        self.assertEqual(self.UI.command("assignAccountSection username classNumber"),
                         "Your command has an invalid number of arguments. Please enter your command in the following format: "
                         "assignTALab username classNumber labSectionNumber")

    def test_command_assignTALab_tooMany(self):
        self.assertEqual(self.UI.command("assignAccountSection userName classNumber labsection classNum"),
                         "Your command has an invalid number of arguments. Please enter your command in the following"
                         " format: assignTALab username classNumber labSectionNumber")

    def test_command_assignTALab_invalidCourse(self):
        self.assertEqual(self.UI.command("assignAccountSection taman 111 804"), "Invalid course number")

    def test_command_assignTALav_invalidLab(self):
        self.assertEqual(self.UI.command("assignAccountSection taman 351 801"), "Invalid lab section")

    """
          When the viewInfo command is entered it takes one argument: 
          -accountName 

          If the account does not exist, an error message is displayed, otherwise, public data is displayed   
      """

    def test_command_viewInfo_success(self):
        self.assertEqual(self.UI.command("viewInfo userName"), "")

    def test_command_viewInfo_user_does_not_exist(self):
        self.assertEqual(self.UI.command("viewInfo userName"), "Account does not exist")

    def test_command_viewInfo_no_accountName(self):
        self.assertEqual(self.UI.command("viewInfo"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "viewInfo userName")

    """
        editInfo command
        The editInfo command does not take a userName because it is implied that the user will be editing his/her 
        own information when he/she is logged into the system. 
        When the editInfo command is entered it takes two arguments: 
        -Field that needs editing, can include: 
            -homePhone
            -email
            -officeHours (start time, end time and day(s) of week entered as a string)
            -Address (entered as a string)
            -Password 
        -What the field should be changed to. 

    """

    def test_command_editInfo_homePhone_success(self):
        self.assertEqual(self.UI.command("editInfo homePhone 262-777-8888"), "Home phone successfully updated")

    def test_command_editInfo_email_success(self):
        self.assertEqual(self.UI.command("editInfo email timmy123@uwm.edu"), "Email successfully updated")

    def test_command_editInfo_officeHours(self):
        self.assertEqual(self.UI.command("editInfo officeHours ""start end daysOfWeek"),
                         "Office hours successfully updated")

    def test_command_editInfo_address(self):
        self.assertEqual(self.UI.command("editInfo address ""6785 Holly Lane Milwaukee WI 54389"),
                         "Address successfully updated")

    def test_command_editInfo_password(self):
        self.assertEqual(self.UI.command("editInfo password newPassword"), "Password successfully changed.")

    def test_command_editInfo_missingArgument(self):
        self.assertEqual(self.UI.command("editInfo homePhone"),
                         "Your command is missing arguments, please enter your command in the following format: "
                         "editInfo field newInformation")

    """
        viewCourseAssignments
        When the viewCourseAssignments command is entered, it takes no arguments 
        It is implied that the viewCourseAssignments will display the course assignments 
        for the instructor who is currently logged in to the system. 

    """

    def test_command_viewCourseAssignments_instnoAssign(self):
        self.assertEqual(self.UI.command("viewcourseassign janewayk123"), "janewayk123 does not have any assignments")

    def test_command_viewCourseAssignments_TAnoAssign(self):
        self.assertEqual(self.UI.command("viewcourseassign picard304"), "picard304 does not have any assignments")

    def test_command_viewCourseAssignments_instoneAssign(self):
        self.assertEqual(self.UI.command("viewcourseassign cheng41"), "cheng41 is assigned to: Algorithms")

    def test_command_viewCourseAssignments_TAoneAssign(self):
        self.assertEqual(self.UI.command("viewcourseassign taman"), "taman is assigned to: DiscreteMath")

    def test_command_viewCourseAssignments_invalidTitle(self):
        self.assertEqual(self.UI.command("viewcourseassign kirkj22"),
                         "Only Ta and Instructor accounts can have Assignments")

    def test_command_viewCourseAssignments_invalidName(self):
        self.assertEqual(self.UI.command("viewcourseassign kirkj2"), "Account not found")

    def test_command_viewCourseAssignments_tooFew(self):
        self.assertEqual(self.UI.command("viewcourseassign"),
                         "Your command has an invalid number of arguments. Please enter your command" \
                         " in the following format: viewCourseAssignments userName")

    def test_command_viewCourseAssignments_tooMany(self):
        self.assertEqual(self.UI.command("viewcourseassign jane kirk"),
                         "Your command has an invalid number of arguments. Please enter your command" \
                         " in the following format: viewCourseAssignments userName")

    """
       When the viewTAAssignments command is entered, it takes one argument
       - class Number 

       If the class Number is not entered, an error message is displayed
       If the class does not exist, an error message is displayed 

    """

    def test_command_viewTAAssignments_success(self):
        self.assertEqual(self.UI.command("viewTAAssignments classNumber"), "The TA Assignments are: ")

    def test_command_viewTAAssignments_noClassNum(self):
        self.assertEqual(self.UI.command("viewTAAssignments"),
                         "Your command is missing arguments, please enter the command in the following format: "
                         "viewTAAssignments classNumber")

    def test_command_viewTAAssignments_classDoesNotExist(self):
        self.assertEqual(self.UI.command("viewTAAssignments classNumber"), "Class does not exist")

