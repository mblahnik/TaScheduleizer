from django.shortcuts import render, redirect
from django.views import View
from UserInterface import UI
from Commands import login, displayAllCourseAssign, createAccount, getPrivateDataList, getPublicDataList, editPubInfo
from CurrentUserHelper import CurrentUser
from Main.models import Account
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

            check = CU.getCurrentUserTitle(request)

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


class adminPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle != 3:
            return render(request, 'errorPage.html', {"message": "Only admins may view this page"})
        return render(request, 'Accounts/AdminHome.html')


class supervisorPage(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "Only supervisors may view this page"})
        return render(request, 'Accounts/SupervisorHome.html')


class instructorPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle != 2:
            return render(request, 'errorPage.html', {"message": "Only instructors may view this page"})
        return render(request, 'Accounts/InstructorHome.html', {"account": account})


class taPage(View):

    def get(self, request):
        CU = CurrentUser()
        account = CU.getCurrentUser(request)
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle != 1:
            return render(request, 'errorPage.html', {"message": "Only Teaching Assistants may view this page"})
        return render(request, 'Accounts/TaHome.html', {"account": account})


class createAccountView(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)

        if currentusertitle < 3:
            return render(request, 'errorPage.html', {"message": "You do not have permission to View this page"})

        return render(request, 'createAccount.html')

    def post(self, request):
        userName = str(request.POST["username"])
        firstName = str(request.POST["firstname"])
        lastName = str(request.POST["lastname"])
        email = str(request.POST["email"])
        title = str(request.POST["title"])
        #try:
        message = createAccount(userName=userName, firstName=firstName,
                                lastName=lastName, email=email, title=title)

        return render(request, 'createAccount.html', {"message": message})
        #except Exception as e:
         #   return render(request, 'createAccount.html', {"message": str(e)})


class courseAssignmentsList(View):

    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle == 0:
            return render(request, 'errorPage.html', {"message": "You must log in to view this page"})
        courses = displayAllCourseAssign()
        return render(request, 'courseAssignmentList.html', {"courseList": courses})


class deleteAccount(View):
    def get(self, request):
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList
        # CU = CurrentUser()
        # currentusertitle = CU.getCurrentUserTitle(request)
        # if currentusertitle < 3:
            # return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'deleteAccount.html', {"stafflist": staffList})

    def post(self, request):
        username = str(request.POST["username"])
        message = deleteAccount(userName=username)
        instructorList = Account.objects.filter(title=2)
        taList = Account.objects.filter(title='1')
        staffList = instructorList | taList

        return render(request, 'deleteAccount.html', {"message": message, "stafflist": staffList})


class instructorCourse(View):
    def get(self, request):
        CU = CurrentUser()
        currentusertitle = CU.getCurrentUserTitle(request)
        if currentusertitle != 4:
            return render(request, 'errorPage.html', {"message": "You do not have permission to view this page"})
        return render(request, 'assignInstructor.html')

    def post(self, request):
        pass


class directoryView(View):

    def get(self, request):
        CU = CurrentUser()
        title = CU.getCurrentUserTitle(request)

        if title == 0:
            return render(request, 'errorPage.html', {"message": "You Must log in to View this page"})
        if title == 1 or title == 2:
            directory = getPublicDataList()
        else:
            directory = getPrivateDataList()

        return render(request, 'Directory.html', {"directory": directory})


class editPubInfoView(View):

    def get(self, request):
        CU = CurrentUser()
        user = CU.getCurrentUser(request)
        return render(request, 'editPubInfo.html', {'i': user})

    def post(self, request):
        dict = {
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
        user = CU.getCurrentUser(request)
        message = editPubInfo(user, dict)
        return render(request, 'editPubInfo.html', {"message": message})

