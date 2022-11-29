from watchlist_app.api.serializers import WatchListSerializer, ReviewSerializer, StreamPlatformSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from watchlist_app.models import WatchList, StreamPlatform, Review
# from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class StreamPlatFormVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# Concreate class based view
# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     querset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    throttle_classes=[ReviewCreateThrottle]

    def get_queryset(self):
        return Review().objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already Review this Movie !")
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
            print(watchlist.avg_rating)
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating+serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes=[ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    


# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class WatchListListAV(APIView):
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"errors": "Movie Not Found:"})
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"data": "Data Deleted successfully:"})

    # @api_view(['GET', 'POST'])
    # def movie_list(request):
    #     if request.method == 'GET':
    #         movies = Movie.objects.all()
    #         serializer = MovieSerializer(movies, many=True)
    #         return Response(serializer.data)
    #     if request.method == "POST":
    #         serializer = MovieSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors)

    # @api_view(['GET', 'DELETE', 'PUT'])

    # def movie_details(request, pk):
    #     if request.method == "GET":
    #         movie = Movie.objects.get(pk=pk)
    #         serializer = MovieSerializer(movie)
    #         return Response(serializer.data)

    #     # if request.method == "DELETE":

    #     if request.method == 'PUT':
    #         movie = Movie.objects.get(pk=pk)
    #         serializer = MovieSerializer(movie, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors)

    #     if request.method == 'DELETE':
    #         movie = Movie.objects.get(pk=pk)
    #         movie.delete()
    #         return Response({"data": "Data Deleted successfully:"})
