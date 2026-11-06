from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name



class Pet(models.Model):

    GENDER_CHOICES = (

        ('Male', 'Male'),

        ('Female', 'Female'),

    )


    name = models.CharField(max_length=100)

    age = models.CharField(
    max_length=50
)

    breed = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='pets/'
    )

    is_adopted = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.name
    
class AdoptionRequest(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE
    )

    message = models.TextField(
        blank=True
    )


    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Rejected', 'Rejected'),

    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return f"{self.user.username} - {self.pet.name}"
    

class PetSubmission(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    STRAY_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    RELATION_CHOICES = (
        ('Owner', 'Owner'),
        ('Friend', 'Friend'),
        ('Neighbour', 'Neighbour'),
        ('Rescued Stray', 'Rescued Stray'),
        ('NGO', 'NGO'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submitted_pets"
    )

    pet_name = models.CharField(max_length=100)

    breed = models.CharField(max_length=100)

    age = models.CharField(
    max_length=50
)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    gender = models.CharField(
        max_length=10,
        choices=Pet.GENDER_CHOICES
    )

    vaccination = models.BooleanField(default=False)

    stray = models.CharField(
        max_length=10,
        choices=STRAY_CHOICES
    )

    relation = models.CharField(
        max_length=30,
        choices=RELATION_CHOICES
    )

    address = models.TextField()

    description = models.TextField()

    image = models.ImageField(
        upload_to="submitted_pets/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pet_name} ({self.status})"

class Contact(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name