from rest_framework.response import Response
from rest_framework.decorators import api_view
from workout_app.models import BlogPost
from workout_app.serializers.blog_serializer import BlogPostSerializer


@api_view(["GET"])
def get_all_articles(_):
    articles = BlogPost.objects.all()  # optional: newest first
    serializer = BlogPostSerializer(articles, many=True)
    return Response(serializer.data)
