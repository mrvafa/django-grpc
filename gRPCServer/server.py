import os
import sys
from concurrent import futures

import django

sys.path.extend(
    [os.getenv('DJANGO_PROJECT_FULL_PATH'), ]
)
if 'setup' in dir(django):
    django.setup()

import grpc
from django.db.models import Q

import post_pb2
import tag_pb2
import post_pb2_grpc
from core.models import Post


class PostService(post_pb2_grpc.PostServiceServicer):
    def __init__(self):
        self.status = {
            'non_status': post_pb2.PostStatus.NO_STATUS,
            'accepted': post_pb2.PostStatus.ACCEPTED,
            'rejected': post_pb2.PostStatus.REJECTED,
        }

    def Search(self, request, context):
        search_key = request.search_key
        posts = Post.objects.filter(
            Q(title__icontains=search_key),
            Q(body__icontains=search_key),
        )
        responds = []
        for post in posts:
            tags = [tag_pb2.Tag(id=tag.id, title=tag.title, body=tag.body) for tag in post.tags.all()]
            responds.append(post_pb2.Post(
                id=post.id,
                title=post.title,
                body=post.body,
                tags=tags,
                post_status=self.status[post.status],
            ))
        return post_pb2.PostsRespond(posts=responds)


    def GetPostByID(self, request, context):
        post_id = request.id
        post = Post.objects.filter(id=post_id).first()
        tags = [tag_pb2.Tag(id=tag.id, title=tag.title, body=tag.body) for tag in post.tags.all()]
        respond = post_pb2.Post(
            id=post.id,
            title=post.title,
            body=post.body,
            tags=tags,
            post_status=self.status[post.status],
        )
        return respond


def serve():
    server = grpc.server((futures.ThreadPoolExecutor(max_workers=10)))
    post_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
