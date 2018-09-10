from django.db import models
from django.contrib.auth.models import User


class Username(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    #about_me = models.CharField(max_length = 150)
    email = models.EmailField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

''''
class Posts(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    post = models.TextField(blank = True, default = '')
    def get_absolute_url(self):

        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        
        String for representing the Model object.
        
        return self.title
'''