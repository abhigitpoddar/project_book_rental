import uuid

from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class Status(Enum):
    FREE='Free'
    PURCHASED='Purchased'
    INACTIVE='Inactive'

    @classmethod
    def choices(cls) -> list:
        return [(key.value, key.name) for key in cls]


def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )


class Book(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    name = models.CharField(max_length=30)
    page = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Rental(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0, validators=[validate_decimals])
    status = models.CharField(default=Status.FREE.value, choices=Status.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
