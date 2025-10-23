from django.db import models


class Proposal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    student_name = models.CharField(max_length=100)
    mentor_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ],
            default='pending',
    )

    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.student_name} ({self.status})"
