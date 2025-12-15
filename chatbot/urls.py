from django.urls import path
from .views import chatbot_view, chat_page_view  # We'll add chat_page_view for the HTML

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot_api'),
    path('', chat_page_view, name='chat_page'),  # Root for HTML page
]