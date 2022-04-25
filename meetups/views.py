from django.shortcuts import render, redirect
from .models import Meetup, Participant
from django.views.defaults import page_not_found
from .forms import RegisterationForm

# Create your views here.


def index(request):
    meetups = Meetup.objects.all()
    return render(request, 'meetups/index.html', {
        'meetups': meetups,
    }
                  )


def meetup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == 'GET':
            registration_form = RegisterationForm()
        else:
            registration_form = RegisterationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, _ = Participant.objects.get_or_create(email=user_email)  # _ = was_created but we ignored
                selected_meetup.participants.add(participant)
                return redirect('confirm-register', meetup_slug=meetup_slug)

            else:
                pass
        return render(request, 'meetups/meetups-details.html',
                      {'meetup_title': selected_meetup.title,
                       'meetup_desc': selected_meetup.description,
                       'meetup_slug': selected_meetup.slug,
                       'meetup_location': selected_meetup.location,
                       'meetup_image_url': selected_meetup.image.url,
                       'meetup_organiser': selected_meetup.organiser_email,
                       'form': registration_form,
                       })
    except Exception as exc:
        return page_not_found(request, exc, template_name='404.html')


def confirm_registration(request, meetup_slug):
    try:
        meetup = Meetup.objects.get(slug=meetup_slug)
    except Exception as exc:
        return page_not_found(request, exc, template_name='404.html')

    return render(request, 'meetups/registration-success.html', {'organiser_email': meetup.organiser_email})
