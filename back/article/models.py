from django.db import models
from accounts.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    img_path = models.TextField(null=True, blank=True)
    like_users = models.ManyToManyField(User, related_name="like_article",blank=True)
    view_count = models.IntegerField(default=0)  # 조회수 필드 추가

    def __str__(self):
        return self.title
    #좋아요 갯수
    @property
    def like_count(self):
        return self.like_users.count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return self.content


