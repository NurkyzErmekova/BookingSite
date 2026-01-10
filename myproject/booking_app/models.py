from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_image = models.ImageField(upload_to='country_images')
    country_name = models.CharField(max_length=40,  unique=True)

    def __str__(self):
        return self.country_name


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(80)],
                                           null=True, blank=True)
    user_images = models.ImageField(upload_to='user_images', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    RoleChoices = (
    ('client', 'client'),
    ('owner', 'owner')
    )
    user_role = models.CharField(max_length=20, choices=RoleChoices, default='client')
    register_data = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='country')
    city_photo = models.ImageField(upload_to='city_images')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_images')
    service_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.service_name}, {self.service_image}'

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotel')
    street = models.CharField(max_length=100)
    postel_code = models.PositiveSmallIntegerField(verbose_name='почтовый индекс')
    hotel_stars  =  models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField()
    service = models.ManyToManyField(Service)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.hotel_name

    def get_avg_rating(self):
        reviews = self.hotel_reviews.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(), 1)
        return 0
    def get_count_people(self):
        return self.hotel_reviews.count()



class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_photo')

    def __str__(self):
        return f'{self.hotel}, {self.hotel_img}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rooms')
    room_number = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    RoomTypeChoices = (
    ('Люкс', 'Люкс'),
    ('Полулюкс', 'Полулюкс'),
    ('Семеный', 'Семеный'),
    ('Эконом', 'Эконом'),
    ('Одноместный', 'Одноместный'))
    room_type = models.CharField(max_length=20, choices=RoomTypeChoices)
    RoomStatusChoices = (
    ('Занят', 'Занят'),
    ('Забронирован', 'Забронирован'),
    ('Свободен', 'Свободен') )
    room_status = models.CharField(max_length=100, choices=RoomStatusChoices, )
    description = models.TextField()

    def __str__(self):
        return f'{self.hotel}, {self.room_number}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    room_image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f'{self.room}, {self.room_image}'


class  Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel}, {self.user}'


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.hotel}, {self.user}, {self.room}'