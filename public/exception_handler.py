from django.middleware.common import CommonMiddleware
from .exceptions import UnauthorizedUser
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse , HttpResponseRedirect



class ExceptionHandler(CommonMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            return view_func(request, *view_args, **view_kwargs)
        except UnauthorizedUser as error:
            messages.info(request, error.message)
            # response = HttpResponseRedirect('http://localhost:8000/login')
            response = HttpResponseRedirect('/login')
            response.delete_cookie("at")
            response.delete_cookie("user")
            return response

