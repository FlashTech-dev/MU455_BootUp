
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, SentimentForm, FileForm, TextForm
from .models import Sentiment

import os
import threading
import concurrent.futures
import pandas as pd

import re


from pathlib import Path

from .code.translate import translate_text
from .code.clean_text1 import clean_text1
from .code.main import getPickleResult, getSentimentResult, getSentiment, punctuation, clean_text, get_pickle_result, get_sentiment

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

# class myThread (threading.Thread):
#     def __init__(self, threadID, name, text, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.text = text
#         self.counter = counter
#     def run(self):
#         print("Starting " + self.name)
#         # print_time(self.name, 5, self.counter)
#         if self.counter == 1:
#             model1(self.text)
#         else:
#             model2(self.text)
#         print("Exiting " + self.name)

def model1(text, username):
    print("Thread 1")
    # translated_text = translate_text(text)  # Result from Translate.py

    result_text = clean_text1(text)  # Result from clean_text1.py
    pickle_text = getPickleResult(result_text)  # Result from pickle file
    result_arr = getSentimentResult(pickle_text)    # Result from h5 file

    pie_arr = result_arr[0]

    result = getSentiment(pie_arr[0])


    s = Sentiment(text=text, translated_text=text, sentiment=result, username=username)
    s.save()
    # print(pie_arr)
    return pie_arr

def model2(text):
    print("Thread 2")
    translated_text = translate_text(text)  # Result from Translate.py

    punc_text = punctuation(translated_text)
    pic_text = get_pickle_result(punc_text)
    result2 = get_sentiment(pic_text)
    return result2

# @login_required
# def home(request):
#     if request.method == 'POST':
#         form = SentimentForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']    # Result from form in UI
            
#             # translated_text = translate_text(text)  # Result from Translate.py

#             # result_text = clean_text1(translated_text)  # Result from clean_text1.py
#             # pickle_text = getPickleResult(result_text)  # Result from pickle file
#             # result_arr = getSentimentResult(pickle_text)    # Result from h5 file

#             # pie_arr = result_arr[0]
#             # print(pie_arr)

#             # threadLock = threading.Lock()
#             # que = Queue.Queue()
#             # threads = []

#             # Create new threads
#             # thread1 = myThread(1, "Thread-1", text,   1)
#             # thread2 = myThread(2, "Thread-2", text,  2)
#             # thread1 = threading.Thread(target=model1, args=(text))
#             # thread2 = threading.Thread(target=model2, args=(text))

#             # Start new Threads
#             # thread1.start()
#             # thread2.start()

#             # Add threads to thread list
#             # threads.append(thread1)
#             # threads.append(thread2)

#             # Wait for all threads to complete
#             # for t in threads:
#                 # t.join()
#             # pie_arr = thread1.join()
#             # result2 = thread2.join()

#             username = request.user.username    # Get the username of current user
#             # result = getSentiment(pie_arr[0])

#             # s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username)
#             # s.save()





#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 future = executor.submit(model1, text, username)
#                 pie_arr = future.result()
#                 print(pie_arr)
#                 future = executor.submit(model2, text)
#                 result2 = future.result()
#                 print(result2)

#             negative_val = pie_arr[0] * 100
#             neutral_val = pie_arr[1] * 100
#             positive_val = pie_arr[2] * 100

#             result = getSentiment(pie_arr)



            

#             # 2nd Model
#             # punc_text = punctuation(translated_text)
#             # pic_text = get_pickle_result(punc_text)
#             # result2 = get_sentiment(pic_text)

#             # print(result2)

#             empty_val = result2.loc[0, "percentage"]
#             sadness_val = result2.loc[1, "percentage"]
#             enthusiasm_val = result2.loc[2, "percentage"]
#             neutral_val1 = result2.loc[3, "percentage"]
#             worry_val = result2.loc[4, "percentage"]
#             surprise_val = result2.loc[5, "percentage"]
#             love_val = result2.loc[6, "percentage"]
#             fun_val = result2.loc[7, "percentage"]
#             hate_val = result2.loc[8, "percentage"]
#             happiness_val = result2.loc[9, "percentage"]
#             boredom_val = result2.loc[10, "percentage"]
#             relief_val = result2.loc[11, "percentage"]
#             anger_val = result2.loc[12, "percentage"]

#             # form = SentimentForm()


#     else:
#         form = SentimentForm()
#         result = ''
#         positive_val = 1
#         neutral_val = 1
#         negative_val = 1
#         empty_val = 1
#         sadness_val = 1
#         enthusiasm_val = 1
#         neutral_val1 = 1
#         worry_val = 1
#         surprise_val = 1
#         love_val = 1
#         fun_val = 1
#         hate_val = 1
#         happiness_val = 1
#         boredom_val = 1
#         relief_val = 1
#         anger_val = 1
    
#     return render(request, 'user/home.html', {'form': form,
#         'result': result,
#         'positive_val': positive_val,
#         'neutral_val': neutral_val,
#         'negative_val': negative_val,
#         'empty_val': empty_val,
#         'sadness_val': sadness_val,
#         'enthusiasm_val': enthusiasm_val,
#         'neutral_val1': neutral_val1,
#         'worry_val': worry_val,
#         'surprise_val': surprise_val,
#         'love_val': love_val,
#         'fun_val': fun_val,
#         'hate_val': hate_val,
#         'happiness_val': happiness_val,
#         'boredom_val': boredom_val,
#         'relief_val': relief_val,
#         'anger_val': anger_val,
#         })


    # if request.method == 'POST' and request.method == 'FILES':
    #     form = SentimentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         value = form.cleaned_data['value']
    #         print(value)
    #         newdoc = Sentiment(docfile = request.FILES['docfile'])
    #         newdoc.save()

    #         print("File Path:", Path(__file__).absolute())
    #         print("Directory Path:", Path().absolute())  
    #         print(newdoc.docfile.url)

    #         ABS_PATH = Path().absolute()
    #         FILE_PATH = newdoc.docfile.url

    #         BASE_DIR = f'{ABS_PATH}{FILE_PATH}'
    #         print(BASE_DIR)

    #         with open(BASE_DIR, 'r') as f:
    #             text = f.read().replace('\n', '')

    #             translated_text = translate_text(text)  # Result from Translate.py

    #             result_text = clean_text1(translated_text)  # Result from clean_text1.py
    #             pickle_text = getPickleResult(result_text)  # Result from pickle file
    #             result_arr = getSentimentResult(pickle_text)    # Result from h5 file

    #             pie_arr = result_arr[0]
    #             print(pie_arr)

    #             negative_val = pie_arr[0] * 100
    #             neutral_val = pie_arr[1] * 100
    #             positive_val = pie_arr[2] * 100

    #             result = getSentiment(result_arr)

    #             username = request.user.username    # Get the username of current user

    #             # Save the data to DB
    #             s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username)
    #             s.save()

    #             # 2nd Model
    #             punc_text = punctuation(translated_text)
    #             pic_text = get_pickle_result(punc_text)
    #             result2 = get_sentiment(pic_text)

    #             print(result2)

    #             empty_val = result2.loc[0, "percentage"]
    #             sadness_val = result2.loc[1, "percentage"]
    #             enthusiasm_val = result2.loc[2, "percentage"]
    #             neutral_val1 = result2.loc[3, "percentage"]
    #             worry_val = result2.loc[4, "percentage"]
    #             surprise_val = result2.loc[5, "percentage"]
    #             love_val = result2.loc[6, "percentage"]
    #             fun_val = result2.loc[7, "percentage"]
    #             hate_val = result2.loc[8, "percentage"]
    #             happiness_val = result2.loc[9, "percentage"]
    #             boredom_val = result2.loc[10, "percentage"]
    #             relief_val = result2.loc[11, "percentage"]
    #             anger_val = result2.loc[12, "percentage"]

    #             return render(request, 'user/home.html', {'form': form,
    #                 'result': result,
    #                 'positive_val': positive_val,
    #                 'neutral_val': neutral_val,
    #                 'negative_val': negative_val,
    #                 'empty_val': empty_val,
    #                 'sadness_val': sadness_val,
    #                 'enthusiasm_val': enthusiasm_val,
    #                 'neutral_val1': neutral_val1,
    #                 'worry_val': worry_val,
    #                 'surprise_val': surprise_val,
    #                 'love_val': love_val,
    #                 'fun_val': fun_val,
    #                 'hate_val': hate_val,
    #                 'happiness_val': happiness_val,
    #                 'boredom_val': boredom_val,
    #                 'relief_val': relief_val,
    #                 'anger_val': anger_val,
    #                 })



    # elif request.method == 'POST':
    #     form = SentimentForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']    # Result from form in UI
            
    #         translated_text = translate_text(text)  # Result from Translate.py

    #         result_text = clean_text1(translated_text)  # Result from clean_text1.py
    #         pickle_text = getPickleResult(result_text)  # Result from pickle file
    #         result_arr = getSentimentResult(pickle_text)    # Result from h5 file

    #         pie_arr = result_arr[0]
    #         print(pie_arr)

    #         negative_val = pie_arr[0] * 100
    #         neutral_val = pie_arr[1] * 100
    #         positive_val = pie_arr[2] * 100

    #         result = getSentiment(result_arr)

    #         username = request.user.username    # Get the username of current user

    #         # Save the data to DB
    #         s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username, docfile='')
    #         s.save()


    #         # 2nd Model
    #         punc_text = punctuation(translated_text)
    #         pic_text = get_pickle_result(punc_text)
    #         result2 = get_sentiment(pic_text)

    #         print(result2)

    #         empty_val = result2.loc[0, "percentage"]
    #         sadness_val = result2.loc[1, "percentage"]
    #         enthusiasm_val = result2.loc[2, "percentage"]
    #         neutral_val1 = result2.loc[3, "percentage"]
    #         worry_val = result2.loc[4, "percentage"]
    #         surprise_val = result2.loc[5, "percentage"]
    #         love_val = result2.loc[6, "percentage"]
    #         fun_val = result2.loc[7, "percentage"]
    #         hate_val = result2.loc[8, "percentage"]
    #         happiness_val = result2.loc[9, "percentage"]
    #         boredom_val = result2.loc[10, "percentage"]
    #         relief_val = result2.loc[11, "percentage"]
    #         anger_val = result2.loc[12, "percentage"]

    #         return render(request, 'user/home.html', {'form': form,
    #             'result': result,
    #             'positive_val': positive_val,
    #             'neutral_val': neutral_val,
    #             'negative_val': negative_val,
    #             'empty_val': empty_val,
    #             'sadness_val': sadness_val,
    #             'enthusiasm_val': enthusiasm_val,
    #             'neutral_val1': neutral_val1,
    #             'worry_val': worry_val,
    #             'surprise_val': surprise_val,
    #             'love_val': love_val,
    #             'fun_val': fun_val,
    #             'hate_val': hate_val,
    #             'happiness_val': happiness_val,
    #             'boredom_val': boredom_val,
    #             'relief_val': relief_val,
    #             'anger_val': anger_val,
    #             })

            # form = SentimentForm()

    
    
    



@login_required
def history(request):
    data = Sentiment.objects.all().filter(username = request.user.username)

    return render(request, 'user/history.html', {'data': data})

@login_required
def home_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            output_url = ''
            newdoc = Sentiment(docfile = request.FILES['docfile'])
            newdoc.save()

            print("File Path:", Path(__file__).absolute())
            print("Directory Path:", Path().absolute())  
            print(newdoc.docfile.url)

            ABS_PATH = Path().absolute()
            FILE_PATH = newdoc.docfile.url

            BASE_DIR = f'{ABS_PATH}{FILE_PATH}'
            print(BASE_DIR)

            print(BASE_DIR + 'abc')

            username = request.user.username    # Get the username of current user

            if re.search('.csv', BASE_DIR): 
                

                data = pd.read_csv(BASE_DIR, encoding='unicode_escape')
                data = data.sample(frac = 1).reset_index(drop=True)
                print(data.shape)
                data.head()

                text_arr = pd.DataFrame(data)
                print(text_arr)
                print(len(text_arr))

                # writer = pd.ExcelWriter('output-2.xlsx', engine='xlsxwriter')
                # writer.save()
                columns = ['text', 'output']
                # index = 5
                df = pd.DataFrame(columns=columns)
                df = df.fillna(0)

                for index, row in text_arr.iterrows():
                    # translated_text = translate_text(row['module output'])  # Result from Translate.py

                    result_text = clean_text1(row['module output'])  # Result from clean_text1.py
                    pickle_text = getPickleResult(result_text)  # Result from pickle file
                    result_arr = getSentimentResult(pickle_text)    # Result from h5 file

                    pie_arr = result_arr[0]

                    result = getSentiment(pie_arr)

                    df.loc[index] = [row['module output']] + [result]
                print(df)

                df.to_csv('output-result.csv')
                # df.to_excel(writer, sheet_name='Sheet1', index=False)
                # writer.save()

                output_url = 'output-result-final.csv'

            
                
                


    #         with open(BASE_DIR, 'r') as f:
    #             text = f.read().replace('\n', '')

    #             translated_text = translate_text(text)  # Result from Translate.py

    #             result_text = clean_text1(translated_text)  # Result from clean_text1.py
    #             pickle_text = getPickleResult(result_text)  # Result from pickle file
    #             result_arr = getSentimentResult(pickle_text)    # Result from h5 file

    #             pie_arr = result_arr[0]
    #             print(pie_arr)

    #             negative_val = pie_arr[0] * 100
    #             neutral_val = pie_arr[1] * 100
    #             positive_val = pie_arr[2] * 100

    #             result = getSentiment(result_arr)

    #             username = request.user.username    # Get the username of current user

    #             # Save the data to DB
    #             s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username)
    #             s.save()

    #             # 2nd Model
    #             punc_text = punctuation(translated_text)
    #             pic_text = get_pickle_result(punc_text)
    #             result2 = get_sentiment(pic_text)

    #             print(result2)

    #             empty_val = result2.loc[0, "percentage"]
    #             sadness_val = result2.loc[1, "percentage"]
    #             enthusiasm_val = result2.loc[2, "percentage"]
    #             neutral_val1 = result2.loc[3, "percentage"]
    #             worry_val = result2.loc[4, "percentage"]
    #             surprise_val = result2.loc[5, "percentage"]
    #             love_val = result2.loc[6, "percentage"]
    #             fun_val = result2.loc[7, "percentage"]
    #             hate_val = result2.loc[8, "percentage"]
    #             happiness_val = result2.loc[9, "percentage"]
    #             boredom_val = result2.loc[10, "percentage"]
    #             relief_val = result2.loc[11, "percentage"]
    #             anger_val = result2.loc[12, "percentage"]

    else:
        form = FileForm()
        output_url = ''
    #     result = ''
    #     positive_val = 1
    #     neutral_val = 1
    #     negative_val = 1
    #     empty_val = 1
    #     sadness_val = 1
    #     enthusiasm_val = 1
    #     neutral_val1 = 1
    #     worry_val = 1
    #     surprise_val = 1
    #     love_val = 1
    #     fun_val = 1
    #     hate_val = 1
    #     happiness_val = 1
    #     boredom_val = 1
    #     relief_val = 1
        # anger_val = 1

    return render(request, 'user/home-file.html', {'form': form,
            'output_url': output_url,
        # 'result': result,
        # 'positive_val': positive_val,
        # 'neutral_val': neutral_val,
        # 'negative_val': negative_val,
        # 'empty_val': empty_val,
        # 'sadness_val': sadness_val,
        # 'enthusiasm_val': enthusiasm_val,
        # 'neutral_val1': neutral_val1,
        # 'worry_val': worry_val,
        # 'surprise_val': surprise_val,
        # 'love_val': love_val,
        # 'fun_val': fun_val,
        # 'hate_val': hate_val,
        # 'happiness_val': happiness_val,
        # 'boredom_val': boredom_val,
        # 'relief_val': relief_val,
        # 'anger_val': anger_val,
        })

@login_required
def home_text(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']    # Result from form in UI
            
            # translated_text = translate_text(text)  # Result from Translate.py

            # result_text = clean_text1(translated_text)  # Result from clean_text1.py
            # pickle_text = getPickleResult(result_text)  # Result from pickle file
            # result_arr = getSentimentResult(pickle_text)    # Result from h5 file

            # pie_arr = result_arr[0]
            # print(pie_arr)

            # threadLock = threading.Lock()
            # que = Queue.Queue()
            # threads = []

            # Create new threads
            # thread1 = myThread(1, "Thread-1", text,   1)
            # thread2 = myThread(2, "Thread-2", text,  2)
            # thread1 = threading.Thread(target=model1, args=(text))
            # thread2 = threading.Thread(target=model2, args=(text))

            # Start new Threads
            # thread1.start()
            # thread2.start()

            # Add threads to thread list
            # threads.append(thread1)
            # threads.append(thread2)

            # Wait for all threads to complete
            # for t in threads:
                # t.join()
            # pie_arr = thread1.join()
            # result2 = thread2.join()

            username = request.user.username    # Get the username of current user
            # result = getSentiment(pie_arr[0])

            # s = Sentiment(text=text, translated_text=translated_text, sentiment=result, username=username)
            # s.save()





            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(model1, text, username)
                pie_arr = future.result()
                print(pie_arr)
                future = executor.submit(model2, text)
                result2 = future.result()
                print(result2)

            negative_val = pie_arr[0] * 100
            neutral_val = pie_arr[1] * 100
            positive_val = pie_arr[2] * 100

            result = getSentiment(pie_arr)



            

            # 2nd Model
            # punc_text = punctuation(translated_text)
            # pic_text = get_pickle_result(punc_text)
            # result2 = get_sentiment(pic_text)

            # print(result2)

            empty_val = result2.loc[0, "percentage"]
            sadness_val = result2.loc[1, "percentage"]
            enthusiasm_val = result2.loc[2, "percentage"]
            neutral_val1 = result2.loc[3, "percentage"]
            worry_val = result2.loc[4, "percentage"]
            surprise_val = result2.loc[5, "percentage"]
            love_val = result2.loc[6, "percentage"]
            fun_val = result2.loc[7, "percentage"]
            hate_val = result2.loc[8, "percentage"]
            happiness_val = result2.loc[9, "percentage"]
            boredom_val = result2.loc[10, "percentage"]
            relief_val = result2.loc[11, "percentage"]
            anger_val = result2.loc[12, "percentage"]

    else:
        form = TextForm()
        result = ''
        positive_val = 1
        neutral_val = 1
        negative_val = 1
        empty_val = 1
        sadness_val = 1
        enthusiasm_val = 1
        neutral_val1 = 1
        worry_val = 1
        surprise_val = 1
        love_val = 1
        fun_val = 1
        hate_val = 1
        happiness_val = 1
        boredom_val = 1
        relief_val = 1
        anger_val = 1

    return render(request, 'user/home-text.html', {'form': form,
        'result': result,
        'positive_val': positive_val,
        'neutral_val': neutral_val,
        'negative_val': negative_val,
        'empty_val': empty_val,
        'sadness_val': sadness_val,
        'enthusiasm_val': enthusiasm_val,
        'neutral_val1': neutral_val1,
        'worry_val': worry_val,
        'surprise_val': surprise_val,
        'love_val': love_val,
        'fun_val': fun_val,
        'hate_val': hate_val,
        'happiness_val': happiness_val,
        'boredom_val': boredom_val,
        'relief_val': relief_val,
        'anger_val': anger_val,
        })