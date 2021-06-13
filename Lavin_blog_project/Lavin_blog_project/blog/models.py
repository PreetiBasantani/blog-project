from django.contrib import auth
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    category_list = [
        ('Lifestyle','Lifestyle'),
        ('Health','Health'),
        ('Recipes','Recipes'),
        ('Travel','Travel'),
        ('Music','Music'),
        ('Products','Products'),
    ]
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='media/')
    post_title = models.CharField(max_length=256)
    text = models.TextField()
    category = models.CharField(max_length=40, choices=category_list)
    created_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.post_title

    def publish(self):
        self.published_on = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'pk': self.pk})

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=256)
    comment_text = models.TextField()
    create_date = models.DateTimeField(auto_now=True)
    approved_comments = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_text

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list')