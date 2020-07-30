
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, SentimentForm
from .models import Sentiment

from .code.translate import translate_text
from .code.clean_text1 import clean_text1
from .code.main import getPickleResult, getSentimentResult, getSentiment

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form' : form})


@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('home')

	else:
		form = UserUpdateForm(instance=request.user)

	return render(request, 'user/profile.html', {'form': form})

def team(request):
    return render(request, 'user/team.html')

def docs(request):
    return render(request, 'user/docs.html')

def hwdi(request):
    return render(request, 'user/hwdi.html')

def faq(request):
    return render(request, 'user/faq.html')

@login_required
def home(request):
    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']    # Result from form in UI
            
            translated_text = translate_text(text)  # Result from Translate.py

            result_text = clean_text1(translated_text)  # Result from clean_text1.py
            pickle_text = getPickleResult(result_text)  # Result from pickle file
            result_arr = getSentimentResult(pickle_text)    # Result from h5 file

            pie_arr = result_arr[0]
            print(pie_arr)


            negative_val = pie_arr[0] * 100
            neutral_val = pie_arr[1] * 100
            positive_val = pie_arr[2] * 100

            result = getSentiment(result_arr)

            username = request.user.username    # Get the username of current user

            s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username)
            s.save()

            form = SentimentForm()
    else:
        form = SentimentForm()
        result = ''
        positive_val = 1
        neutral_val = 1
        negative_val = 1
    
    return render(request, 'user/home.html', {'form': form,
        'result': result,
        'positive_val': positive_val,
        'neutral_val': neutral_val,
        'negative_val': negative_val,
        })

@login_required
def history(request):
    data = Sentiment.objects.all().filter(username = request.user.username)


    return render(request, 'user/history.html', {'data': data})
