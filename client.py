import grpc
import post_pb2_grpc
import post_pb2

channel = grpc.insecure_channel('localhost:50051')
client = post_pb2_grpc.PostServiceStub(channel)
request = post_pb2.PostIDRequest(id=1)
respond = client.GetPostByID(request)
print(respond.title, respond.id)

request = post_pb2.SearchText(search_key='5')
posts = client.Search(request).posts
for post in posts:
    print(post.id, post.title, post.body)

