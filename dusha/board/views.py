from allauth.account.views import SignupView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.urls import reverse

def index(request):
    print(request.user)
    return render(request, "board/index.html")
    # return HttpResponse("<h1>웹 메인 페이지 입니다.</h1>")

#비밀번호 변경시 인덱스 페이지로 리버스
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')


def question_list(request):
    #question_list = Question.objects.all()
    question_list = Question.objects.order_by('-create_date')
    context = { 'question_list': question_list }
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) # 데이터가 없으면 404 처리
    context = {'question' : question}
    return render(request, 'board/detail.html', context)

# 질문 등록
@login_required(login_url='common:login') # 로그인 페이지로 이동
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST) # 입력된 데이터가 있는 폼
        if form.is_valid(): # 폼이 유효성 검사를 통과했다면
            question = form.save(commit=False) #가저장
            question.author = request.user # 세션 권한(로그인한) 있는 글쓴이
            question.create_date = timezone.now()  #등록일 생성
            form.save() #진짜로 저장
            return redirect('board:question_list') # 질문 목록 페이지 이동

    else:  #get 방식
        form = QuestionForm()  #폼 객체 생성(빈 폼 생성)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)  # get 방식


def answer_create(request, question_id):
    # 답변 등록
    # question = Question.objects.get(id=question_id) #해당 id의 질문 객체 생성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)  # 입력값 전달받음
        if form.is_valid():
            answer = form.save(commit=False)  # 내용만 저장됨
            answer.create_date = timezone.now()  # 작성일
            answer.author = request.user  # 세션 발급
            answer.question = question  # 외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'board/detail.html', context)


# 질문수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


# 질문 삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('board:question_list')


# 답변 삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()





class SignupView(SignupView):
  def get_success_url(self): #어떤 폼이 성공적으로 처리되면 어디로 리디렉션할지 정해줌

    return reverse("/")