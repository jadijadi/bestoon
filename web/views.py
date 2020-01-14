# -*- coding: utf-8 -*-

from json import JSONEncoder
from datetime import datetime

from django.core import serializers
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST

from .models import User, Token, Expense, Income, Passwordresetcodes, News

# Create your views here.
from postmark import PMMail

from .utils import grecaptcha_verify, RateLimited

# create random string for Toekn
random_str = lambda N: ''.join(
    random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# login , (API) , returns : JSON = statuns (ok|error) and token



@csrf_exempt
def news(request):
    news = News.objects.all().order_by('-date')[:11]
    news_serialized = serializers.serialize("json", news)
    return JsonResponse(news_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def login(request):
    # check if POST objects has username and password
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        this_user = get_object_or_404(User, username=username)
        if (check_password(password, this_user.password)):  # authentication
            this_token = get_object_or_404(Token, user=this_user)
            token = this_token.token
            context = {}
            context['result'] = 'ok'
            context['token'] = token
            # return {'status':'ok','token':'TOKEN'}
            return JsonResponse(context, encoder=JSONEncoder)
        else:
            context = {}
            context['result'] = 'error'
            # return {'status':'error'}
            return JsonResponse(context, encoder=JSONEncoder)


# register (web)


def register(request):
    if 'requestcode' in request.POST:  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        # is this spam? check reCaptcha
        # if not grecaptcha_verify(request):  # captcha was not correct
        #     context = {
        #         'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'}  # TODO: forgot password
        #     return render(request, 'register.html', context)

        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            context = {
                'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = get_random_string(length=32)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes(
                email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            #message = PMMail(api_key=settings.POSTMARK_API_TOKEN,
            #                 subject="فعالسازی اکانت بستون",
            #                 sender="jadi@jadi.net",
            #                 to=email,
            #                 text_body=" برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: {}?code={}".format(
            #                     request.build_absolute_uri('/accounts/register/'), code),
            #                 tag="account request")
            #message.send()
            message = 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'
            message = 'قدیم ها ایمیل فعال سازی می فرستادیم ولی الان شرکتش ما رو تحریم کرده (: پس راحت و بی دردسر'
            body = " برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: <a href=\"{}?code={}\">لینک رو به رو</a> ".format(request.build_absolute_uri('/accounts/register/'), code)
            message = message + body
            context = {
                'message': message }
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET:  # user clicked on code
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(
                code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password,
                                          email=new_temp_user.email)
            this_token = get_random_string(length=48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            Passwordresetcodes.objects.filter(code=code).delete()
            context = {
                'message': 'اکانت شما ساخته شد. توکن شما {} است. آن را ذخیره کنید چون دیگر نمایش داده نخواهد شد! جدی!'.format(
                    this_token)}
            return render(request, 'index.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'register.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


# return username based on sent POST Token


@csrf_exempt
@require_POST
def whoami(request):
    if 'token' in request.POST:
        this_token = request.POST['token']  # TODO: Check if there is no `token`- done-please Check it
        # Check if there is a user with this token; will retun 404 instead.
        this_user = get_object_or_404(User, token__token=this_token)

        return JsonResponse({
            'user': this_user.username,
        }, encoder=JSONEncoder)  # return {'user':'USERNAME'}

    else:
        return JsonResponse({
            'message': 'لطفا token را نیز ارسال کنید .',
        }, encoder=JSONEncoder)  #


# return General Status of a user as Json (income,expense)





@csrf_exempt
@require_POST
def query_expenses(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    expenses = Expense.objects.filter(user=this_user).order_by('-date')[:num]
    expenses_serialized = serializers.serialize("json", expenses)
    return JsonResponse(expenses_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def query_incomes(request):
    this_token = request.POST['token']
    num = request.POST.get('num', 10)
    this_user = get_object_or_404(User, token__token=this_token)
    incomes = Income.objects.filter(user=this_user).order_by('-date')[:num]
    incomes_serialized = serializers.serialize("json", incomes)
    return JsonResponse(incomes_serialized, encoder=JSONEncoder, safe=False)


@csrf_exempt
@require_POST
def generalstat(request):
    # TODO: should get a valid duration (from - to), if not, use 1 month
    # TODO: is the token valid?
    this_token = request.POST['token']
    this_user = get_object_or_404(User, token__token=this_token)
    income = Income.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    expense = Expense.objects.filter(user=this_user).aggregate(
        Count('amount'), Sum('amount'))
    context = {}
    context['expense'] = expense
    context['income'] = income
    # return {'income':'INCOME','expanse':'EXPANSE'}
    return JsonResponse(context, encoder=JSONEncoder)


# homepage of System


def index(request):
    context = {}
    return render(request, 'index.html', context)



@csrf_exempt
@require_POST
def edit_expense(request):
    """edit an income"""
    print (request.POST)
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_pk = request.POST['id'] if 'id' in request.POST else "-1"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    this_expense = get_object_or_404(Expense, pk=this_pk, user=this_user)
    this_expense.text = this_text
    this_expense.amount = this_amount
    this_expense.save()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

@csrf_exempt
@require_POST
def edit_income(request):
    """ edit an income """
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_pk = request.POST['id'] if 'id' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    this_income = get_object_or_404(Income, pk=this_pk, user=this_user)
    this_income.text = this_text
    this_income.amount = this_amount
    this_income.save()

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

# submit an income to system (api) , input : token(POST) , output : status
# = (ok)

@csrf_exempt
@require_POST
def remove_expense(request):
    """ remove an expense """
    this_pk = request.POST['id'] if 'id' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    this_expense = get_object_or_404(Expense, pk=this_pk, user=this_user)
    this_expense.delete()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

# submit an income to system (api) , input : token(POST) , output : status
# = (ok)


@csrf_exempt
@require_POST
def remove_income(request):
    """ remove an income """
    this_pk = request.POST['id'] if 'id' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    this_income = get_object_or_404(Income, pk=this_pk, user=this_user)
    this_income.delete()
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)

# submit an income to system (api) , input : token(POST) , output : status
# = (ok)

@csrf_exempt
@require_POST
def submit_income(request):
    """ submit an income """

    # TODO: revise validation for the amount
    this_date = request.POST['date'] if 'date' in request.POST else timezone.now()
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    Income.objects.create(user=this_user, amount=this_amount,
                          text=this_text, date=this_date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


# submit an expanse to system (api) , input : token(POST) , output :
# status = (ok)
@csrf_exempt
@require_POST
def submit_expense(request):
    """ submit an expense """

    # TODO: revise validation for the amount
    this_date = request.POST['date'] if 'date' in request.POST else timezone.now()
    this_text = request.POST['text'] if 'text' in request.POST else ""
    this_amount = request.POST['amount'] if 'amount' in request.POST else "0"
    this_token = request.POST['token'] if 'token' in request.POST else ""
    this_user = get_object_or_404(User, token__token=this_token)

    Expense.objects.create(user=this_user, amount=this_amount,
                           text=this_text, date=this_date)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)  # return {'status':'ok'}
