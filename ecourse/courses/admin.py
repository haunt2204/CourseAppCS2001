from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Course, User, Tag

# Register your models here.
class CourseTagInlineAdmin(admin.TabularInline):
    model = Course.tags.through

class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    search_fields = ['subject']
    list_filter = ['id', 'subject']
    readonly_fields = ['ava']
    form = CourseForm
    inlines = [CourseTagInlineAdmin]
    def ava(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(User)
admin.site.register(Tag)