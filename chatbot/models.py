from django.db import models

class KnowledgeBase(models.Model):
    content = models.TextField()  # General data (facts, docs, etc.)
    category = models.CharField(max_length=100, blank=True)  # Optional for filtering
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # Show first 50 chars for admin