from django.contrib import admin
from .models import (
    Category,
    Pet,
    AdoptionRequest,
    PetSubmission
)
from django.utils.html import format_html
from django.urls import reverse
from .models import Contact

admin.site.register(Category)

admin.site.register(Pet)

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'pet',
        'status',
        'created_at'
    )


    list_editable = (
        'status',
    )


    search_fields = (
        'user__username',
        'pet__name',
    )

@admin.register(PetSubmission)
class PetSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "pet_name",
        "owner",
        "category",
        "status",
        "submitted_at",
        "approval_actions",
    )


    list_filter = (
        "status",
        "category",
        "gender",
        "stray",
    )


    search_fields = (
        "pet_name",
        "breed",
        "owner__username",
    )


    def approval_actions(self, obj):

        if obj.status == "Pending":

            return format_html(
                '<a class="button" href="{}">Approve</a> '
                '<a class="button" style="background:red;color:white" href="{}">Reject</a>',
                reverse(
                    "approve_pet",
                    args=[obj.id]
                ),
                reverse(
                    "reject_pet",
                    args=[obj.id]
                )
            )

        return obj.status


    approval_actions.short_description = "Actions"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "created_at"
    )

    search_fields = (
        "name",
        "email"
    )