from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Comment
from users.models import Profile
from friend.models import FriendRequest, FriendList
from chat.models import Room, Chat
from notification.models import Notification


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'profile_pic']
        read_only_fields = ['id', 'date_joined']
    
    def get_profile_pic(self, obj):
        try:
            return obj.profile.image.url
        except:
            return None


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'image', 'favorites']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'author', 'likes_count', 'comments_count', 'is_liked']
        read_only_fields = ['id', 'date_posted', 'author']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, source='name')
    content = serializers.CharField(source='body')
    date_posted = serializers.DateTimeField(source='date_added', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'date_posted']
        read_only_fields = ['id', 'date_posted', 'author']


## Removed LikeSerializer because likes are a ManyToMany relation on Post


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'is_active', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class FriendListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friends = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = FriendList
        fields = ['id', 'user', 'friends']


class ChatSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'room_id', 'author', 'friend', 'text', 'date', 'has_seen']
        read_only_fields = ['id', 'date']


class RoomSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = ['id', 'author', 'friend', 'created', 'last_message']
        read_only_fields = ['id', 'created']
    
    def get_last_message(self, obj):
        last_chat = obj.chats.last()
        if last_chat:
            return {
                'text': last_chat.text,
                'date': last_chat.date,
                'author': last_chat.author.username
            }
        return None


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'post', 'sender', 'user', 'notification_type', 'text_preview', 'date', 'is_seen']
        read_only_fields = ['id', 'date']
