from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
from Commands import login, logout,  deleteAccountCom, createSection,createAccount, editPubInfo, createCourse, assignAccSection, deleteCourseCom
from CurrentUserHelper import CurrentUser
from Main.models import Account, Course, Section, AccountSection
from AccountCourse.models import AccountCourse

# Create your views here.


class commandLine(View):
    def get(self, request):
        return render(request, 'commandline.html')

    def post(self, request):
        yourInstance = UI()
        commandInput = request.POST["command"]
        if commandInput:
            response = yourInstance.command(commandInput)
        else:
            response = ""
        return render(request, 'commandline.html', {"message": response})


def redirect_login(request):
    return redirect('/login/')


class loginPage(View):

    def get(self, request):
        CU = CurrentUser()
        CU.removeCurrentUser(request)
        return render(request, 'loginscreen.html', {"message": ""})

    def post(self, request):
        CU = CurrentUser()
        username = str(request.POST["username"])
        password = str(request.POST["password"])

        try:
            currentUser = login(username, password)
            CU.setCurrentUser(currentUser, request)

            check = currentUser.title

            if check == 1:
                return redirect('/ta/')
            if check == 2:
                return redirect('/instructor/')
            if check == 3:
                return redirect('/administrator/')
            if check == 4:
                return redirect('/supervisor/')

        except Exception as e:
            return render(request, 'loginscreen.html', {"message": str(e)})


class logoutView(View):
    def get(self, request):
        CU = CurrentUser()
        message = logout(CU.getCurrentUser(request))
        CU.removeCurrentUser(request)
        return render(request, "logout.html", {"message": message})


class adminPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 3:
            return render(request, 'errorPage.html', {"message": "Only admins may view this page"})
        return render(request, 'Accounts/AdminHome.html', {"base": base})


class supervisorPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "Only supervisors may view this page"})
        return render(request, 'Accounts/SupervisorHome.html', {"base": base})


class instructorPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 2:
            return render(request, 'errorPage.html', {"message": "Only instructors may view this page"})
        return render(request, 'Accounts/InstructorHome.html', {"account": account, "base": base})


class taPage(View):
    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle != 1:
            return render(request, 'errorPage.html', {"message": "Only Teaching Assistants may view this page"})
        return render(request, 'Accounts/TaHome.html', {"account": account, "base": base})


class createAccountView(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)

        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to View this page"})

        base = CU.getTemplate(request)

        return render(request, 'createAccount.html', {"i": user, "base": base})

    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        base = CU.getTemplate(request)
        userName = str(request.POST["username"])
        firstName = str(request.POST["firstname"])
        lastName = str(request.POST["lastname"])
        email = str(request.POST["email"])
        title = str(request.POST["title"])

        message = createAccount(userName=userName, firstName=firstName,
                                lastName=lastName, email=email, title=title)

        return render(request, 'createAccount.html', {"message": message, "i": user, "base": base})



class courseAssignmentsList(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})

        base = CU.getTemplate(request)
        sectionList = Section.objects.all()
        courses = Course.objects.all()
        accountList = AccountCourse.objects.all()
        accountsec = AccountSection.objects.all()
        return render(request, 'courseAssignmentList.html', {"courseList": courses, "i": user,
                                                             "accountList": accountList, "sectionList": sectionList,
                                                             'accountSec': accountsec, "base" : base})


class deleteAccount(View):
    def get(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'deleteAccount.html', {"stafflist": staffList, "i": user, "base": base})

    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        username = str(request.POST["username"])
        message = deleteAccountCom(username)
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList
        base = CU.getTemplate(request)

        return render(request, 'deleteAccount.html', {"message": message, "stafflist": staffList, "i": user, "base": base})


class accountSection(View):
    def get(self, request):
        CU = CurrentUser()
        currentuser = CU.getCurrentUser(request)
        currentusertitle = currentuser.title
        courseList = []
        base = CU.getTemplate(request)
        if currentusertitle == 4:
            courseList = Course.objects.all()
        elif currentusertitle == 2:
            aCList = AccountCourse.objects.filter(Account=currentuser)
            for i in aCList:
                courseList.append(i.Course)
        else:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'findCourses.html', {"courseList": courseList, "i": currentuser, "base": base})

    def post(self, request):
        courseName = str(request.POST["course"])
        course = Course.objects.get(name=courseName)
        CU = CurrentUser()
        title = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)
        base = CU.getTemplate(request)
        accountList = []
        sectionList = []
        if title == 4:
            aCList = AccountCourse.objects.filter(Course=course)
            for i in aCList:
                accountList.append(i.Account)
            sectionList = Section.objects.filter(course=course)
        elif title == 2:
            aCList = AccountCourse.objects.filter(Course=course)
            for i in aCList:
                if i.Account.title == 1:
                    accountList.append(i.Account)
            sectionList = Section.objects.filter(course=course, type=0)
        return render(request, 'assignSection.html', {"course": course, "accountList": accountList, "sectionList": sectionList, "i": user, "base": base})


class sectionAssignment(View):
    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        accountName = str(request.POST["account"])
        account = Account.objects.get(userName=accountName)
        section = str(request.POST["section"])
        courseName = str(request.POST["course"])
        course = Course.objects.get(name=courseName)
        sec = Section.objects.get(number=section, course=course)
        courseNum = str(sec.course.number)
        base = CU.getTemplate(request)
        message = assignAccSection(accountName, courseNum, section)
        return render(request, 'assignSection.html', {"message": message, "i": user, "base": base})


class directoryView(View):

    def get(self, request):
        CU = CurrentUser()
        title = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)
        if title == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})

        talist = Account.objects.filter(title=1)
        inslist = Account.objects.filter(title=2)

        directory = talist | inslist

        base = CU.getTemplate(request)

        return render(request, 'Directory.html', {"directory": directory, "i": user, "base": base})


class editPubInfoView(View):

    def get(self, request):
        CU = CurrentUser()
        title = CU.getCurrentUser(request)
        base = CU.getTemplate(request)
        if not title:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        editor = CU.getCurrentUser(request)
        return render(request, 'editPubInfo.html', {'i': editor, "editor": editor, "base": base})

    def post(self, request):
        dict = {
            'userName' : str(request.POST.get("username")),
            'firstName': str(request.POST.get("firstname")),
            'lastName': str(request.POST.get('lastname')),
            'email': str(request.POST.get('email')),
            'password': str(request.POST.get('password')),
            'homephone': str(request.POST.get("homephone")),
            'address': str(request.POST.get('address')),
            'city': str(request.POST.get('city')),
            'state': str(request.POST.get('state')),
            'zipcode': str(request.POST.get('zipcode')),
            'officenumber': str(request.POST.get('officenumber')),
            'officephone': str(request.POST.get('officephone')),
            'officedays': str(request.POST.get('officedays')),
            'officestart': str(request.POST.get('officestart')),
            'officeend': str(request.POST.get('officeend'))}
        CU = CurrentUser()
        editor = CU.getCurrentUser(request)
        base = CU.getTemplate(request)

        user = Account.objects.get(userName=dict['userName'].replace(" ", ""))
        message = editPubInfo(user, dict)
        info = makeUserDictionary(user)
        return render(request, 'editPubInfo_success.html', {"message": message, "i": user, "info": info,
                                                            "editor": editor, "base": base})


def makeUserDictionary(user):
    dict = {
        'First Name': user.firstName,
        'Last Name': user.lastName,
        'Email': user.email,
        'Password': user.password,
        'Home phone': user.homePhone,
        'Address': user.address,
        'City': user.city,
        'State': user.state,
        'Zipcode': user.zipCode,
        'Office number': user.officeNumber,
        'Office phone': user.officePhone,
        'Office days': user.officeDays,
        'Office hours start': user.officeHoursStart,
        'Office hours end': user.officeHoursEnd }
    return dict


class createCourseView(View):
    def get(self,request):
        CU = CurrentUser()
        Acc = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        if currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})

        base = CU.getTemplate(request)

        return render(request, 'createCourse.html', {"editor": Acc, "base": base})

    def post(self, request):
        CU = CurrentUser()
        Acc = CU.getCurrentUser(request)

        name = str(request.POST["name"])
        number = str(request.POST["number"])
        onCampus = str(request.POST["onCampus"])
        #days = str(request.POST["days"])
        #start = str(request.POST["start"])
        #end = str(request.POST["end"])

        messsage = createCourse(name, number, onCampus)
        base = CU.getTemplate(request)

        return render(request, 'createCourse.html', {"message": messsage, "editor": Acc, "base": base})


class createSectionView(View):
    def get(self,request):
        CU = CurrentUser()
        Acc = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)
        courseList = Course.objects.all()
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        if currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})

        base = CU.getTemplate(request)
        return render(request, 'createSection.html', {"editor": Acc, "courseList": courseList, "base": base})

    def post(self, request):
        CU = CurrentUser()
        Acc = CU.getCurrentUser(request)
        courseList = Course.objects.all()
        courseName = str(request.POST.get("course"))
        #course = Course.objects.get(name=courseName)
        # courseNum = str(course.number)
        type = str(request.POST["type"])
        number = str(request.POST["number"])
        days = str(request.POST["days"])
        start = str(request.POST["start"])
        end = str(request.POST["end"])

        base = CU.getTemplate(request)
        message = createSection(courseName, type, number, days, start, end)
        return render(request, 'createSection.html', {"message": message, "editor": Acc, "courseList": courseList, "base": base})


class editUserInfoView(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        editor = CU.getCurrentUser(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        if currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})

        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList
        base = CU.getTemplate(request)
        return render(request, 'editUserInfo.html', {"stafflist" : staffList, "editor":editor, "base": base})

    def post(self, request):

        CU = CurrentUser()
        editor = CU.getCurrentUser(request)
        user = str(request.POST['username'])
        account = Account.objects.get(userName=user)
        info = makeUserDictionary(account)
        base = CU.getTemplate(request)
        return render(request, 'editPubInfo.html', {'i': account, "editor": editor, "info": info, "base": base})


class contact(View):

    def get(self, request):
        CU = CurrentUser()
        CU.removeCurrentUser(request)
        return render(request, 'contact.html')

    def post(self, request):
        return render(request, 'contact.html')


class testView(View):
    def get(self, request):
        CU = CurrentUser()
        title = CU.getCurrentUserTitle(request)
        user = CU.getCurrentUser(request)
        base = CU.getTemplate(request)
        return render(request, 'test/testCreateAccount.html', {"i": user, "base": base})


class deleteCourseView(View):
    def get(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        courseList = Course.objects.all()
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        base = CU.getTemplate(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        elif currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'deletecourse.html', {"courselist": courseList, "i": user, "base": base})

    def post(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        courseName = str(request.POST['Cname'])
        message = deleteCourseCom(courseName)
        courseList = Course.objects.all()
        base = CU.getTemplate(request)

        return render(request, 'deletecourse.html', {"message": message, "courselist": courseList, "i": user, "base": base})
