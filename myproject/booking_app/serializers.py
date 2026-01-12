from rest_framework import serializers
from .models import (
    Country, UserProfile, City, Service, Hotel, HotelImage,
    Room, RoomImage, Review, Booking
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'username', 'email', 'password', 'country']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class HotelListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    region = serializers.IntegerField(source='city.id', read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'image', 'hotel_name', 'region']

    def get_image(self, obj):
        first_image = obj.hotel_images.first()
        if first_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.hotel_image.url)
            return first_image.hotel_image.url
        return None

class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_images = serializers.SerializerMethodField()
    def get_hotel_images(self, obj):
        return [img.hotel_image.url for img in obj.hotel_images.all()]
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = '__all__'