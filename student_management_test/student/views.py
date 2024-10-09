import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Profile
from .forms import ProfileForm  # ModelForm for Profile
from django.contrib import messages

# Initialize logger for view-specific messages
#logger = logging.getLogger('student.views')
logger = logging.getLogger(__name__)

# HOME View
def home(request):
    return render(request, "student/home.html")

# CREATE View
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            try:
                profile = form.save()
                logger.info(f"Profile created successfully: {profile}")
                messages.success(request, 'Profile created successfully!')
                return redirect('profile_list')  # Redirect to profile llist view
            except Exception as e:
                logger.error(f"Error creating profile: {str(e)}")
                messages.error(request, 'An error occurred while creating the profile.')
    else:
        form = ProfileForm()  # Render an empty form for GET request

    return render(request, 'student/profile_form.html', {'form': form})  # Render the template with the form

# READ View (Detail View)
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    logger.info(f"Viewed profile: {profile}")
    return render(request, 'student/profile_detail.html', {'profile': profile})  # Render the profile detail template

# UPDATE View
def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Profile updated successfully: {profile}")
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile_list')  # Redirect to profile llist view
            except Exception as e:
                logger.error(f"Error updating profile: {str(e)}")
                messages.error(request, 'An error occurred while updating the profile.')
    else:
        form = ProfileForm(instance=profile)  # Load the form with the existing profile data

    return render(request, 'student/profile_form.html', {'form': form, 'profile': profile})

# DELETE View
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':  # Confirm the delete action via POST
        try:
            profile.delete()
            logger.info(f"Profile deleted successfully: {profile}")
            messages.success(request, 'Profile deleted successfully!')
            return redirect('profile_list')  # Redirect to the profile list page after deletion
        except Exception as e:
            logger.error(f"Error deleting profile: {str(e)}")
            messages.error(request, 'An error occurred while deleting the profile.')

    return render(request, 'student/profile_confirm_delete.html', {'profile': profile})

# LIST View
def profile_list(request):
    profiles = Profile.objects.all()  # Get all profiles
    logger.info(f"Listing all profiles. Total: {profiles.count()}")
    return render(request, 'student/profile_list.html', {'profiles': profiles})
