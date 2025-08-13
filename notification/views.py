from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from notification.models import Notification
import json

# Create your views here.

""" All notifications """
@login_required
def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    
    # Get unread count
    unread_count = notifications.filter(is_seen=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'blog/notifications.html', context)


@csrf_exempt
def mark_notification_read(request):
    """Mark notification as read via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification_id = data.get('notification_id')
            
            if notification_id:
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_seen = True
                notification.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Notification marked as read'
                })
            
            return JsonResponse({
                'success': False,
                'error': 'Notification ID required'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            })
        except Notification.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Notification not found'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })


@csrf_exempt
def mark_all_notifications_read(request):
    """Mark all notifications as read via AJAX"""
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)
        
        return JsonResponse({
            'success': True,
            'message': 'All notifications marked as read'
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })


@csrf_exempt
def get_unread_count(request):
    """Get unread notification count via AJAX"""
    if request.method == 'GET':
        count = Notification.objects.filter(user=request.user, is_seen=False).count()
        
        return JsonResponse({
            'success': True,
            'unread_count': count
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    })