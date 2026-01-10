from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    UserProfileDetailAPIView, UserProfileListAPIView,
    CityListAPIView, CityDetailAPIView,
    HotelListAPIView, HotelDetailAPIView,
    RoomDetailAPIView, RoomListAPIView,
    ReviewCreateAPIView, ReviewEditAPIView,
    BookingViewSet, HotelViewSet,
    RegisterView, LoginView, LogoutView,
    HotelCreateAPIView
)

router = SimpleRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'hotel_methods', HotelViewSet, basename='hotel-methods')

urlpatterns = [
    path('', include(router.urls)),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('hotel_create/<int:pk>/', HotelCreateAPIView.as_view(), name='hotel_manage'),
    path('cities/', CityListAPIView.as_view(), name='city_list'),
    path('cities/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('room/', RoomListAPIView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room_detail'),
    path('users/', UserProfileListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='users_detail'),
    path('review/', ReviewCreateAPIView.as_view(), name='create_review'),
    path('review/<int:pk>/', ReviewEditAPIView.as_view(), name='review_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]