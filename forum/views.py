from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
@login_required
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/question_list.html', {'questions': questions})

@login_required
def forum_home(request):
    if not request.user.is_verified:
        return redirect('users:verify_otp')
    return redirect('question_list')  # redirect to main forum view


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('forum:question_list')
    else:
        form = QuestionForm()
    return render(request, 'forum/ask_question.html', {'form': form})
@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('forum:question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'forum/question_detail.html', {'question': question, 'form': form})


# Create your views here.
