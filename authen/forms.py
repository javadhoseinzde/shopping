from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

class SighUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50, required=False, label="نام")
	last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')
	email = forms.EmailField(max_length=254, label="ایمیل")
	username = forms.CharField(label="یوزرنیم")
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['placeholder'] = 'ایمیل خود را وارد کنید'
		self.fields['first_name'].widget.attrs['placeholder'] = ' نام خود را وارد کید'
		self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی خود را وارد کیند'

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'یوزرنیم خود را وارد کنید'
		self.fields['username'].label=''
		self.fields['username'].help_text='<div class="form-text text-muted"><small>ضروری. 150 کاراکتر یا کمتر. فقط حروف، ارقام و @/./+/-/_. </small></div>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'رمز عبور را وارد کنید'
		self.fields['password1'].label=''
		self.fields['password1'].help_text='<ul class="form-text text-muted small"><li>.رمز عبور شما نمی تواند خیلی شبیه سایر اطلاعات شخصی شما باشد </li><li>.رمز عبور شما باید حداقل 8 کاراکتر داشته باشد</li><li>.رمز عبور شما نمی تواند رمز عبور رایج استفاده شود</li><li>.رمز عبور شما نمی تواند کاملاً عددی باشد</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'رمز عبور را تأیید کنید'
		self.fields['password2'].label=''
		self.fields['password2'].help_text='<div class="form-text text-muted"><small>.برای تایید همان رمز عبور قبلی را وارد کنید</small></div>'

class LoginForm(forms.Form):
	username = forms.CharField(label="یوزرنیم")
	password = forms.CharField(widget=forms.PasswordInput)
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'ایمیل خود را وارد کنید'
		self.fields['password'].widget.attrs['placeholder'] = 'پسورد خود را وارد کنید'
		self.fields['password'].label='پسورد'


class MyPasswordChangeForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
		self.fields["old_password"].label='رمز قدیمی'

		self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
		self.fields["new_password1"].label='رمز جدید'
		self.fields["new_password1"].help_text='<ul class="form-text text-muted small"><li>رمز عبور شما نمی تواند خیلی شبیه سایر اطلاعات شخصی شما باشد</li><li>.رمز عبور شما باید حداقل 8 کاراکتر داشته باشد</li><li>.رمز عبور شما نمی تواند رمز عبور رایج استفاده شود</li><li>.رمز عبور شما نمی تواند کاملاً عددی باشد</li></ul>'
		self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})
		self.fields["new_password2"].label='تکرار رمز جدید'

