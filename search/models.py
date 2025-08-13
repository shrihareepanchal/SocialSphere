from django.db import models
from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from blog.models import Post


class SearchIndex(models.Model):
    """Model for tracking search analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.query} - {self.timestamp}"


# Elasticsearch Document for Posts
@registry.register_document
class PostDocument(Document):
    author = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
    })
    
    title = fields.TextField()
    content = fields.TextField()
    date_posted = fields.DateField()
    likes_count = fields.IntegerField(attr='total_likes')
    comments_count = fields.IntegerField(attr='comments.count')
    
    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Post
        fields = [
            'id',
        ]


# Elasticsearch Document for Users
@registry.register_document
class UserDocument(Document):
    username = fields.TextField()
    first_name = fields.TextField()
    last_name = fields.TextField()
    email = fields.TextField()
    date_joined = fields.DateField()
    
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = User
        fields = [
            'id',
        ]
