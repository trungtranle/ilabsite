from django.shortcuts import render
from main.forms import ContactForm
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request = request, level= messages.SUCCESS, message= 'Chúng tôi đã nhận được thông tin của bạn. Chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất!')
            return HttpResponseRedirect("/")
        else:
            print(form.errors)
    else:
        form = ContactForm()

        return render(request, 'index.html', {'form':form})
