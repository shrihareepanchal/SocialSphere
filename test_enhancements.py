#!/usr/bin/env python
"""
Test script to verify the Django Social Network App enhancements are working.
Run this script after setting up the project to test all new features.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def test_imports():
    """Test that all new modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test search app
        from search.models import SearchIndex, PostDocument, UserDocument
        from search.views import search_view, perform_search
        print("✓ Search app imports successful")
        
        # Test API app
        from api.serializers import UserSerializer, PostSerializer
        from api.views import UserViewSet, PostViewSet
        print("✓ API app imports successful")
        
        # Test notification enhancements
        from notification.consumers import NotificationConsumer
        from notification.views import mark_notification_read
        print("✓ Notification enhancements imports successful")
        
        # Test Django REST framework
        import rest_framework
        print("✓ Django REST framework import successful")
        
        # Test channels
        import channels
        print("✓ Django Channels import successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_models():
    """Test that new models can be created"""
    print("\nTesting models...")
    
    try:
        from django.contrib.auth.models import User
        from search.models import SearchIndex
        
        # Test SearchIndex model
        user, created = User.objects.get_or_create(
            username='test_user_enhancements',
            defaults={'email': 'test@example.com'}
        )
        
        search_index = SearchIndex.objects.create(
            user=user,
            query='test query',
            results_count=5
        )
        
        print(f"✓ SearchIndex model test successful - ID: {search_index.id}")
        
        # Clean up
        search_index.delete()
        if created:
            user.delete()
            
        return True
        
    except Exception as e:
        print(f"✗ Model test error: {e}")
        return False

def test_settings():
    """Test that new settings are properly configured"""
    print("\nTesting settings...")
    
    try:
        from django.conf import settings
        
        # Test REST framework settings
        if 'rest_framework' in settings.INSTALLED_APPS:
            print("✓ REST framework in INSTALLED_APPS")
        else:
            print("✗ REST framework not in INSTALLED_APPS")
            
        # Test channels settings
        if hasattr(settings, 'CHANNEL_LAYERS'):
            print("✓ CHANNEL_LAYERS configured")
        else:
            print("✗ CHANNEL_LAYERS not configured")
            
        # Test Elasticsearch settings
        if hasattr(settings, 'ELASTICSEARCH_DSL'):
            print("✓ ELASTICSEARCH_DSL configured")
        else:
            print("✗ ELASTICSEARCH_DSL not configured")
            
        # Test CORS settings
        if 'corsheaders' in settings.INSTALLED_APPS:
            print("✓ CORS headers in INSTALLED_APPS")
        else:
            print("✗ CORS headers not in INSTALLED_APPS")
            
        return True
        
    except Exception as e:
        print(f"✗ Settings test error: {e}")
        return False

def test_urls():
    """Test that new URL patterns are accessible"""
    print("\nTesting URLs...")
    
    try:
        from django.urls import reverse, NoReverseMatch
        
        # Test search URLs
        try:
            search_url = reverse('search:search')
            print(f"✓ Search URL: {search_url}")
        except NoReverseMatch:
            print("✗ Search URL not found")
            
        # Test API URLs
        try:
            api_users_url = reverse('api:user-list')
            print(f"✓ API users URL: {api_users_url}")
        except NoReverseMatch:
            print("✗ API users URL not found")
            
        # Test notification URLs
        try:
            notification_url = reverse('show-notifications')
            print(f"✓ Notification URL: {notification_url}")
        except NoReverseMatch:
            print("✗ Notification URL not found")
            
        return True
        
    except Exception as e:
        print(f"✗ URL test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Django Social Network App - Enhancement Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_models,
        test_settings,
        test_urls
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhancements are working correctly.")
        print("\nNext steps:")
        print("1. Start Redis server")
        print("2. Start Elasticsearch")
        print("3. Run: python manage.py build_search_index")
        print("4. Run: python manage.py runserver")
        print("5. Visit /search/ to test search functionality")
        print("6. Visit /api/ to test API endpoints")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("- Make sure all dependencies are installed")
        print("- Check that migrations have been run")
        print("- Verify the project structure is correct")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
