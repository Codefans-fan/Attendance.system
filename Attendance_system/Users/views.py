from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout  
from django.template.response import TemplateResponse
import time


from django.contrib.auth import REDIRECT_FIELD_NAME

# Create your views here.
def login(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            # login success
            user_login(req, form.get_user())
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm(req)
    context = {
        'form':form,
        'errors':form.errors.get('__all__','')
        }
    return render(req, 'login.html', context)

def redirect_to_login(next, login_url=None,
                      redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, passing the given 'next' page
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))