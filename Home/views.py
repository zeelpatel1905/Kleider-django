from django.shortcuts import render,redirect, get_list_or_404
from .forms import ContactForm, UserForm, ProfileForm, HelpForm, FeedbackForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    template = 'index.html'
    return render(request, template, {})


def contact(request):
    cform = ContactForm(request.POST)
    if request.method == 'POST':
        if cform.is_valid():
            contact_name = cform.cleaned_data['name']
            contact_email = cform.cleaned_data['email']
            content = cform.cleaned_data['content']
            cform.save()
            subject = 'Hello ' + contact_name + ' From Kleider'
            message = "stay connected. we would love to hear from you."
            email_from = settings.EMAIL_HOST_USER
            email_to = [contact_email, ]
            send_mail(subject, message, email_from, email_to)
            return render(request, 'account/msg1.html', {'title': subject, 'content': 'hello'})
        else:
            cform = ContactForm()
    template = 'contact.html'
    return render(request, template, {'form': cform})

def profile(request):
    template = 'profile.html'
    return render(request, template, {})

@login_required
@transaction.atomic
def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profileform.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#Deleteview
def deleteProfile(request, pk):
    template = 'profiledelete.html'
    instance = get_list_or_404(User, pk=pk)
    if request.method =='POST':
        instance.delete()
        return redirect('home')
    return render(request, template, {'object': instance})

def help(request):
    hform = HelpForm(request.POST)
    if request.method == 'POST':
        if hform.is_valid():
            hform.save()
            messages.success(request, 'We recwived your queary.')
            return redirect('help')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        hform = HelpForm()
    template = 'help.html'
    return render(request, template, {'form': hform})

def Feedback(request, template_name='feedback.html'):
    fform = FeedbackForm(request.POST or None, request.FILES or None)
    if fform.is_valid():
        f = fform.save(commit=False)
        f.user = request.user.profile
        f.save()
        return redirect('home')
    else:
        messages.error(request, template_name, {'form': fform})
        fform = FeedbackForm()
    return render(request, template_name, {'form': fform})

def Howitworks(request):
    template = 'howitworks.html'
    return render(request, template, {})

def aboutus(request):
    template = 'aboutus.html'
    return render(request, template, {})

def location(request):
    template = 'location.html'
    return render(request, template, {})