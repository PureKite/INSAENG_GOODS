from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.views.generic import CreateView
import json

# Create your models here.
class Topic(models.Model):
    message = models.TextField(max_length=5000, null=True)
    subject = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now_add=True, null=True)
    writter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE, null=True)

class Reply(models.Model):
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.CASCADE)
    updated_at = models.DateField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    
class TestModel(models.Model):
    test_list = models.TextField(blank=False)
    
class AuthorForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = "__all__"
        
class Itemtest(CreateView):
    model = TestModel
    success_url = '/'
    template_name = 'board/shareboard.html'
    form_class = AuthorForm
    
    def get(self, request, *args, **kwargs):
        qs = TestModel.objects.all().last()
        result = json.loads(qs.test_list)
        ctx = {'result':result}
        return self.render_to_response(ctx)
    
    def form_valid(self, form):
        test = form.save(commit=False)
        test.test_list = json.dumps(self.request.POST.getlist('test_list'))
        test.save()
        return super().form_valid(form)

class Board(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)