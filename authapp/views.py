from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.conf import settings

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import ShopUser as User


class Login(LoginView):
    form_class = UserLoginForm
    template_name = 'authapp/login.html'


class Register(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    success_message = 'Successfully registered! Check your mailbox for ' \
                      'activation code.'

    def form_valid(self, form, *args, **kwargs):
        user = form.save()
        verify_link = reverse('auth:verify',
                              args=[user.email, user.activation_key])
        email = EmailMessage(
            subject='Verification mail',
            body=(
                f'To activate your account {user.username} at '
                f'{settings.DOMAIN_NAME} please click the next link:\n'
                f'{settings.DOMAIN_NAME}{verify_link}'
            ),
            from_email=settings.EMAIL_HOST_USER,
            to=(user.email,),
        )
        email.send(fail_silently=False)
        return super(Register, self).form_valid(form)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES,
                               instance=request.user)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile edited successfully.')
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'authapp/profile.html', context)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user.activation_key == activation_key and \
            not user.is_activation_key_expired():
        user.is_active = True
        user.save()
    context = {'user': user}
    return render(request, 'authapp/verification.html', context)
