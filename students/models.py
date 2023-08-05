from django.db import models
from django.core.validators import MinLengthValidator
from srmapstudents.settings import common

class Student(models.Model):
    id = models.CharField(max_length=13,primary_key=True, validators=[MinLengthValidator(13)])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=20)
    section = models.CharField(max_length=1)
    codeforces_username = models.CharField(max_length=255, unique=True)
    codechef_username = models.CharField(max_length=255, unique=True)
    leetcode_username = models.CharField(max_length=255, unique=True)
    hackerrank_username = models.CharField(max_length=255, unique=True)
    github_username = models.CharField(max_length=255, unique=True)
    linkedin_username = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(common.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CodeForcesDetail(models.Model):
    tag = models.CharField(max_length=255)
    current_rating = models.PositiveIntegerField(null=True)
    maximum_rating = models.PositiveIntegerField(null=True)
    number_of_problems_solved = models.PositiveIntegerField(null=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)

class GitHubDetail(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    number_of_repos = models.PositiveIntegerField()
    valid = models.CharField(max_length=20)

class CodeChefDetail(models.Model):
    rating = models.PositiveIntegerField()
    highest_rating = models.PositiveIntegerField()
    global_rank = models.CharField(max_length=50)
    country_rank = models.CharField(max_length=50)
    no_of_contests = models.PositiveIntegerField()
    number_of_problems_solved = models.PositiveIntegerField()
    division = models.CharField(max_length=255)
    star_rating = models.PositiveSmallIntegerField()
    partially_solved_questions = models.PositiveIntegerField()
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)

class LeetCodeDetail(models.Model):
    general_rank = models.BigIntegerField()
    easy = models.PositiveIntegerField()
    medium = models.PositiveIntegerField()
    hard = models.PositiveIntegerField()
    participated_in_contests = models.BooleanField()
    contest_rank = models.PositiveBigIntegerField()
    number_of_contests = models.PositiveIntegerField()
    contest_rating = models.PositiveIntegerField()
    familiar_languages = models.CharField(max_length=255)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)

# class LinkedIn(models.Model):

# class HackerRank(models.Model):
