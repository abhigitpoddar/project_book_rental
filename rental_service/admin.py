import os

from .actions import RentalServiceAction
from .models import Book, Rental, Status

from datetime import datetime, timezone
from django.contrib import admin
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.safestring import SafeString
from django.utils.html import format_html
from pytz import timezone


class BookRentalAdmin(admin.ModelAdmin):
    change_list_template = "admin/rental_service/rental/change_list.html"
    model = Rental
    list_display = [
        'user',
        'book',
        'display_amount',
        'created_at',
        'stop_rental_button_display',
    ]
    readonly_fields = ("book", "user", "amount", "status",)
    list_filter = ['user',]

    def set_stop_rental(self, request: HttpRequest, **kwargs: dict) -> HttpResponseRedirect:
        rental_action = RentalServiceAction()
        rental_obj = Rental.objects.get(id=kwargs["id"])
        current_time = datetime.now(timezone(os.environ.get('TIMEZONE')))
        rental_action.refresh_amounts(rental_obj, current_time)
        rental_obj.status = Status.INACTIVE.value
        rental_obj.save()
        url = reverse("admin:rental_service_rental_changelist")
        return HttpResponseRedirect(url)

    def get_urls(self) -> str:
        urls = super().get_urls()
        my_urls = [
            path("refresh_amounts/", self.set_refresh_amounts),
            path("stop/<str:id>", self.set_stop_rental, name="stop_rental")
        ]
        return my_urls + urls

    def set_refresh_amounts(self, request: HttpRequest) -> HttpResponseRedirect:
        url = f"{reverse('admin:index')}rental_service/rental/"
        current_time = datetime.now(timezone(os.environ.get('TIMEZONE')))
        all_rentals = Rental.objects.filter(Q(status=Status.FREE.value) | Q(status=Status.PURCHASED.value))
        rental_action = RentalServiceAction()
        for rent in all_rentals:
            # if (current_time - rent.updated_at).total_seconds() / 60.0 > 1:
            rental_action.refresh_amounts(rent, current_time)
        return HttpResponseRedirect(url)

    def stop_rental_button_display(self, rental_obj: Rental) -> SafeString:
        if rental_obj.status != Status.INACTIVE.value:
            return format_html(
                '<a class="button" style="background: #4E9CAF; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold; color: white; width: 115px; height: 25px;" href="{}">Stop</a>&nbsp;',
                reverse("admin:stop_rental", args=(str(rental_obj.id),)),
            )
        else:
            return format_html("-")

    def has_delete_permission(self, request: HttpRequest, rental_obj=None) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest, rental_obj=None) -> bool:
        return False

    stop_rental_button_display.short_description = "ACTION"
    stop_rental_button_display.allow_tags = True

    def display_amount(self, rental_obj: Rental) -> str:
        return rental_obj.amount

    display_amount.short_description = format_html(
        "<span style='color: gray; font-weight: bold;'>AMOUNT {currency}</span>",
        currency=os.environ.get('CURRENCY'),
    )


# Register your models here.
admin.site.register(Book)
admin.site.register(Rental, BookRentalAdmin)
