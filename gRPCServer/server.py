import sys
from concurrent import futures

import django

sys.path.extend(
    ['/home/mrvafa/Projects/Python/DjangoGRPC', ]
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
            0: 'non_status',
            1: 'accepted',
            2: 'rejected',
        }

    def Search(self, request, context):
        search_key = request.seach_key
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
                status=self.status[post.status],
            ))
        return responds

    def GetPostByID(self, request, context):
        post_id = request.id
        post = Post.objects.filter(id=post_id).first()
        tags = [tag_pb2.Tag(id=tag.id, title=tag.title, body=tag.body) for tag in post.tags.all()]
        respond = post_pb2.Post(
            id=post.id,
            title=post.title,
            body=post.body,
            tasg=tags,
            status=self.status[post.status],
        )
        return respond


def serve():
    server = grpc.server((futures.ThreadPoolExecutor(max_workers=10)))
    post_pb2_grpc.add_PostServiceServicer_to_server(PostService, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
