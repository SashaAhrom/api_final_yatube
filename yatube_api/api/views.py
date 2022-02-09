from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .mixins import CreateListViewSet
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer,)
from posts.models import Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering and /api/v1/posts/ has pagination.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Api endpoint has only GET methods without registering.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(PostViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering.
    """
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(CreateListViewSet):
    """
    Api endpoint has full match search.
    Can`t subscribe twice and you can`t follow yourself.
    """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
