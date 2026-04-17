from flask import redirect
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect


def vulnerable(user_url):
    redirect(user_url)
    HttpResponseRedirect(user_url)
    HttpResponsePermanentRedirect(user_url)
