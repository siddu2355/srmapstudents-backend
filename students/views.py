from rest_framework.response import Response
from .serializers import CodeChefSerializer, CodeForcesSerializer, GitHubSerializer, StudentSerializer, LeetCodeSerializer
from .models import CodeChefDetail, CodeForcesDetail, GitHubDetail, Student, LeetCodeDetail
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

@api_view()
def home(request):
    return Response('''Home Page  try:  admin/  auth/ auth/  srmapstudents/''')

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
            number_of_repos = number_of_repos_span.text
            if number_of_repos == "":
                number_of_repos = 0
            else:
                number_of_repos = int(number_of_repos_span.text)
        else:
            number_of_repos = '0'
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
            global_rank = rank_div.ul.li.a.text
            country_rank = rank_div.ul.li.find_next('li').a.text
        else:
            global_rank = '0'
            country_rank = '0'
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

@api_view()
def leetcode(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    for record in serializer.data:
        stat = 0
        id = record['id']
        username = record['leetcode_username']
        content = requests.get(f"https://leetcode.com/{username}").text
        languages = ['C++', 'Python3', 'Java', 'C', 'C#']
        familiar_languages = 'languages - '
        for l in languages:
            if l in content:
                familiar_languages += f"{l}, "
        participated_in_contests = False
        global_ranking = 0
        rating = 0
        contests_count = 0
        data = {}
        try:
            cInd = content.index("attendedContestsCount", 220000)
        except:
            cInd = -1
        if cInd != -1:
            cSIndex = cInd+len("attendedContestsCount")+2
            cEIndex = cSIndex+3
            rSInd = content.index("rating", cInd)
            rEInd = content.index("globalRanking", cInd)
            comma = content.index(",", rEInd)
            participated_in_contests = True
            global_ranking = int(content[rEInd+15: comma])
            rating = int(content[rSInd + 8: rEInd-2])
            contests_count = int(content[cSIndex:cEIndex].replace('''"''', "").replace(',', ''))
        response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
        if response.status_code == 200:
            data = response.json()
            if data["status"] == 'error':
                familiar_languages = 'Invalid Username..'
        else:
            (hard, easy, medium, ranking) = (0, 0, 0, 0)
            try:
                i = content.index("acSubmissionNum", 280000)
            except:
                i = -1
            if i != -1:
                med = '''"Medium","count"'''
                har = '''"Hard","count"'''
                x = content.index(med, i)
                y = content.index(har, i)
                hSIndex = y+len(har)+1
                hEIndex = hSIndex+3
                mSIndex = x+len(med)+1
                mEIndex = mSIndex+3
                eSIndex = x - 18
                eEIndex = x - 15
            else:
                familiar_languages = 'Invalid Username..'
            try:
                rankEI = content.index("userAvatar", 200000)
            except:
                rankEI = -1
            if rankEI != -1:
                rankSI = content.index("ranking", rankEI-30)
                ranking = content[rankSI+9: rankEI-2]
            else:
                familiar_languages = 'Invalid Username .'
            medium = content[mSIndex:mEIndex].replace("}", "").replace(',', '')
            easy = content[eSIndex:eEIndex].replace("}", "").replace(',', '')
            hard = content[hSIndex:hEIndex].replace("}", "").replace("]", '')
            data = {
                'ranking': ranking,
                'easySolved': easy,
                'mediumSolved':medium,
                'hardSolved': hard,
            }
            
        result_data = {
                'general_rank': data['ranking'], 
                'easy': data['easySolved'],
                'medium': data['mediumSolved'],
                'hard': data['hardSolved'],
                'participated_in_contests': participated_in_contests,
                'contest_rank': global_ranking, 
                'number_of_contests': contests_count, 
                'contest_rating': rating, 
                'familiar_languages': familiar_languages[:-2],
                'student_id': id,
        }
        try:
            leetcode_details = LeetCodeDetail.objects.get(pk = id)
        except LeetCodeDetail.DoesNotExist:
            stat = 404
        if stat == 404: 
            seria = LeetCodeSerializer(data=result_data)
        else:
            seria = LeetCodeSerializer(leetcode_details, data=result_data)
        seria.is_valid(raise_exception=True)
        seria.save()
    return Response("Data is Scraped and Stored.")

class GitHubDetailList(ListAPIView):
    queryset = GitHubDetail.objects.all()
    serializer_class = GitHubSerializer

class CodeForcesDetailList(ListAPIView):
    queryset = CodeForcesDetail.objects.all()
    serializer_class = CodeForcesSerializer

class CodeChefDetailList(ListAPIView):
    queryset = CodeChefDetail.objects.all()
    serializer_class = CodeChefSerializer

class LeetCodeDetailList(ListAPIView):
    queryset = LeetCodeDetail.objects.all()
    serializer_class = LeetCodeSerializer

class GitHubDetails(RetrieveAPIView):
    queryset = GitHubDetail.objects.all()
    serializer_class = GitHubSerializer

class CodeForcesDetails(RetrieveAPIView):
    queryset = CodeForcesDetail.objects.all()
    serializer_class = CodeForcesSerializer

class CodeChefDetails(RetrieveAPIView):
    queryset = CodeChefDetail.objects.all()
    serializer_class = CodeChefSerializer

class LeetCodeDetails(RetrieveAPIView):
    queryset = LeetCodeDetail.objects.all()
    serializer_class = LeetCodeSerializer

