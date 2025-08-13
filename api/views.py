from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import (
    UserSerializer, ProfileSerializer, PostSerializer, CommentSerializer,
    FriendRequestSerializer, FriendListSerializer,
    ChatSerializer, RoomSerializer, NotificationSerializer
)
from blog.models import Post, Comment
from users.models import Profile
from friend.models import FriendRequest, FriendList
from chat.models import Room, Chat
from notification.models import Notification


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get user profile"""
        user = self.get_object()
        try:
            profile = user.profile
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search users"""
        query = request.query_params.get('q', '')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )[:20]
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response([])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like/unlike a post"""
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'liked': False})
        post.likes.add(user)
        return Response({'liked': True})
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """Add comment to post"""
        post = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get post comments"""
        post = self.get_object()
        comments = post.comments.all().order_by('date_added')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get user's feed"""
        user = request.user
        # Get posts from user and friends
        friends = FriendList.objects.filter(user=user).first()
        if friends:
            friend_ids = [friend.id for friend in friends.friends.all()]
            friend_ids.append(user.id)
            posts = Post.objects.filter(author__id__in=friend_ids).order_by('-date_posted')
        else:
            posts = Post.objects.filter(author=user).order_by('-date_posted')
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter requests for current user"""
        return FriendRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept friend request"""
        friend_request = self.get_object()
        
        if friend_request.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        # Add to friend list
        sender_list, _ = FriendList.objects.get_or_create(user=friend_request.sender)
        receiver_list, _ = FriendList.objects.get_or_create(user=friend_request.receiver)
        
        sender_list.friends.add(friend_request.receiver)
        receiver_list.friends.add(friend_request.sender)
        
        # Deactivate request
        friend_request.is_active = False
        friend_request.save()
        
        return Response({'message': 'Friend request accepted'})
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline friend request"""
        friend_request = self.get_object()
        
        if friend_request.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        friend_request.is_active = False
        friend_request.save()
        
        return Response({'message': 'Friend request declined'})


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter chats for current user"""
        return Chat.objects.filter(
            Q(author=self.request.user) | Q(friend=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def rooms(self, request):
        """Get user's chat rooms"""
        rooms = Room.objects.filter(
            Q(author=request.user) | Q(friend=request.user)
        ).order_by('-created')
        
        serializer = RoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get messages from a room"""
        room = get_object_or_404(Room, pk=pk)
        
        if room.author != request.user and room.friend != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        messages = room.chats.all().order_by('date')
        serializer = ChatSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter notifications for current user"""
        return Notification.objects.filter(user=self.request.user).order_by('-date')
    
    @action(detail=True, methods=['post'])
    def mark_seen(self, request, pk=None):
        """Mark notification as seen"""
        notification = self.get_object()
        notification.is_seen = True
        notification.save()
        return Response({'message': 'Notification marked as seen'})
    
    @action(detail=False, methods=['post'])
    def mark_all_seen(self, request):
        """Mark all notifications as seen"""
        self.get_queryset().update(is_seen=True)
        return Response({'message': 'All notifications marked as seen'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_seen=False).count()
        return Response({'unread_count': count})
