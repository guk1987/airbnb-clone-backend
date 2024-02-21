from rest_framework import serializers
from . models import Amenity, Room
from wishlists.models import Wishlist
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitiySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )

class RoomDetailSerializer(serializers.ModelSerializer):
       
        owner = TinyUserSerializer(read_only=True)
        amenities = AmenitiySerializer(
            read_only = True, 
            many=True,
            )
        category = CategorySerializer(read_only=True)
        rating = serializers.SerializerMethodField()
        is_owner = serializers.SerializerMethodField()
        photos = PhotoSerializer(many=True, read_only=True)
        is_liked = serializers.SerializerMethodField()
        
        class Meta:
            model = Room
            fields = "__all__"
        
        def get_rating(self, room):
            return room.rating()
        
        def get_is_owner(self, room):
            request = self.context.get("request")
            return room.owner == request.user
    
        def get_is_liked(self, room):
            request = self.context.get("request")
            return Wishlist.objects.filter(user=request.user, rooms=room).exists()
        
class RoomListSerializer(serializers.ModelSerializer):
        
        rating = serializers.SerializerMethodField()
        is_owner = serializers.SerializerMethodField()
        photos = PhotoSerializer(many=True, read_only=True)
        is_liked = serializers.SerializerMethodField()
        class Meta:
            model = Room
            fields = (
                "pk",
                "name",
                "country",
                "city",
                "price",
                "rating",
                "is_owner",
                "is_liked",
                "photos",
            )
            
        def get_rating(self, room):
            return room.rating()
        
        def get_is_owner(self, room):
            request = self.context["request"]
            return room.owner == request.user
            
        
        #프론트에서 룸 리스트를 불러올 때 로그인 정보 때문에 아래 코드는 문제가 있음..
        # def get_is_liked(self, room):
        #     request = self.context["request"]
        #     return Wishlist.objects.filter(user=request.user, rooms=room).exists()
        
        def get_is_liked(self, room):
            if self.context.get('request').user.is_authenticated:
                return Wishlist.objects.filter(user=self.context.get('request').user, rooms=room).exists()
            else:
                return False  # Or any other default value for non-logged-in users