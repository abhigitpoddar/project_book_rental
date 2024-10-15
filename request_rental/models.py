import uuid

from django.contrib.auth.models import User
from django.db import models
from enum import Enum
from rental_service.models import Book


class RequestStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DECLINED = 'Declined'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Create your models here.
class RequestRental(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default=RequestStatus.PENDING.value, choices=RequestStatus.choices())
    approved_on = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
