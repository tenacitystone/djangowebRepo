#from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Production, UserInfo
from django.shortcuts import render_to_response, HttpResponse
from django.template import loader, Context
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
import re

# Create your views here.

class Products(TemplateView):
    template_name = 'products.html'
    OPEN_PAGE_OF_DATA = 2
    startPos = 0
    endPos = OPEN_PAGE_OF_DATA

    def get(self, request, *args, **kwargs):
        page = 1
        if 'curPage' in request.GET or 'pageType' in request.GET:
            try:
                page = int(request.GET.get('curPage', 1))
                pageType = str(request.GET.get('pageType', ''))
            except ValueError:
                page = 1
                pageType = ''

            if pageType == 'Next':
                page += 1
            elif pageType == 'Previous':
                page -= 1

            self.startPos = (page - 1) * self.OPEN_PAGE_OF_DATA
            self.endPos = self.startPos + self.OPEN_PAGE_OF_DATA
        else:
            self.startPos = 0
            self.endPos = 3

        all_data_count = Production.objects.count()
        cur_page = page
        all_page = all_data_count / self.OPEN_PAGE_OF_DATA
        remain_data_count = all_data_count % self.OPEN_PAGE_OF_DATA
        if remain_data_count > 0:
            all_page += 1

        productArray = Production.objects.all()[self.startPos: self.endPos]
        template = loader.get_template(self.template_name)
        # 之前使用的是Context，但是运行完之后会报错需要改成dict
        context = dict({'productArray': productArray,
                           'all_page': all_page,
                           'cur_page': cur_page})
        return HttpResponse(template.render(context))

    '''def get_context_data(self, **kwargs):
        context = super(Products, self).get_context_data(**kwargs)
        context['productArray'] = Production.objects.all()[self.startPos: self.endPos]
        return context'''

class Home(TemplateView):
    template_name = 'home.html'

class ProductsCart(TemplateView):
    template_name = 'addToCart.html'

    def get(self, request, *args, **kwargs):
        pid = int(request.GET['pid'])
        print('pid', pid)
        template = loader.get_template(self.template_name)
        context = dict()
        return HttpResponse(template.render(context))

def search(request):
    #应该打开一个搜索页面
    error = False
    if 's_param' in request.GET:
        content = request.GET['s_param']
        if not content:
            error = True
        else:
            productArray = Production.objects.filter(pName__icontains=content)
            return render_to_response('products.html',
                                      {'productArray': productArray,
                                       'error': error
                                       })
    else:
        return render_to_response('products.html', {'error': error})

'''def make_hashers(request):
    content = 'text_content'
    from django.contrib.auth.hashers import make_password, check_password
    #make_password 每次生成的加密后的密码是不一样的所以需要将第二个参数设置一个固定值暂定django
    #pbkdf2_sha256是一种加密方式,unsalted_md5就是常见的md5加密，如果对加密哈希算法不是很了解，那么就使用django最新的哈希算法pbkdf2_sha256就好
    password = make_password(content, 'django', 'pbkdf2_sha256')
    result = check_password(content, password)
    print(result)'''

def login(request):
    error = []
    print("POST")
    print(request.POST)
    if 'username' in request.POST:
        username = request.POST['username']
        if len(username) <= 0:
            error.append("请输入用户名")
            return render_to_response('login.html', {'ErrorMessage': error})
        password1 = request.POST['password']
        if len(password1) <= 0:
            error.append("请输入密码")
            return render_to_response('login.html', {'ErrorMessage': error})

        password = make_password(password1, 'django', 'pbkdf2_sha256')

        tempUser = UserInfo.objects.filter(user_name=username)
        if len(tempUser) <= 0:
            print("database does not has this user")
            error.append("该用户不存在")
            return render_to_response('login.html', {'ErrorMessage': error})

        reslut = UserInfo.objects.filter(user_name=username, user_password=password)

        if len(reslut) > 0:
            user = UserInfo.objects.get(user_name=username)
            return render_to_response('home.html', {'user': user})
        else:
            error.append("请输入正确的密码")
            return render_to_response('login.html', {'ErrorMessage': error})
    else:
        return render_to_response('login.html', {'ErrorMessage': None})

def logout(request):
    return render_to_response('home.html', {'user': None})

def register(request):
    if 'username' in request.POST:
        username = request.POST['username']
        errors = []
        if username is not None:
            filterResult = UserInfo.objects.filter(user_name=username)
            if len(filterResult) > 0:
                return render_to_response('register.html', {"errors": "用户名已存在"})
            password1 = request.POST['password']
            password2 = request.POST['againpassword']
            if (password1 != password2):
                errors.append("两次输入的密码不一致!")
                return render_to_response('register.html', {'errors': errors})

            password1 = password2

            #使用正则表达式判断输入的手机号码
            phone = request.POST['phone']
            p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
            phonematch = p2.match(phone)
            if not phonematch:
                errors.append("请输入正确的手机号码!")
                return render_to_response('register.html', {'errors': errors})

            address = request.POST['address']

            password = make_password(password1, 'django', 'pbkdf2_sha256')
            print("password = " + password)
            # 将表单写入数据库
            user = UserInfo.objects.create(user_name=username,
                                           user_password=password,
                                           user_phone_number=phone,
                                           user_address=address)
            user.save()

            return render_to_response('home.html', {'user': user})
    else:
        return render_to_response('register.html', None)