from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, User


class RegisterForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'لطفا فیلد نام کاربری را کامل کنید'})
    email = forms.EmailField(error_messages={'required': 'لطفا فیلد ایمیل را کامل کنید'})
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))
    password_2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm password'}))

    def clean_password_2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_2'] and cd['password'] != cd['password_2']:
            raise forms.ValidationError('پسورد همخوانی ندارد')
        return cd['password_2']


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': 'لطفا فیلد ایمیل را کامل کنید'})
    password = forms.CharField(error_messages={'required': 'لطفا فیلد پسورد را کامل کنید'}, widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'bank_card_num', 'shaba_num']

    # def clean(self):
    #     cleaned_data = super(ProfileForm, self).clean()
    #     name = cleaned_data.get('name')
    #     last_name = cleaned_data.get('last_name')
    #     bank_card_num = cleaned_data.get('bank_card_num')
    #     shaba_num = cleaned_data.get('shaba_num')
    #     if name is None or last_name is None or bank_card_num is None or shaba_num is None:
    #         raise forms.ValidationError('لطفا همه فیلد هارا کامل کنید')
    #     return self.cleaned_data


class IdCardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id_card']


class BankCardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bank_card_pic']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class EmailResetPassword(forms.Form):
    email = forms.EmailField()


class PasswordResetForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput())
    password_2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')
        if password_1 and password_2 and password_1 != password_2:
            self._errors['password_1'] = self.error_class(['پسورد همخوانی ندارد'])
        return self.cleaned_data


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']


class SmsCodeForm(forms.Form):
    code = forms.CharField(max_length=4)
