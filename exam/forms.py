from django import forms


class CandidateForm(forms.Form):
    name = forms.CharField(max_length=120, label="Full name", widget=forms.TextInput(attrs={"placeholder": "Enter your full name"}))
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={"placeholder": "name@example.com"}))
