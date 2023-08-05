from django.contrib import admin
from . import models

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'branch', 'section'] #'usernames', 'get_leetcode_username']
    ordering= ['section']
    list_per_page = 10
    search_fields = ['id__istartswith', 'first_name__istartswith', 'last_name__istartswith', 'branch__istartswith', 'section__istartswith']

    def name(self, student):
        return f'{student.first_name} {student.last_name}'
    # def get_leetcode_username(self, student:models.Student):
    #     return student.usernames.leetcode_username

@admin.register(models.GitHubDetail)
class GitHubDetailAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'name',
        'number_of_repos',
        ]
    list_per_page = 10
    list_select_related = ['student']
    search_fields = ['student__id__istartswith', 'student__first_name__istartswith', 'student__last_name__istartswith']
    def name(self, username):
        return f'{username.student.first_name} {username.student.last_name}'

@admin.register(models.CodeChefDetail)
class CodeChefDetailAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'name',
        'star_rating',
        'rating',
        'highest_rating',
        'country_rank',
        'global_rank',
        'no_of_contests',
        'number_of_problems_solved',
        'partially_solved_questions',
        'division',
        ]
    list_per_page = 10
    list_select_related = ['student']
    search_fields = ['student__id__istartswith', 'student__first_name__istartswith', 'student__last_name__istartswith']
    def name(self, username):
        return username.student.first_name

@admin.register(models.CodeForcesDetail)
class CodeForcesDetailAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'name',
        'tag',
        'current_rating',
        'maximum_rating',
        'number_of_problems_solved',
    ]
    list_per_page = 10
    list_select_related = ['student']
    search_fields = ['student__id__istartswith', 'student__first_name__istartswith', 'student__last_name__istartswith']
    def name(self, username):
        return f'{username.student.first_name} {username.student.last_name}'

@admin.register(models.LeetCodeDetail)
class LeetCodeDetailAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'student_id',
        'general_rank',
        'easy',
        'medium',
        'hard',
    ]
    list_per_page = 10
    list_select_related = ['student']
    search_fields = ['student__id__istartswith', 'student__first_name__istartswith', 'student__last_name__istartswith']
    def name(self, username):
        return f'{username.student.first_name} {username.student.last_name}'
    
