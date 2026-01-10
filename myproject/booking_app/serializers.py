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
        fields = ['first_name',  'username', 'email', 'password', 'country']
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
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class CountryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_image', 'country_name']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_images', 'user_role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileReviewSerializer(serializers.ModelSerializer):
    country = CountryProfileSerializer()
    class Meta:
        model = UserProfile
        fields = ['first_name', 'user_images', 'country']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_photo', 'city_name']



class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']



class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_image', 'service_name']



class ServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name']



class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']



class HotelListSerializer(serializers.ModelSerializer):
    city = CityNameSerializer()
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_images', 'city', 'hotel_stars', 'description']



class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'




class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'price', 'room_type', 'room_status', 'description']


class ReviewCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Review
        fields = ['rating', 'comment', 'user', 'hotel']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y')
    user  = UserProfileReviewSerializer()
    class Meta:
        model = Review
        fields = ['user', 'comment', 'created_date']


class CityDetailSerializer(serializers.ModelSerializer):
    city_hotel = HotelListSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = [ 'city_name', 'city_hotel']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']



class RoomDetailSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['room_number', 'price', 'room_type', 'room_status', 'description', 'room_images']



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    country = CountrySerializer()
    city = CityNameSerializer()
    service = ServiceListSerializer(many=True)
    hotel_rooms = RoomListSerializer(many=True, read_only=True)
    hotel_reviews = ReviewSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'country', 'city', 'hotel_images', 'hotel_stars',
                  'street', 'postel_code', 'description', 'service', 'hotel_rooms',
                  'get_avg_rating', 'get_count_people', 'hotel_reviews']
    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()