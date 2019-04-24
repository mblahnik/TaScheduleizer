from django.test import TestCase
from Main.models import Account, Course, AccountCourse, Section, AccountSection
from Commands import assignAccSection

class TestAssignAccSection(TestCase):
    def setUp(self):
        Account.objects.create(userName="janewayk123", firstName="Kathryn", lastName="Janeway", password="123456",
                               email="janewayk@uwm.com", title=2,
                               address="14 Voyager Drive", city="Delta", state="Quadrant", zipCode="00000",
                               officeNumber="456", officePhone="555-555-5555", officeDays="TR",
                               officeHoursStart="1300", officeHoursEnd="1400", currentUser=False)
        Account.objects.create(userName="picard304", firstName="Jean Luc", lastName="Picard", password="90456",
                               email="picardj@uwm.com", title=1, address="87 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="11111", officeNumber="54",
                               officePhone="777-777-7777", officeDays="W", officeHoursStart="0900",
                               officeHoursEnd="1000", currentUser=False)
        Account.objects.create(userName="kirkj22", firstName="James", lastName="Kirk", password="678543",
                               email="kirkj22@uwm.com", title=4, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)
        Account.objects.create(userName="bones837", firstName="Leonard", lastName="McCoy", password="851468",
                               email="bones837@uwm.com", title=3, address="789 Enterprise Avenue",
                               city="Alpha", state="Quadrant", zipCode="89765", officeNumber="987",
                               officePhone="897-654-398", officeDays="MW", officeHoursStart="1500",
                               officeHoursEnd="1600", currentUser=False)
        self.c1 = Course.objects.create(name="Temporal Mechanics", number="581", onCampus=True, classDays="MW",
                              classHoursStart="0900", classHoursEnd="1030")
        self.c2 = Course.objects.create(name="Warp Theory", number="468", onCampus=True, classDays="TR",
                              classHoursStart="1300", classHoursEnd="1500")
        self.c3 = Course.objects.create(name="Political Turmoil in the Klingon Empire", number="492", onCampus=False)
        Section.objects.create(course=self.c1, type=2, number=401, meetingDays="T", startTime="1500", endTime="1600")
        Section.objects.create(course=self.c2, type=2, number=401, meetingDays="W", startTime="1500", endTime="1600")
        Section.objects.create(course=self.c1, type=1, number=201, meetingDays="MW", startTime="0900", endTime="1030")
        Section.objects.create(course=self.c2, type=1, number=201, meetingDays="TR", startTime="1300", endTime="1500")

    def test_assign_success(self):
        self.assertEqual(assignAccSection("janewayk123", "Temporal Mechanics"), "User was successfully assigned to course")
        self.assertEqual(assignAccSection("picard304", "Warp Theory"), "User was successfully assigned to course")
        self.assertEqual(assignAccSection("janewayk123", "Political Turmoil in the Klingon Empire"), "User was successfully assigned to course")
        self.assertEqual(assignAccSection("picard304", "Political Turmoil in the Klingon Empire"), "User was successfully assigned to course")

    def test_assign_invalid_course(self):
        self.assertEqual(assignAccSection("janewayk123", "Ethics of the Prime Directive"), "Invalid course name")
        self.assertEqual(assignAccSection("picard304", "How to Deal with Children"), "Invalid course name")

    def test_assign_nonexistent_acct(self):
        self.assertEqual(assignAccSection("tuvix009", "Temporal Mechanics"), "Invalid user name")
        self.assertEqual(assignAccSection("SevenOf9", "Warp Theory"), "Invalid user name")
        self.assertEqual(assignAccSection("Mudd847", "Warp Theory"), "Invalid user name")

    def test_assign_invalid_title(self):
        self.assertEqual(assignAccSection("kirkj22", "Temporal Mechanics"), "User is not an instructor or TA")
        self.assertEqual(assignAccSection("bones837", "Temporal Mechanics"), "User is not an instructor or TA")
