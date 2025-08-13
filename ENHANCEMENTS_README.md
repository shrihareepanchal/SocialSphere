# Django Social Network App - Enhancements

This document describes the new enhancements added to the Django Social Network App.

## New Features Added

### 1. Real-time Notifications (Django Channels + Redis)
- **WebSocket-based real-time notifications** using Django Channels
- **Redis backend** for scalable channel layers
- **Instant notification delivery** for likes, comments, friend requests, etc.
- **Real-time unread count updates** in the UI
- **Mark notifications as read** via WebSocket or AJAX

#### Files Modified/Created:
- `notification/consumers.py` - WebSocket consumer for real-time notifications
- `notification/routing.py` - WebSocket routing configuration
- `notification/views.py` - Enhanced views with AJAX endpoints
- `notification/urls.py` - New URL patterns for AJAX operations
- `myproject/routing.py` - Updated ASGI routing to include notifications
- `myproject/settings.py` - Redis configuration for channel layers

### 2. Direct Messaging System
- **Enhanced chat functionality** with real-time messaging
- **WebSocket-based communication** for instant message delivery
- **Chat room management** with user-to-user conversations
- **Message status tracking** (read/unread)
- **Chat history persistence**

#### Files Modified/Created:
- `chat/models.py` - Enhanced chat models (already existed)
- `chat/consumers.py` - WebSocket consumer for real-time chat (already existed)
- `chat/routing.py` - WebSocket routing (already existed)

### 3. Advanced Search (Elasticsearch)
- **Full-text search** across posts and users
- **Fuzzy matching** with typo tolerance
- **Search suggestions** based on user input
- **Search analytics** tracking user search patterns
- **Multi-field search** (title, content, author, etc.)
- **Search result categorization** (posts vs users)

#### Files Modified/Created:
- `search/` - New search app
- `search/models.py` - Elasticsearch document models and search tracking
- `search/views.py` - Search functionality and API endpoints
- `search/urls.py` - Search URL patterns
- `search/templates/` - Search UI templates
- `search/management/commands/build_search_index.py` - Management command for building indices
- `myproject/settings.py` - Elasticsearch configuration

### 4. API for Mobile Apps (Django REST Framework)
- **RESTful API endpoints** for all major functionality
- **Token-based authentication** for mobile apps
- **Comprehensive serializers** for all models
- **ViewSet-based architecture** with custom actions
- **CORS support** for cross-origin requests
- **Pagination** for large datasets

#### Files Modified/Created:
- `api/` - New API app
- `api/serializers.py` - Serializers for all models
- `api/views.py` - API viewsets with custom actions
- `api/urls.py` - API URL routing
- `myproject/settings.py` - REST framework and CORS configuration

## Setup Instructions

### Prerequisites
1. **Python 3.8+**
2. **Redis server** (for real-time features)
3. **Elasticsearch 7.x** (for advanced search)

### Installation

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Start Redis Server
```bash
# On Windows (using WSL or Docker)
redis-server

# On macOS
brew services start redis

# On Linux
sudo systemctl start redis
```

#### 3. Start Elasticsearch
```bash
# Download and start Elasticsearch 7.17.0
# Or use Docker:
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.0
```

#### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Build Elasticsearch Indices
```bash
python manage.py build_search_index
```

#### 6. Start the Development Server
```bash
python manage.py runserver
```

### Configuration

#### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
EMAIL_PORT=587
GOOGLE_RECAPTCHA_SECRET_KEY=your_recaptcha_key
```

#### Redis Configuration
The app is configured to use Redis on `localhost:6379`. Update `REDIS_HOST` and `REDIS_PORT` in `settings.py` if needed.

#### Elasticsearch Configuration
The app is configured to use Elasticsearch on `localhost:9200`. Update `ELASTICSEARCH_DSL` in `settings.py` if needed.

## Usage

### Real-time Notifications
- Notifications are automatically sent via WebSocket when events occur
- Users receive instant updates for likes, comments, friend requests, etc.
- Unread count is updated in real-time

### Advanced Search
- Visit `/search/` to use the search interface
- Search across posts and users with fuzzy matching
- Get search suggestions as you type
- View search analytics and recent searches

### API Endpoints
- **Users**: `/api/users/`
- **Posts**: `/api/posts/`
- **Friend Requests**: `/api/friend-requests/`
- **Chat**: `/api/chats/`
- **Notifications**: `/api/notifications/`

### Direct Messaging
- Visit `/chats/` to access the chat interface
- Create chat rooms with friends
- Send and receive real-time messages

## API Documentation

### Authentication
The API supports both session and token authentication:
- **Session Auth**: Use Django's built-in session authentication
- **Token Auth**: Use Django REST framework's token authentication

### Example API Usage

#### Get User Feed
```bash
GET /api/posts/feed/
Authorization: Token your_token_here
```

#### Like a Post
```bash
POST /api/posts/{post_id}/like/
Authorization: Token your_token_here
```

#### Send Friend Request
```bash
POST /api/friend-requests/
Authorization: Token your_token_here
Content-Type: application/json

{
    "receiver": user_id
}
```

## WebSocket Events

### Notifications
- **Connect**: `ws://localhost:8000/ws/notifications/`
- **Events**:
  - `notification`: New notification received
  - `notification_update`: Notification updated
  - `unread_count`: Unread count update

### Chat
- **Connect**: `ws://localhost:8000/ws/chat/{room_id}/`
- **Events**:
  - `chat_message`: New message received
  - `user_join`: User joined chat
  - `user_leave`: User left chat

## Troubleshooting

### Common Issues

#### 1. Redis Connection Error
- Ensure Redis server is running
- Check Redis host/port configuration
- Verify Redis is accessible from your application

#### 2. Elasticsearch Connection Error
- Ensure Elasticsearch is running on port 9200
- Check Elasticsearch version compatibility (7.x required)
- Verify network connectivity

#### 3. WebSocket Connection Issues
- Check if Django Channels is properly configured
- Verify ASGI routing configuration
- Ensure Redis channel layer is working

#### 4. Search Not Working
- Run `python manage.py build_search_index` to create indices
- Check Elasticsearch logs for errors
- Verify document models are properly configured

### Performance Optimization

#### 1. Redis
- Configure Redis persistence if needed
- Monitor memory usage
- Use Redis clustering for production

#### 2. Elasticsearch
- Configure proper sharding and replication
- Monitor cluster health
- Optimize index settings for your use case

#### 3. Django Channels
- Use Redis as channel layer backend
- Monitor WebSocket connections
- Implement connection pooling if needed

## Production Deployment

### Requirements
- **WSGI/ASGI server** (e.g., Daphne, uvicorn)
- **Redis cluster** for production
- **Elasticsearch cluster** for production
- **Load balancer** for WebSocket connections
- **SSL/TLS** for secure WebSocket connections

### Environment Variables
Set production environment variables:
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
REDIS_HOST=your_redis_host
ELASTICSEARCH_HOST=your_elasticsearch_host
ALLOWED_HOSTS=your_domain.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
