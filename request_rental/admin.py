from .models import RequestRental, RequestStatus

from django.contrib import admin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString
from rental_service.models import Rental


class RequestRentalAdmin(admin.ModelAdmin):
    model=RequestRental
    list_display = [
        'user',
        'book',
        'status',
        'created_at',
        'approve_request_button_display',
    ]
    readonly_fields = ("book", "status", "user", "approved_on")

    def set_approve_request(self, request: HttpRequest, **kwargs: dict) -> HttpResponseRedirect:
        request_rental_obj = RequestRental.objects.get(id=kwargs["id"])
        rental = Rental.objects.create(
            user=request_rental_obj.user,
            book=request_rental_obj.book,
        )
        rental.save()
        request_rental_obj.status = RequestStatus.APPROVED.value
        request_rental_obj.approved_on = rental.updated_at
        request_rental_obj.save()
        url = reverse("admin:request_rental_requestrental_changelist")
        return HttpResponseRedirect(url)

    def get_urls(self) -> str:
        urls = super().get_urls()
        my_urls = [
            path("approve/<str:id>", self.set_approve_request, name="approve_rental_request")
        ]
        return my_urls + urls

    def approve_request_button_display(self, request_rental_obj: RequestRental) -> SafeString:
        if request_rental_obj.status == RequestStatus.PENDING.value:
            return format_html(
                '<a class="button" style="background: #4E9CAF; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold; color: white; width: 115px; height: 25px;" href="{}">Approve</a>&nbsp;',
                reverse("admin:approve_rental_request", args=(str(request_rental_obj.id),)),
            )
        else:
            return format_html("-")

    def has_add_permission(self, request: HttpRequest, request_rental_obj=None) -> bool:
        return False

    approve_request_button_display.short_description = "ACTION"
    approve_request_button_display.allow_tags = True

# Register your models here.
admin.site.register(RequestRental, RequestRentalAdmin)
