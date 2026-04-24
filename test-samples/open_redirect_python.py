from flask import redirect
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect


def vulnerable(user_url):
    redirect(user_url)
    HttpResponseRedirect(user_url)
    HttpResponsePermanentRedirect(user_url)

def false_negative_expansion_redirect_python(user_url, self):
    RedirectResponse(user_url)
    web.HTTPFound(user_url)
    self.redirect(user_url)
