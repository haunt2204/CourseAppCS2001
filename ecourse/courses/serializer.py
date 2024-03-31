from .models import Category, Course, Lesson, Tag, User, Comment
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/static/%s" % obj.image.name

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'description', 'created_date', 'updated_date', 'image', 'tags']

class LessonSerializeDetail(LessonSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return lesson.like_set.filter(liked=True, user=request.user).exists()

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['liked']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'avatar']

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']