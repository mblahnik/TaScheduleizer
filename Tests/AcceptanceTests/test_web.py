from django.test import TestCase
from django.test import Client
from Main.models import Account, Course, Section
from AccountCourse.models import AccountCourse
from Commands import getPublicDataList, getPrivateDataList, displayAllCourseAssign


class Test_web(TestCase):

    def setUp(self):

        self.c = Client()

        self.account1 = Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.com", title=2,
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)

        self.account2 = Account.objects.create(userName="picard304", firstName="Jean Luc", lastName="Picard", password="90456",
                               email="picardj@uwm.com", title=1, address="87 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="11111", officeNumber="54",
                               officePhone="777-777-7777", officeDays="W", officeHoursStart="0900",
                               officeHoursEnd="1000", homePhone='123-456-7893', currentUser=False)

        self.account3 = Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.com", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)

        self.account4 = Account.objects.create(userName="admin", title=3, password="password")

        Account.objects.create(userName="jerry2", firstName="Jerry", lastName="Smith")
        # Set up for Course testing
        Course.objects.create(name="DataStructures", number=351, onCampus=True)

        Course.objects.create(name="ComputerArchitecture", number=458, onCampus=True)

        Section.objects.create(course=Course.objects.get(number="351"), number=804)

        Section.objects.create(course=Course.objects.get(number="351"), number=404)

        Section.objects.create(course=Course.objects.get(number="458"), number=804)

        # Set up for section testing
        Course.objects.create(name="TemporalMechanics", number=784, onCampus=True)

        Course.objects.create(name="WarpTheory", number=633, onCampus=True)

        Course.objects.create(name="QuantumMechanics", number=709, onCampus=True)

        Course.objects.create(name="Linguistics", number=564, onCampus=False)

        self.c1 = Course.objects.get(name="TemporalMechanics")
        self.c2 = Course.objects.get(name="WarpTheory")
        self.c3 = Course.objects.get(name="QuantumMechanics")

        Section.objects.create(course=self.c1, number=201, meetingDays="W", startTime=1000, endTime=1200)
        Section.objects.create(course=self.c1, number=202, meetingDays="F", startTime=1400, endTime=1700)
        Section.objects.create(course=self.c1, number=203, meetingDays="T", startTime=1000, endTime=1200)

        # set up for AssignAccountCourses testing
        self.cheng = Account.objects.create(userName="cheng41", title="2")
        self.taman = Account.objects.create(userName="taman", title="1")
        Account.objects.create(userName="bob15", title="2")
        Course.objects.create(number="535", name="Algorithms")
        Course.objects.create(number="537")
        discreteMath = Course.objects.create(number="317", name="DiscreteMath")
        self.course1 = Course.objects.get(number="535")
        self.course2 = Course.objects.get(number="317")
        AccountCourse.objects.create(Course=self.course1, Account=self.cheng)
        AccountCourse.objects.create(Account=self.taman, Course=discreteMath)

        # set up for assign TA to Section
        self.datastructures = Course.objects.get(name="DataStructures")
        self.tamanAccount = Account.objects.get(userName="taman")

        # setup for directory view
        self.pubDirecotry = getPublicDataList()
        self.privateDirecotry = getPrivateDataList()

        self.startdefault = Account._meta.get_field('officeHoursStart').get_default()
        self.enddefault = Account._meta.get_field('officeHoursEnd').get_default()
        self.daysdefault = Account._meta.get_field('officeDays').get_default()

    """
    login
    """

    def test_login_wrong_password(self):
        response = self.c.post('/login/', {'username': 'janewayk123', 'password': '********'})
        self.assertEqual(response.context['message'],
                         "Incorrect password")

    def test_login_username_does_not_exist(self):
        response = self.c.post('/login/', {'username': 'ariana02', 'password': '0192pg'})
        self.assertEqual(response.context['message'],
                         "Account Not Found")


    """
    createAccount 
    """

    def test_createAccount_render(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createaccount/', {'firstname': 'Dan', 'lastname': 'Miles',
                                                   'username': 'miles', 'title': 'TA',
                                                   'email': 'miles@uwm.edu'})
        self.assertEqual(response.status_code, 200)

    def test_createAccount_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createaccount/', {'firstname': 'Miles', 'lastname': 'OBrien',
                                                   'username': 'obrien31', 'title': 'TA',
                                                   'email': 'obrien31@uwm.edu'})
        self.assertEqual(response.context['message'],
                         "Account successfully created.  Temporary password is: obrien31456")

    def test_createAccount_alreadyexists(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createaccount/', {'firstname': 'Jean Luc', 'lastname': 'Picard',
                                                   'username': 'picard304', 'title': 'TA',
                                                   'email': 'picardj@uwm.edu'})
        self.assertEqual(response.context['message'], "Account already exists")

    def test_createAccount_invalid_email(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createaccount/', {'firstname': 'Harry', 'lastname': 'Kim',
                                                   'username': 'kim4', 'title': 'Instructor',
                                                   'email': 'kim4@starfleet.com'})
        self.assertEqual(response.context['message'], "The email address you have entered in not valid.  "
                                                      "Please make sure you are using a uwm email address in the "
                                                      "correct format.")

    def test_createAccount_invalid_title(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createaccount/', {'firstname': 'Harry', 'lastname': 'Kim',
                                                   'username': 'kim4', 'title': 'Engineer',
                                                   'email': 'kim4@uwm.edu'})
        self.assertEqual(response.context['message'], "Invalid title, account not created")

    """
    deleteAccount

    """

    def test_deleteAccount_render(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/deleteaccount/', {'username': 'jerry2'})
        self.assertEqual(response.status_code, 200)

    def test_deleteAccount_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/deleteaccount/', {'username': 'jerry2'})

        self.assertEqual(response.context['message'],
                         "Account successfully deleted")

    def test_deleteAccount_doesnotexists(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/deleteaccount/', {'username':'henry42'})

        self.assertEqual(response.context['message'], "Account does not exist")

    """
    createCourse
    """

    def test_createCourse_render(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 520,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.status_code, 200)

    def test_createCourse_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 520,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course successfully created")

    def test_createCourse_invalidNumber(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 1024,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course number must be numeric and three digits long")

    def test_createCourse_invalidNumber2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 1,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course number must be numeric and three digits long")

    def test_createCourse_invalidNumber3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 'abc',
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course number must be numeric and three digits long")

    def test_createCourse_invalidNumber4(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerNetwork', 'number': 40,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course number must be numeric and three digits long")

    def test_createCourse_course_exists(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'ComputerSecurity', 'number': 633,
                                                  'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "Course already exists")

    def test_createCourse_invalid_locations(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': 'hybrid'})
        self.assertEqual(response.context['message'], "Location is invalid, please enter campus or online.")

    def test_createCourse_invalid_locations2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': '6'})
        self.assertEqual(response.context['message'], "Location is invalid, please enter campus or online.")

    def test_createCourse_invalid_locations3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'Server Side Web Programming', 'number': 452,
                                                  'onCampus': 'q'})
        self.assertEqual(response.context['message'], "Location is invalid, please enter campus or online.")

    def test_createCourse_name_exists(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createcourse/', {'name': 'DataStructures', 'number': 332, 'onCampus': 'campus'})
        self.assertEqual(response.context['message'], "A course with this name already exists")


    """
    createSection
    type is an integer field, 1 for lecture section, 0 for lab section. 
    """

    def test_createSection_Lab_render(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                    'days': 'TR', 'start': 1400,
                                                    'end': 1600})
        self.assertEqual(response.status_code, 200)

    def test_createSection_Lab_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                    'days': 'TR', 'start': 1400,
                                                    'end': 1600})

        self.assertEqual(response.context['message'], "Section successfully created.")

    def test_createSection_Lec_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 401,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'], "Section successfully created.")

    def test_createSection_Lec_invalidNumber(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lecture section number must be 400 level, numeric, and three digits long.")

    def test_createSection_Lec_invalidNumber2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 10,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lecture section number must be 400 level, numeric, and three digits long.")

    def test_createSection_Lec_invalidNumber3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 2,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lecture section number must be 400 level, numeric, and three digits long.")

    def test_createSection_Lec_invalidNumber4(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 'abc',
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lecture section number must be 400 level, numeric, and three digits long.")

    def test_createSection_Lab_invalidNumber(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 401,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lab section number must be 200 level, numeric, and three digits long.")

    def test_createSection_Lab_invalidNumber2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 4,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lab section number must be 200 level, numeric, and three digits long.")

    def test_createSection_Lab_invalidNumber3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 'abc',
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lab section number must be 200 level, numeric, and three digits long.")

    def test_createSection_Lab_invalidNumber4(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 20,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Lab section number must be 200 level, numeric, and three digits long.")

    def test_createSection_Lab_invalidCourseNumber(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 3551, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'], "Course number must be numeric and three digits long")

    def test_createSection_onlineCourseLec(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 564, 'type': 1, 'number': 401,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'], "Section successfully created.")

    def test_createSection_onlineCourseLab(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 564, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'], "You cannot create a lab section for an online course.")

    def test_createSection_invalidDays(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TRQ', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Invalid days of the week, please enter days in the format: MWTRF")

    def test_createSection_invalidStart(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': "Now",
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createSection_invalidStart2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 999,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createSection_invalidStart3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1299,
                                                   'end': 1600})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createSection_invalidEnd(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': "Never"})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createSection_invalidEnd2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 9999})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def test_createSection_invalidEnd3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 0, 'number': 201,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 89765})

        self.assertEqual(response.context['message'],
                         "Invalid start or end time, please use a 4 digit military time representation")

    def teat_createSection_invalidTime(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 401,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1300})

        self.assertEqual(response.context['message'], "End time must be after start time.")

    def test_createSection_exists(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/createsection/', {'course': 351, 'type': 1, 'number': 404,
                                                   'days': 'TR', 'start': 1400,
                                                   'end': 1600})

        self.assertEqual(response.context['message'], "Section already exists; section not added.")

    """
    editPubInfo
    """

    def test_editPubInfo_render(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'James',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.status_code, 200)


    def test_editPubInfo_firstName(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'James',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_firstName_none(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': '',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: You must enter a first name")

    def test_editPubInfo_password_none(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'James',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: You must enter a password")

    def test_editPubInfo_password_none_email_none(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'James',
                                                 'lastname': 'Picard', 'email': '',
                                                'password': '', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: You must enter an email, You must enter a password")




    def test_editPubInfo_lastName(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Brooks', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_two_fields(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Chicago', 'state': 'Illinois',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")


    def test_editPubInfo_homephone_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': 'abc-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Errors: Home Phone can only contain numbers")

    def test_editPubInfo_officephone_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '77c-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Errors: Office Phone can only contain numbers")

    def test_editPubInfo_zipcode_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '1111b', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: ZipCode my be only numeric")

    def test_editPubInfo_zipcode_invalid2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': 'a', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: ZipCode my be only numeric")

    def test_editPubInfo_officenum_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '5q4', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: Office Number must be numeric")

    def test_editPubInfo_officenum_invalid2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': 'g',
                                                 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: Office Number must be numeric")

    def test_editPubInfo_firstname_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc12', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: First Name can only contain letters")

    def test_editPubInfo_lastname_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard12',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: Last name can only contain letters")

    def test_editPubInfo_city_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha12', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: City must contain only letters")


    def test_editPubInfo_city_none(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': '', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_city_invalid2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': '000045', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: City must contain only letters")

    def test_editPubInfo_state_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant12',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: State must contain only letters")

    def test_editPubInfo_state_none(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': '',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_state_invalid2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': '999999',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: State must contain only letters")

    def test_editPubInfo_officetimes_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304','firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '9900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: Invalid start time, please use a "
                                                      "4 digit military time representation")

    def test_editPubInfo_officetimes_invalid2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response1 = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': '13009'})

        self.assertEqual(response1.context['message'], "Errors: Invalid end time, please use a "
                         "4 digit military time representation")

    def test_editPubInfo_officetimes_invalid3(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0900', 'officeend': 'b'})

        self.assertEqual(response.context['message'], "Errors: Invalid end time, please use a "
                                                      "4 digit military time representation")

    def test_editPubInfo_officetimes_invalid4(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username':'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '0abc', 'officeend': 'b'})

        self.assertEqual(response.context['message'], "Errors: Invalid start time, please use a "
                                                      "4 digit military time representation, "
                                                      "Invalid end time, please use a 4 digit military "
                                                      "time representation")

    def test_editPubInfo_officetimes_invalid5(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/',
                               {'username': 'picard304', 'firstname': 'Jean Luc', 'lastname': 'Picard',
                                'email': 'picardj@uwm.edu',
                                'password': '90456', 'homephone': '123-456-7893',
                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                'officedays': 'W', 'officestart': '8000000', 'officeend': '1300'})

        self.assertEqual(response.context['message'], "Errors: Invalid start time, please use a "
                                                      "4 digit military time representation")


    def test_editPubInfo_start_no_end_default(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304','firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '1300',
                                                 'officeend': str(self.enddefault)})
        self.assertEqual(response.context['message'], "Errors: You must enter both a start and end time for office hours")


    def test_editPubInfo_start_no_end2_emptString(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username':'picard304','firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '1300',
                                                 'officeend': ''})
        self.assertEqual(response.context['message'], "Errors: You must enter both a start and end time for office hours")


    def test_editPubInfo_end_noStart_default(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': str(self.startdefault),
                                                 'officeend': '1400'})
        self.assertEqual(response.context['message'], "Errors: You must enter both a start and end time for office hours")

    def test_editPubInfo_end_noStart_emptString(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '',
                                                 'officeend': '1400'})
        self.assertEqual(response.context['message'], "Errors: You must enter both a start and end time for office hours")

    def test_editPubInfo_times_noDays_default(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': str(self.daysdefault), 'officestart': '1300',
                                                 'officeend': '1400'})
        self.assertEqual(response.context['message'], "Errors: You must enter office days if you enter office hours")

    def test_editPubInfo_times_noDays_default_emptString(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': '', 'officestart': '1300',
                                                 'officeend': '1400'})
        self.assertEqual(response.context['message'], "Errors: You must enter office days if you enter office hours")

    def test_editPubInfo_days_noTimes_default(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'M', 'officestart': str(self.startdefault),
                                                 'officeend': str(self.enddefault)})
        self.assertEqual(response.context['message'], "Errors: You must enter office hours if you enter office days")

    def test_editPubInfo_change_multipleFields_three(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'James',
                                                 'lastname': 'Brooks', 'email': 'james@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_change_multipleFields_four(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Bob',
                                                 'lastname': 'Smith', 'email': 'bob@uwm.edu',
                                                 'password': '20987', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_change_multipleFields_five(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Mike',
                                                 'lastname': 'Chay', 'email': 'mike@uwm.edu',
                                                 'password': 'password', 'homephone': '444-444-4444',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Fields successfully updated")

    def test_editPubInfo_change_multipleFields_six(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Thomas',
                                                 'lastname': 'Rivers', 'email': 'tom@uwm.edu',
                                                 'password': '123456', 'homephone': '444-444-4449',
                                                 'address': '102 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})
        self.assertEqual(response.context['message'], "Fields successfully updated")


    def test_editPubInfo_FN_LN_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': '12',
                                                 'lastname': '42', 'email': 'picardj@uwm.edu',
                                                'password': '90456', 'homephone': '123-456-7893',
                                                'address': '87 Enterprise Avenue', 'city': 'Alpha', 'state': 'Quadrant',
                                                'zipcode': '11111', 'officenumber': '54', 'officephone': '777-777-7777',
                                                'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: First Name can only contain letters, "
                                                      "Last name can only contain letters")

    def test_editPubInfo_FN_LN_email_HP_CITY_invalid(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': '12',
                                                 'lastname': '42', 'email': 'picardj@hotmail.edu',
                                                 'password': '90456', 'homephone': '12g-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': '89',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: First Name can only contain letters, "
                                                      "Last name can only contain letters, The email address you have "
                                                      "entered is not valid. Please make sure you are using a uwm email "
                                                      "address in the correct format., Home Phone can only "
                                                      "contain numbers, City must contain only letters")

    def test_editPubInfo_correct_FN_incorrect_LN(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jim',
                                                 'lastname': '42', 'email': 'picardj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '0900', 'officeend': '1000'})

        self.assertEqual(response.context['message'], "Errors: Last name can only contain letters")

    def test_editPubInfo_correct_email_days_no_times_empStrings(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'pj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': '', 'officeend': ''})

        self.assertEqual(response.context['message'], "Errors: You must enter office hours if you enter office days")

    def test_editPubInfo_correct_email_days_no_times_defaults(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/editpubinfo/', {'username': 'picard304', 'firstname': 'Jean Luc',
                                                 'lastname': 'Picard', 'email': 'pj@uwm.edu',
                                                 'password': '90456', 'homephone': '123-456-7893',
                                                 'address': '87 Enterprise Avenue', 'city': 'Alpha',
                                                 'state': 'Quadrant',
                                                 'zipcode': '11111', 'officenumber': '54',
                                                 'officephone': '777-777-7777',
                                                 'officedays': 'W', 'officestart': str(self.startdefault),
                                                 'officeend': str(self.enddefault)})

        self.assertEqual(response.context['message'], "Errors: You must enter office hours if you enter office days")

    """
    Assign Account Course tests 
    """

    def test_assignInsCourse_render(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'picard304', 'course':'DataStructures'})
        self.assertEqual(response.status_code, 200)

    def test_assignInsCourse_success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'picard304', 'course':'DataStructures'})
        self.assertEqual(response.context['message'], "User was successfully assigned to course")

    def test_assignInsCourse_course_does_not_exits(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username':'picard304', 'course':'Dance'})
        self.assertEqual(response.context['message'], "Course does not exist")

    def test_assignInsCourse_user_does_not_exist(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username':'shane22', 'course': 'DataStructures'})
        self.assertEqual(response.context['message'], "Invalid user name")

    def test_assignTACourse_user_does_not_exist(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigntacourse/', {'username': 'shane22', 'course': 'DataStructures'})
        self.assertEqual(response.context['message'], "Invalid user name")

    """
    Viewing information tests
    """

    def test_viewPublicInfo_not_logged_in(self):
        response = self.c.get('/directory/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_viewPublicInfo_success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/directory/')

    """
    Testing Account Home Pages
    """

    def test_viewTAHome_Success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})

        response = self.c.get('/ta/')

        self.assertEqual(response.context['account'], self.account2)

    def test_viewInstructorHome_success(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})

        response = self.c.get('/instructor/')

        self.assertEqual(response.context['account'], self.account1)


    """
    Send out Notification tests 
    """

    def test_sendOutNotification_ins_success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'janewayk123', 'course':'DataStructures'})
        self.assertEqual(response.context['message'], "Instructor was successfully assigned to class, "
                                                      "Notification sent successfully")

    def test_sendOutNotification_TA_success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'picard304', 'course': 'DataStructures'})
        self.assertEqual(response.context['message'], "Instructor was successfully assigned to class, "
                                                      "Notification sent successfully")

    def test_sendOutNotification_TA_not_success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'picard304', 'course': 'DataStructures'})
        self.assertEqual(response.context['message'], "Instructor was successfully assigned to class, "
                                                      "But failed to send notification")

    def test_sendOutNotification_ins_not_success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/assigninstructor/', {'username': 'janewayk123', 'course': 'DataStructures'})
        self.assertEqual(response.context['message'], "Instructor was successfully assigned to class, "
                                                      "But failed to send notification")

    """
    Tests to write.
    - Test access each page without logging in
    - Test delete course
    - Test delete assignments 
    // 
    """

    def test_viewTaHome_noLogin(self):
        response = self.c.get('/ta/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_viewTaHome_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/ta/')
        self.assertEqual(response.context['message'], "Only Teaching Assistants may view this page")

    def test_viewTaHome_AdminLogin(self):
        self.c.post('/login/', {'username': 'admin', 'password': 'password'})
        response = self.c.get('/ta/')
        self.assertEqual(response.context['message'], "Only Teaching Assistants may view this page")

    def test_viewTahome_SupervisorLogin(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.get('/ta/')
        self.assertEqual(response.context['message'], "Only Teaching Assistants may view this page")

    def test_viewInstructorHome_nologin(self):
        response = self.c.get('/instructor/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_viewInsturctorHome_Talogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/instructor/')
        self.assertEqual(response.context['message'], "Only instructors may view this page")

    def test_viewInstructorHome_AdminLogin(self):
        self.c.post('/login/', {'username': 'admin', 'password': 'password'})
        response = self.c.get('/instructor/')
        self.assertEqual(response.context['message'], "Only instructors may view this page")

    def test_viewInstructorHome_SupervisorLogin(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.get('/instructor/')
        self.assertEqual(response.context['message'], "Only instructors may view this page")

    def test_viewAdminHome_nologin(self):
        response = self.c.get('/administrator/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_viewAdminHome_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/administrator/')
        self.assertEqual(response.context['message'], "Only admins may view this page")

    def test_viewAdminHome_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/administrator/')
        self.assertEqual(response.context['message'], "Only admins may view this page")

    def test_viewAdminHome_SupervisorLogin(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.get('/administrator/')
        self.assertEqual(response.context['message'], "Only admins may view this page")

    def test_viewSupervisorHome_nologin(self):
        response = self.c.get('/supervisor/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_viewSupervisorHome_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/supervisor/')
        self.assertEqual(response.context['message'], "Only supervisors may view this page")

    def test_viewSupervisorHome_Instructorlogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/supervisor/')
        self.assertEqual(response.context['message'], "Only supervisors may view this page")

    def test_viewSupervisorHome_AdminLogin(self):
        self.c.post('/login/', {'username': 'admin', 'password': 'password'})
        response = self.c.get('/supervisor/')
        self.assertEqual(response.context['message'], "Only supervisors may view this page")

    def test_createAccount_nologin(self):
        response = self.c.get('/createaccount/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_createAccount_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/createaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to View this page")

    def test_createAccount_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/createaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to View this page")

    def test_viewCourseAssignmenets_nologin(self):
        response = self.c.get('/courseassignments/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_deleteAccount_nologin(self):
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_deleteAccount_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_deleteAccount_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignInsCourse_nologin(self):
        response = self.c.get('/assigninstructor/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_assignInsCourse_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/assigninstructor/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignInsCourse_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/assigninstructor/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignInsCourse_AdminLogin(self):
        self.c.post('/login/', {'username': 'admin', 'password': 'password'})
        response = self.c.get('/assigninstructor/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignTaCourse_nologin(self):
        response = self.c.get('/assigntacourse/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_assignTaCourse_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/assigntacourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignTaCourse_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/assigntacourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_assignTaCourse_AdminLogin(self):
        self.c.post('/login/', {'username': 'admin', 'password': 'password'})
        response = self.c.get('/assigntacourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_directory_nologin(self):
        response = self.c.get('/directory/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_editPubInfo_nologin(self):
        response = self.c.get('/editpubinfo/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_createCourse_nologin(self):
        response = self.c.get('/createcourse/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_createCourse_Talogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/createcourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_createCourse_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/createcourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_editUserInfo_nologin(self):
        response = self.c.get('/edituserinfo/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_editUserInfo_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/edituserinfo/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_editUserInfo_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/edituserinfo/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_deleteAccount_nologin2(self):
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_deleteAccount_TaLogin2(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_deleteAccount_InstructorLogin2(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/deleteaccount/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_deleteCourse_nologin(self):
        response = self.c.get('/deletecourse/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_deleteCourse_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/deletecourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_deleteCourse_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/deletecourse/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_createSection_nologin(self):
        response = self.c.get('/createsection/')
        self.assertEqual(response.context['message'], "You must log in to view this page")

    def test_createSection_TaLogin(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.get('/createsection/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    def test_createSection_InstructorLogin(self):
        self.c.post('/login/', {'username': 'janewayk123', 'password': '123456'})
        response = self.c.get('/createsection/')
        self.assertEqual(response.context['message'], "You do not have permission to view this page")

    """
    Delete Account tests Start here
    """

    def test_deleteAccount_Success(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/deleteaccount/', {'username': 'janewayk123'})
        self.assertEqual(response.context['message'], "Account successfully deleted")

    def test_deleteAccount_accountNotFound(self):
        self.c.post('/login/', {'username': 'picard304', 'password': '90456'})
        response = self.c.post('/deleteaccount/', {'username': 'secretAccount'})
        self.assertEqual(response.context['message'], "Account does not exist")

    """
    Delete Course tests
    """

    def test_deleteCourse_Success(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/deletecourse/', {'Cname': 'TemporalMechanics'})
        self.assertEqual(response.context['message'], "Course successfully deleted")

    def test_deleteCourse_notFound(self):
        self.c.post('/login/', {'username': 'kirkj22', 'password': '678543'})
        response = self.c.post('/deletecourse/', {'Cname': 'secretCourse'})
        self.assertEqual(response.context['message'], "Course does not exist")

