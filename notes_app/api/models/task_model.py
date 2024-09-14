from django.db import models
from django.core.validators import MinLengthValidator

class Task(models.Model):
    """The model for the notes"""
    title = models.TextField(null=False, blank=False, validators=[MinLengthValidator(limit_value=1)])
    description = models.TextField(null=True, blank=True)
    completion_status = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self) -> str:
        return "Title: " + self.title + "\nDescription: " + self.description + "\nCompletion Status: " + \
        "Complete" if self.completion_status else "Incomplete"