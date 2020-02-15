from django.contrib.auth import  login,logout,authenticate
from django.views.decorators.http import  require_POST
from    .forms import LoginForm,RegisterForm
from  django.http import  JsonResponse
from utils import restful
from django.shortcuts import redirect,reverse
#一般这样设计api
#{'code':200,"message":"","data":{}}
from utils.captcha.xfzcaptcha import  Captcha
from io import  BytesIO
from    django.http import HttpResponse
from utils.aliyunsdk import  aliyunsms
from utils import restful
from  django.core.cache import  cache
from django.contrib.auth import  get_user_model
User = get_user_model()
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        print(password)
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username = telephone,password = password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()#返回json数据
            else:
                return restful.unauth_error(message="您的账号已经被冻结")
        else:
            return  restful.params_error(message="手机号或者密码错误")
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))#重定向





@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.object.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())



def img_captcha(request):
    text,image = Captcha.gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type = 'image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)

    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    print(code)
    cache.set(telephone, code, 5 * 60)
    #result = aliyunsms.send_sms(telephone,code)
    #print(result)
    print('短信验证码'+code)

    return restful.ok()


def cache_test(request):
    cache.set('username','zpc',60)
    resutl = cache.get('username')
    print(resutl)
    return  HttpResponse('success')