from rest_framework.response import Response
from .serializers import CodeChefSerializer, CodeForcesSerializer, GitHubSerializer, StudentSerializer
from .models import CodeChefDetail, CodeForcesDetail, GitHubDetail, Student
from django.shortcuts import * 
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup

class StudentList(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [IsAuthenticated]

class StudentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def student_user(request):
    student = get_object_or_404(Student, user_id=request.user.id)
    serializer = StudentSerializer(student)
    return Response(serializer.data)
    
@api_view()
def github(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    for record in serializer.data:
        stat = 0
        id = record['id']
        username = record['github_username']
        html = requests.get(f"https://github.com/{username}")
        soup = BeautifulSoup(html.text, 'lxml')
        number_of_repos_span = soup.find('span', class_='Counter')
        valid = "Valid Username."
        if number_of_repos_span is not None:
            number_of_repos = int(number_of_repos_span.text)
        else:
            number_of_repos = 0
            valid = "Invalid Username."
        result_data = {
            'student_id': id,
            'number_of_repos': number_of_repos,
            'valid':valid
        }
        try:
            github_details = GitHubDetail.objects.get(pk=id)
        except GitHubDetail.DoesNotExist:
            stat = 404
        if stat == 404:
            seria = GitHubSerializer(data=result_data)
        else:
            seria = GitHubSerializer(github_details, data=result_data)
        seria.is_valid(raise_exception=True)
        seria.save()
    return Response("Data is scraped and stored.")

@api_view()
def codeforces(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    for record in serializer.data:
        stat = 0
        username = record['codeforces_username']
        id = record['id']
        html = requests.get(f'https://codeforces.com/profile/{username}').text
        soup = BeautifulSoup(html, 'lxml')
        tag_div = soup.find('div', class_='user-rank')
        if tag_div is not None:
            tag = tag_div.span.text
        else:
            tag = "Invalid Username."
        rating_div = soup.find('div', class_='main-info main-info-has-badge')
        if rating_div is not None:
            rating = rating_div.find_next('ul').li.span.text
        else:
            rating = 0
        max_rating_span = soup.find('span', class_='smaller')
        if max_rating_span is not None:
            max_rating = max_rating_span.span.find_next('span').text
        else:
            max_rating = 0
        number_of_problems_div = soup.find('div', class_='_UserActivityFrame_counterValue')
        if number_of_problems_div is not None:
            number_of_problems = int(number_of_problems_div.text.replace(' problems', ''))
        else:
            number_of_problems = 0
        result_data = {
                'tag':tag,
                'current_rating':rating,
                'student_id':id,
                'maximum_rating':max_rating,
                'number_of_problems_solved':number_of_problems,
            }
        try:
            codeforces_details = CodeForcesDetail.objects.get(pk=id)
        except CodeForcesDetail.DoesNotExist:
            stat = 404
        if stat == 404:
            seria = CodeForcesSerializer(data = result_data)
        else:
            seria = CodeForcesSerializer(codeforces_details, data = result_data)
        seria.is_valid(raise_exception=True)
        seria.save()
    return Response("Data is scraped and stored.")

@api_view()
def codechef(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    for record in serializer.data:
        stat = 0
        id = record['id']
        username = record['codechef_username']
        html = requests.get(f'https://www.codechef.com/users/{username}').text
        soup = BeautifulSoup(html, 'lxml')
        rank_div = soup.find('div', class_='rating-ranks')
        if rank_div is not None:
            global_rank = int(rank_div.ul.li.a.text)
            country_rank = int(rank_div.ul.li.find_next('li').a.text)
        else:
            global_rank = 0
            country_rank = 0
        number_of_contests_div = soup.find('div', class_='contest-participated-count')
        if number_of_contests_div is not None:
            number_of_contests = int(number_of_contests_div.b.text)
        else:
            number_of_contests = 0
        number_of_problems_solved_section = soup.find('section', class_='rating-data-section problems-solved')
        if number_of_problems_solved_section is not None:
            number_of_problems_solved = int(number_of_problems_solved_section.div.h5.text.replace('Fully Solved (', '').replace(')', ''))
            partially_solved_questions = int(number_of_problems_solved_section.div.h5.find_next('h5').text.replace('Partially Solved (', '').replace(')', ''))
        else:
            number_of_problems_solved = 0
            partially_solved_questions = 0
        rating_div = soup.find('div', class_='rating-number')
        if rating_div is not None:
            rating = int(rating_div.text[0:4].replace("?", "").replace("i", ''))
        else:
            rating = 0
        star_rating_span = soup.find('span', class_='rating')
        if star_rating_span is not None:
            star_rating = star_rating_span.text[0]
        else:
            star_rating = 0
        highest_rating_div = soup.find('div', class_='rating-header text-center')
        if highest_rating_div is not None:
            highest_rating = int(highest_rating_div.small.text.replace("(Highest Rating ", '').replace(')', ''))
        else:
            highest_rating = 0
        division_div =  soup.find('div', class_='rating-number')
        if division_div is not None:
            division = division_div.find_next('div').text.replace('(','').replace(')','')
        else:
            division = "Invalid Username."              
        result_data = {
            'student_id': id,
            'rating': rating,
            'no_of_contests': number_of_contests,
            'number_of_problems_solved':number_of_problems_solved,
            'global_rank':global_rank,
            'country_rank':country_rank,
            'star_rating': star_rating,
            'highest_rating':highest_rating,
            'partially_solved_questions':partially_solved_questions,
            'division':division,
            }
        try:
            codechef_details = CodeChefDetail.objects.get(pk = id)
        except CodeChefDetail.DoesNotExist:
            stat = 404
        if stat == 404: 
            seria = CodeChefSerializer(data=result_data)
        else:
            seria = CodeChefSerializer(codechef_details, data=result_data)
        seria.is_valid(raise_exception=True)
        seria.save()
    return Response("Data is scraped and stored.")


class GitHubDetailList(ListAPIView):
    queryset = GitHubDetail.objects.all()
    serializer_class = GitHubSerializer

class CodeForcesDetailList(ListAPIView):
    queryset = CodeForcesDetail.objects.all()
    serializer_class = CodeForcesSerializer

class CodeChefDetailList(ListAPIView):
    queryset = CodeChefDetail.objects.all()
    serializer_class = CodeChefSerializer

class GitHubDetails(RetrieveAPIView):
    queryset = GitHubDetail.objects.all()
    serializer_class = GitHubSerializer

class CodeForcesDetails(RetrieveAPIView):
    queryset = CodeForcesDetail.objects.all()
    serializer_class = CodeForcesSerializer

class CodeChefDetails(RetrieveAPIView):
    queryset = CodeChefDetail.objects.all()
    serializer_class = CodeChefSerializer
