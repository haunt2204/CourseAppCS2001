from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Category

# Create your views here.
class CategoryView(View):

    def get(self, request):
        cats = Category.objects.all()
        return render(request, 'courses/list.html', {
            'categories': cats
        })

    def post(self, request):
        pass

def index(request):
    return HttpResponse('HELLO CS2001')

def list(request, course_id):
    return HttpResponse(f'COURSE {course_id}')
