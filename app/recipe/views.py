from rest_framework import viewsets, mixins, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers
from rest_framework.decorators import action
from rest_framework.response import Response


class BaseAttrViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Base viewset for recipe owned user attribute"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for authenticated users only"""
        assigned_only = bool(
        int(self.request.query_params.get('assigned_only',0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseAttrViewSet):
    """Manage tags in database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self,qs):
        """Convert list of string ids to list of int ids"""
        return [int(str_id) for str_id in qs.split(',')]


    def get_queryset(self):
        """Return recipes for authenticated users only"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        # print('-----------------------------------------------------')
        # print(tags)
        # print(ingredients)
        #
        # print('-----------------------------------------------------')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            # print(ingredient_ids)
            # print('-----------------------------------------------------')
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
            # print(queryset)
            # print('-----------------------------------------------------')


        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'],detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to recipe"""
        recipe=self.get_object()
        serializer=self.get_serializer(
        recipe,
        data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

        return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
        )
    # def get_object(self):
    #     """Retrieve and return authenticated user"""
    #     return self.request.







#^^INGREDIENT AND TAG COMBINED TO ONE

# class TagViewSet(viewsets.GenericViewSet,
#                 mixins.ListModelMixin,
#                 mixins.CreateModelMixin):
#     """Manage tags in database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer
#
#     def get_queryset(self):
#         """Returns objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new tag"""
#         serializer.save(user=self.request.user)
#
# class IngredientViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,
#                         mixins.CreateModelMixin):
#     """Manage ingredients in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer


#     def get_queryset(self):
#         """Returns objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#
#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)
