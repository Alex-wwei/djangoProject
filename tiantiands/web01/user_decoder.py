from django.http import HttpResponseRedirect

def user(func):
    def filterFun(request, *args, **avg):
        if request.session.get('user_name', ''):
            return func(request, *args, **avg)
        else:
            req = HttpResponseRedirect('/user/login/')
            url = request.get_full_path()
            req.set_cookie('url', url)
            return  req
    return filterFun