"""TaScheduleizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Main import views
from AccountCourse import views as AccCourseViews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_login),
    path('command/', views.commandLine.as_view()),
    path('login/', views.loginPage.as_view()),
    path('administrator/', views.adminPage.as_view()),
    path('supervisor/', views.supervisorPage.as_view()),
    path('instructor/', views.instructorPage.as_view()),
    path('ta/', views.taPage.as_view()),
    path('createaccount/', views.createAccountView.as_view()),
    path('courseassignments/', views.courseAssignmentsList.as_view()),
    path('deleteaccount/', views.deleteAccount.as_view()),
    path('assigninstructor/', AccCourseViews.instructorCourse.as_view()),
    path('assigntacourse/', AccCourseViews.taCourse.as_view()),
    path('assignsection/', views.sectionAssignment.as_view()),
    path('findcourse/', views.accountSection.as_view()),
    path('directory/', views.directoryView.as_view()),
    path('editpubinfo/', views.editPubInfoView.as_view()),
    path('logout/', views.logoutView.as_view()),
    path('createcourse/', views.createCourseView.as_view()),
    path('edituserinfo/', views.editUserInfoView.as_view()),
    path('createsection/', views.createSectionView.as_view()),
    path('contact/', views.contact.as_view()),
    path('deletecourse/', views.deleteCourseView.as_view()),
    path('test', views.testView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



