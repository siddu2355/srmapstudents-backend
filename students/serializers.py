from rest_framework import serializers
from students.models import CodeChefDetail, CodeForcesDetail, GitHubDetail, Student, LeetCodeDetail
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name')
    user_id = serializers.IntegerField()
    class Meta:
        model = Student
        fields = [
            'id', 
            'name', 
            'first_name', 
            'last_name', 
            'branch', 
            'section', 
            'github_username',
            'codechef_username',
            'codeforces_username',
            'linkedin_username',
            'leetcode_username',
            'hackerrank_username', 
            'user_id'
            ]

    def get_name(self, student:Student):
        return (student.first_name + " " + student.last_name)

class GitHubSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=13)
    class Meta:
        model = GitHubDetail
        fields = ['student_id', 'number_of_repos', 'valid']

class CodeForcesSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=13)
    class Meta:
        model = CodeForcesDetail
        fields = ['student_id', 'tag', 'current_rating', 'maximum_rating', 'number_of_problems_solved']

class CodeChefSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=13)
    class Meta:
        model = CodeChefDetail
        fields = [
            'student_id', 
            'rating', 
            'global_rank', 
            'country_rank', 
            'no_of_contests', 
            'number_of_problems_solved', 
            'star_rating', 
            'highest_rating', 
            'partially_solved_questions',
            'division',
            ]

class LeetCodeSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(max_length=13)
    class Meta:
        model = LeetCodeDetail
        fields = [
            'general_rank', 
            'easy',
            'medium',
            'hard',
            'participated_in_contests',
            'contest_rank', 
            'number_of_contests', 
            'contest_rating', 
            'familiar_languages',
            'student_id', 
            ]