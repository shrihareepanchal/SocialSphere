# 🌐 SocialSphere  
**A Modern, Full-Featured Social Networking Platform Built with Django**  

SocialSphere is a **scalable, feature-rich social media application** designed to connect people through posts, chats, blogs, video calls, and more.  
It integrates multiple interactive modules — from real-time messaging to content sharing — in a single, seamless experience.  

---

## 🚀 Features
- 👥 **User Profiles** — Registration, authentication, profile customization.  
- 📝 **Blog System** — Create, edit, and publish blog posts with comments & likes.  
- 💬 **Real-Time Chat** — Instant messaging with WebSocket support.  
- 📹 **Video Calling** — Peer-to-peer video chat using WebRTC.  
- 🖼 **Media Sharing** — Upload, store, and serve images/videos.  
- 🔔 **Notifications** — Instant updates for messages, friend requests, likes, and more.  
- 🔍 **Search** — Find people, posts, and content across the platform.  
- 🤝 **Friend System** — Send requests, accept/reject, and manage friends.  
- 📱 **Responsive UI** — Works across devices.  

---

## 📂 Project Structure

    SocialSphere/
    │
    ├── api/                         # REST API endpoints for frontend-backend communication
    │   ├── migrations/              # Database migration files for API models
    │   ├── serializers.py           # Data serialization for API
    │   ├── urls.py                   # API routes
    │   ├── views.py                  # API request handling logic
    │   └── models.py                 # API-related database models
    │
    ├── blog/                        # Blog management system
    │   ├── migrations/
    │   ├── templates/blog/          # HTML templates for blog pages
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── forms.py                  # Blog forms for creating/editing posts
    │
    ├── chat/                        # Real-time chat module
    │   ├── migrations/
    │   ├── consumers.py              # WebSocket consumers for chat
    │   ├── routing.py                # WebSocket URL routing
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── templates/chat/          # Chat UI templates
    │
    ├── friend/                      # Friend request system
    │   ├── migrations/
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── templates/friend/
    │
    ├── media/                       # Uploaded media files (profile pics, posts, etc.)
    │
    ├── myproject/                   # Main Django project configuration
    │   ├── __init__.py
    │   ├── asgi.py                   # ASGI entry point for async features
    │   ├── settings.py               # Project settings
    │   ├── urls.py                   # Global URL routing
    │   ├── wsgi.py                   # WSGI entry point for deployment
    │   └── middleware.py             # Custom middleware if any
    │
    ├── notification/                # Notification management
    │   ├── migrations/
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── templates/notification/
    │
    ├── search/                      # Search functionality
    │   ├── urls.py
    │   ├── views.py
    │   └── templates/search/
    │
    ├── users/                       # User authentication & profiles
    │   ├── migrations/
    │   ├── forms.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── templates/users/
    │
    ├── videocall/                   # Video calling module
    │   ├── migrations/
    │   ├── urls.py
    │   ├── views.py
    │   ├── models.py
    │   └── templates/videocall/
    │
    ├── .gitignore                   # Files/folders to ignore in Git
    ├── Procfile                     # Heroku deployment config
    ├── manage.py                    # Django management script
    ├── requirements.txt             # Python dependencies
    ├── runtime.txt                  # Python version for deployment
    ├── ENHANCEMENTS_README.md       # Planned improvements
    ├── SOCIALSPHERE_README.md       # Additional project documentation
    ├── test_enhancements.py         # Tests for enhancements


---

## 🛠 Tech Stack
- **Backend:** Python, Django, Django REST Framework, Django Channels  
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (Development)  
- **Real-Time:** WebSockets 

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
    git clone https://github.com/shrihareepanchal/SocialSphere.git
    cd SocialSphere
    
### 2️⃣ Create a Virtual Environment
    python -m venv venv
    venv\Scripts\activate

### 3️⃣ Install Dependencies
    pip install -r requirements.txt

### 4️⃣ Run Migrations
    python manage.py makemigrations
    python manage.py migrate

### 5️⃣ Create a Superuser
    python manage.py createsuperuser

### 6️⃣ Run the Development Server
    python manage.py runserver
  Now visit: http://127.0.0.1:8000/

# 🔮 Future Enhancements
- AI-based content recommendations
- Voice & group video calls
- Hashtag-based trending system
- Dark mode support

# 📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

# 📬 Contact
  Developer: Shriharee Panchal
  📧 Email: shriharee0004@gmail.com
  🌐 GitHub: shrihareepanchal
