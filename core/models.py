from django.db import models

class Tag(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(
        choices=[('non_status', 'No status'),
                 ('accepted', 'Accepted'),
                 ('rejected', 'Rejected')],
        max_length=10,
        default='non_status',
        blank=True,
    )
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
