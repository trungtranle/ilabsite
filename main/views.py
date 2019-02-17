from django.shortcuts import render
from main.forms import ContactForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from main.models import Test, TestCategory
from blog.models import BlogPage, HomePage
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
    blog_post = BlogPage.objects.order_by("-date").live()
    
    recent_blog_post = blog_post[len(blog_post)-3 : len(blog_post)]
    print(recent_blog_post)
    #print(recent_blog_post)
    return render(request,'index.html',{'form':form, 'blog':recent_blog_post})

def category_detail(request, category_slug = None):
    category = TestCategory.objects.get(slug = category_slug).pk
    tests = Test.objects.filter(category = category, publish = True)
    category_name = TestCategory.objects.get(pk = category)
    return render(request, 'category_detail.html', {'tests':tests, 'category_name':category_name})

def test_detail(request, test_slug = None):
    test = Test.objects.get(slug = test_slug)

    return render(request, 'test_detail.html', {'test': test})

def all_services(request):
    tests = Test.objects.filter(publish = True)
    if request.method == "GET":
        if request.GET.get('sortby') == 'A-Z':
            tests = Test.objects.filter(publish = True).order_by('name')
        if request.GET.get('sortby') == 'Nhóm':
            tests = Test.objects.filter(publish = True).order_by('category')

    return render(request, 'all_services.html', {'tests':tests})
