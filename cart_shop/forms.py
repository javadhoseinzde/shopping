from django import forms
from shop.models import Order
'''class OrderDetialForm(forms.Form):
	username_deliverd = forms.CharField(label=":نام گیرنده")
	phone_number = forms.IntegerField(label=":شماره تماس")
	address = forms.CharField(label="ادرس")
	code = forms.IntegerField(label=":کد پستی")
'''

class OrderDetailForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('username_recive', 'address', 'phone_number', 'code_posti')

