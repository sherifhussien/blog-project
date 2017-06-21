from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    #auth.User to refer a Model defined in another app
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    published_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)  # related_name=comments

    def get_absolute_url(self): # after someone create a comment where should the website take him
        return reverse('post_detail',kwargs={'pk':self.pk})  #will go to post_detail page for the pk of the post just created

    def __str__(self):
        return self.title

class Comment(models.Model):
    #related name is used to be able to reference it in the Post Model
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post_list')

    def approve(self):
        approved_comment=True
        self.save()

    def __str__(self):
        return self.text
