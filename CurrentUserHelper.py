from Main.models import Account


class CurrentUser:

    def setCurrentUser(self, account, request):
        request.session["currentUser"] = account.userName
        request.session["title"] = account.title

    def removeCurrentUser(self, request):
        request.session["currentUser"] = 0
        del request.session["currentUser"]

    def getCurrentUser(self, request):
        account = request.session.get("currentUser", 0)
        try:
            CurrentUser = Account.objects.get(userName=account)
            return CurrentUser
        except Account.DoesNotExist:
            return 0

    def getCurrentUserTitle(self, request):

        return request.session["title"]
       #currentUser = self.getCurrentUser(request)

        #if currentUser is 0:
        #    return 0
        #else:
        #    return currentUser.title

    def getTemplate(self, request):

        title = self.getCurrentUserTitle(request)

        if title == 1:
            return 'Accounts/Tabase.html'
        if title == 2:
            return 'Accounts/InstructorBase.html'
        if title == 3:
            return 'Accounts/AdminBase.html'
        if title == 4:
            return 'Accounts/SupervisorBase.html'
        else:
            return None

