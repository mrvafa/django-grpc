from django.core.management.base import BaseCommand
from core.models import Tag, Post
from random import shuffle


class Command(BaseCommand):
    help = 'This command create sample posts and tags'

    def handle(self, *args, **options):
        for i in range(100):
            Post.objects.create(title=f'Post {i}', body=f'Post Body {i}',
                                status='accepted')

        for i in range(20):
            Tag.objects.create(title=f'Tag {i}', body=f'Tag Body {i}')

        tags = Tag.objects.all()
        tags = [t for t in tags]
        for post in Post.objects.all():
            shuffle(tags)
            for tag in tags[11:]:
                post.tags.add(tag)
                post.save()
