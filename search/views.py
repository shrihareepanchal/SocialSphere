from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django_elasticsearch_dsl.search import Search
from .models import SearchIndex, PostDocument, UserDocument
import json


@login_required
def search_view(request):
    """Main search view"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    # Get recent searches for the user
    recent_searches = SearchIndex.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:10]
    
    if query:
        # Track search analytics
        SearchIndex.objects.create(
            user=request.user,
            query=query,
            results_count=0
        )
        
        results = perform_search(query, search_type)
        
        # Update results count
        SearchIndex.objects.filter(
            user=request.user,
            query=query
        ).update(results_count=len(results))
        
        return render(request, 'search/search_results.html', {
            'query': query,
            'results': results,
            'search_type': search_type
        })
    
    return render(request, 'search/search.html', {
        'recent_searches': recent_searches
    })


def perform_search(query, search_type='all'):
    """Perform Elasticsearch search"""
    results = {}
    
    if search_type in ['all', 'posts']:
        # Search posts
        post_search = PostDocument.search().query(
            'multi_match',
            query=query,
            fields=['title', 'content', 'author.username', 'author.first_name', 'author.last_name'],
            fuzziness='AUTO'
        )
        results['posts'] = post_search[:20].to_queryset()
    
    if search_type in ['all', 'users']:
        # Search users
        user_search = UserDocument.search().query(
            'multi_match',
            query=query,
            fields=['username', 'first_name', 'last_name', 'email'],
            fuzziness='AUTO'
        )
        results['users'] = user_search[:20].to_queryset()
    
    return results


@csrf_exempt
def search_api(request):
    """API endpoint for search"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            search_type = data.get('type', 'all')
            
            if query:
                results = perform_search(query, search_type)
                
                # Convert to serializable format
                serialized_results = {}
                
                if 'posts' in results:
                    serialized_results['posts'] = [
                        {
                            'id': post.id,
                            'title': post.title,
                            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
                            'author': {
                                'id': post.author.id,
                                'username': post.author.username,
                                'first_name': post.author.first_name,
                                'last_name': post.author.last_name,
                            },
                            'date_posted': post.date_posted.isoformat(),
                            'likes_count': getattr(post, 'likes_count', 0),
                            'comments_count': getattr(post, 'comments_count', 0),
                        }
                        for post in results['posts']
                    ]
                
                if 'users' in results:
                    serialized_results['users'] = [
                        {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'date_joined': user.date_joined.isoformat(),
                        }
                        for user in results['users']
                    ]
                
                return JsonResponse({
                    'success': True,
                    'query': query,
                    'results': serialized_results,
                    'total_results': sum(len(v) for v in serialized_results.values())
                })
            
            return JsonResponse({'success': False, 'error': 'Query parameter required'})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})


def search_suggestions(request):
    """Get search suggestions based on partial query"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get suggestions from recent searches
    recent_searches = SearchIndex.objects.filter(
        query__icontains=query
    ).values_list('query', flat=True).distinct()[:5]
    
    # Get suggestions from post titles
    post_suggestions = PostDocument.search().query(
        'prefix',
        title=query
    )[:5].to_queryset()
    
    # Get suggestions from usernames
    user_suggestions = UserDocument.search().query(
        'prefix',
        username=query
    )[:5].to_queryset()
    
    suggestions = list(recent_searches)
    suggestions.extend([post.title for post in post_suggestions])
    suggestions.extend([user.username for user in user_suggestions])
    
    # Remove duplicates and limit
    suggestions = list(set(suggestions))[:10]
    
    return JsonResponse({'suggestions': suggestions})
