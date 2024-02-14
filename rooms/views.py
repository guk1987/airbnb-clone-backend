from django.conf import settings
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from . import serializers
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class Rooms(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(
            all_rooms, 
            many=True,
            context={"request": request},)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError(detail="Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError(detail="Category cannot be a kind of experiences")
            except Category.DoesNotExist:
                raise ParseError(detail="Category not found")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    Amenities = request.data.get("amenities")
                    for amenity_pk in Amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = serializers.RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError(detail="Amenity not found") 
        else:
            return Response(serializer.errors)
    
        
class RoomDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = serializers.RoomDetailSerializer(
            room,
            context={"request": request},
            )
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        serializer = serializers.RoomDetailSerializer(
            room, 
            data=request.data,
            partial=True,
            )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError(detail="Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError(detail="Category cannot be a kind of experiences")
            except Category.DoesNotExist:
                raise ParseError(detail="Category not found")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    #request.data.get("amenities") 가 있으면 실행
                    if request.data.get("amenities"):
                        Amenities = request.data.get("amenities")
                        for amenity_pk in Amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = serializers.RoomDetailSerializer(room)
                        return Response(serializer.data)
                    else:
                        serializer = serializers.RoomDetailSerializer(room)
                        return Response(serializer.data)
            except Exception:
                raise ParseError(detail="Amenity not found") 
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(HTTP_204_NO_CONTENT)
    
class Amenities(APIView):
    
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = serializers.AmenitiySerializer(all_amenities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.AmenitiySerializer(data = request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(serializers.AmenitiySerializer(amenity).data)
        else:
            return Response(serializer.errors)
    
class AmenitiyDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitiySerializer(amenity)
        return Response(serializer.data)
    
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitiySerializer(
            amenity, 
            data=request.data,
            partial=True,
            )
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(serializers.AmenitiySerializer(update_amenity).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(HTTP_204_NO_CONTENT)

class RoomReviews(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomPhotos(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)