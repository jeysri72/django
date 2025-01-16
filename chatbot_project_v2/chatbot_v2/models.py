from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username} on {self.timestamp}"


class KnowledgeBase(models.Model):
    query = models.CharField(max_length=255, unique=True)  # Switched to CharField with max_length
    response = models.TextField()  # Assuming response does not need indexing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.query} - Created at {self.created_at}"