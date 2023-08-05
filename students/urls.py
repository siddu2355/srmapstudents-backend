from django.urls import path
from . import views

urlpatterns = [
   path("students/", views.StudentList.as_view()), 
   path("students/<str:pk>/", views.StudentDetail.as_view()),
   path('student/me/', views.student_user),
   path("github/", views.github),
   path("codeforces/", views.codeforces),
   path("codechef/", views.codechef),
   path("leetcode/", views.leetcode),
   path("student-details/github-details/", views.GitHubDetailList.as_view()),
   path("student-details/codechef-details/", views.CodeChefDetailList.as_view()),
   path("student-details/codeforces-details/", views.CodeForcesDetailList.as_view()),
   path("student-details/leetcode-details/", views.LeetCodeDetailList.as_view()),
   path("student-details/github-details/<str:pk>/", views.GitHubDetails.as_view()),
   path("student-details/codechef-details/<str:pk>/", views.CodeChefDetails.as_view()),
   path("student-details/codeforces-details/<str:pk>/", views.CodeForcesDetails.as_view()),
   path("student-details/leetcode-details/<str:pk>/", views.LeetCodeDetails.as_view()),
]