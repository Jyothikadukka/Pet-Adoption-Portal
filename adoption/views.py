from django.shortcuts import render
from .models import Pet
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Pet, AdoptionRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PetSubmissionForm
from django.shortcuts import get_object_or_404
from .models import AdoptionRequest, PetSubmission, Pet
from django.contrib.admin.views.decorators import staff_member_required
from .models import Contact


def home(request):
    pets = Pet.objects.all()

    return render(
        request,
        'adoption/home.html',
        {'pets':pets}
    )


def pet_list(request):

    pets = Pet.objects.all()


    # Search
    search = request.GET.get('search')

    if search:

        pets = pets.filter(
            Q(name__icontains=search) |
            Q(breed__icontains=search)
        )


    # Category filter
    category = request.GET.get('category')

    if category:

        pets = pets.filter(
            category__name=category
        )


    # Gender filter
    gender = request.GET.get('gender')

    if gender:

        pets = pets.filter(
            gender=gender
        )


    # Pagination

    paginator = Paginator(
        pets,
        6
    )

    page_number = request.GET.get('page')

    pets = paginator.get_page(
        page_number
    )


    return render(
        request,
        'adoption/pet_list.html',
        {
            'pets': pets
        }
    )

@login_required
def adopt_pet(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )


    if request.method == "POST":

        message = request.POST.get(
            "message"
        )


        AdoptionRequest.objects.create(
            user=request.user,
            pet=pet,
            message=message
        )


        return redirect(
            'home'
        )


    return render(
        request,
        'adoption/adopt.html',
        {
            'pet': pet
        }
    )

def pet_details(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    similar_pets = Pet.objects.filter(
        category=pet.category
    ).exclude(
        id=pet.id
    )[:3]


    return render(
        request,
        'adoption/pet_details.html',
        {
            'pet': pet,
            'similar_pets': similar_pets
        }
    )

@login_required
def dashboard(request):

    requests = AdoptionRequest.objects.filter(
        user=request.user
    ).select_related("pet")

    submitted_pets = PetSubmission.objects.filter(
        owner=request.user
    ).order_by("-submitted_at")
        # Community Activity
    recent_submissions = PetSubmission.objects.all().order_by(
        "-submitted_at"
    )[:6]

    context = {

    "requests": requests,

    "submitted_pets": submitted_pets,


    "recent_submissions": recent_submissions,


    "total_requests": requests.count(),

    "approved": requests.filter(
        status="Approved"
    ).count(),

    "pending": requests.filter(
        status="Pending"
    ).count(),

    "rejected": requests.filter(
        status="Rejected"
    ).count(),
}

    return render(
        request,
        "adoption/dashboard.html",
        context
    )

def contact(request):

    if request.method == "POST":

        Contact.objects.create(

            name=request.POST.get("name"),

            email=request.POST.get("email"),

            message=request.POST.get("message")

        )

        messages.success(
            request,
            "Your message has been sent successfully! 🐾"
        )

        return redirect("contact")

    return render(
        request,
        "adoption/contact.html"
    )

def give_pet(request):

    recent_submissions = PetSubmission.objects.all().order_by(
        "-submitted_at"
    )[:6]


    return render(
        request,
        "adoption/give_pet.html",
        {
            "recent_submissions": recent_submissions
        }
    )
@login_required
def submit_pet(request):

    if request.method == "POST":

        form = PetSubmissionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            pet = form.save(commit=False)

            pet.owner = request.user

            pet.save()


            messages.success(
                request,
                "🐾 Your pet adoption request has been sent successfully! Our team will review it soon."
            )


            return redirect("my_submitted_pets")


    else:

        form = PetSubmissionForm()


    return render(
        request,
        "adoption/submit_pet.html",
        {
            "form": form
        }
    )

@staff_member_required
def approve_pet(request,id):

    submission = get_object_or_404(
        PetSubmission,
        id=id
    )


    Pet.objects.create(

        name=submission.pet_name,

        age=submission.age,

        breed=submission.breed,

        gender=submission.gender,

        category=submission.category,

        description=submission.description,

        image=submission.image,

        is_adopted=False

    )


    submission.status="Approved"

    submission.save()


    messages.success(
        request,
        "Pet approved successfully"
    )


    return redirect(
        "/admin/adoption/petsubmission/"
    )

@staff_member_required
def reject_pet(request,id):

    submission=get_object_or_404(
        PetSubmission,
        id=id
    )


    submission.status="Rejected"

    submission.save()


    messages.warning(
        request,
        "Pet submission rejected"
    )


    return redirect(
        "/admin/adoption/petsubmission/"
    )

@login_required
def my_submitted_pets(request):

    pets = PetSubmission.objects.filter(
        owner=request.user
    ).order_by("-submitted_at")

    return render(
        request,
        "adoption/my_submitted_pets.html",
        {
            "pets": pets
        }
    )