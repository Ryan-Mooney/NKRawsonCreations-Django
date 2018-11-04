from django import forms

class ProductFilterForm(forms.Form):
	input_type='checkbox'
	clothes=forms.BooleanField(required=False)
	dresses=forms.BooleanField(required=False)
	shirts=forms.BooleanField(required=False)
	crafts=forms.BooleanField(required=False)

class ContactMailer(forms.Form):
	from_address=forms.EmailField(required=True)
	message=forms.CharField(max_length=1000)