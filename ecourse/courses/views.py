from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Course, Lesson, Tag, User
from rest_framework import viewsets, generics, status, permissions
from .serializer import CategorySerializer, CourseSerializer, LessonSerializer, UserSerializer
from .paginator import CoursePaginator


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(subject__icontains=q)
        return queries

    @action(methods=['get'],detail=True)
    def lessons(self, request, pk):
        l = self.get_object().lesson_set.all()
        return Response(LessonSerializer(l, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)

class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



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
