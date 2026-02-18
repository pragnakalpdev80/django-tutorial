from django.db.models import F
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice, Voter
from django.template import loader
from django.http import Http404,request
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

@login_required
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = "/polls/login/"
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(LoginRequiredMixin,generic.DetailView):
    login_url = "/polls/login/"
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class VoteView(View):
    
    def post(self,request,question_id):
        question = get_object_or_404(Question, pk=question_id)
        # print(question_id)
        voters=[users.users_id for users in Voter.objects.filter(question_id=question_id)]
        # print(f"Voters: {voters}")
        # print(f"user id: {request.user.id}")
        if request.user.id in voters:
            voted_choice=[users.choice_id for users in Voter.objects.filter(question_id=question_id)]
            choice=[choice.choice_text for choice in Choice.objects.filter(id=voted_choice[0])]
            
            return render(request, 'polls/detail.html', {
            "question": question,
            'error_message': f"Sorry, but you have already voted to '{choice[0]}'."
            })
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            v = Voter(users_id=request.user.id, question=question,choice=selected_choice)
            v.save()
            return HttpResponseRedirect(reverse("polls:results", args=(question.pk,)))
 

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class LoginView(LoginView):
    template_name = 'polls/login.html'
    def get(self, request):
        form= LoginForm()
        return render(request, self.template_name, { 'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            messages.error(request,"Username or Password not matched")
            return redirect('/polls/login/')
        login(request,user)
        return redirect("/polls/")
    

class LogoutView(View):
    def post(self,request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/polls/login/')
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(username=username, password=password)
#         print(user)
#         if user is None:
#             messages.error(request,"Username or Password not matched")
#             return redirect('/polls/login/')
#         return redirect("/polls/")
#     return render(request, 'registration/login.html')

class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/polls/")
        form = RegistrationForm()
        return render(request, 'polls/register.html', { 'form': form})  
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/polls/login/')        
        messages.info(request, "Account created Successfully!")
    
# def register(request):
#     if request.user.is_authenticated:
#         return redirect("/polls/")
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         print(first_name)
#         last_name = request.POST.get('last_name')
#         print(last_name)
#         username = request.POST.get('username')
#         print(username)
#         email = request.POST.get('email')
#         print(email)
#         password = request.POST.get('password')
#         print(password)
#         cpassword = request.POST.get('cpassword')
#         print(password)
        
#         user = User.objects.filter(username=username)
        
#         if user.exists():
#             messages.info(request, "Username already taken!")
#             return redirect('/polls/register/')
#         if not password==cpassword:
#             print("pass not matched")
#             messages.error(request,"Password not matched")
#             return redirect('/polls/register/')
        
#         user = User.objects.create_user(
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#             email=email
#         )   
        
#         print("user register")
#         user.set_password(password)
#         user.save()        
#         messages.info(request, "Account created Successfully!")
#     return render(request, "polls/register_function.html")
