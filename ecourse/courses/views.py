from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Course, Lesson, Tag, User, Comment, Like
from rest_framework import viewsets, generics, status, permissions, parsers
from .serializer import CategorySerializer, CourseSerializer, LessonSerializer, UserSerializer, CommentSerializer, LessonSerializeDetail
from .paginator import CoursePaginator
from . import perms


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
    serializer_class = LessonSerializeDetail
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post'], url_path="comments", detail=True)
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, lesson = self.get_object(), content=request.data.get('content'))
        comment.save()

        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        like,create = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not create:
            like.liked = not like.liked
            like.save()

        return Response(LessonSerializeDetail(self.get_object(),context={
            "request": request
        }).data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    def get_permissions(self):
        if self.action in ['get_current']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user, context={
            "request": request
        }).data, status=status.HTTP_200_OK)



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

class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [perms.OwnerPermission]
