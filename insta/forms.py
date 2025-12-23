from insta.models import customusermodel,Post,Comment
from django import forms
class userinfoform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    agree=forms.BooleanField(required=True)
    class Meta:
        model=customusermodel
        fields=['first_name','last_name','username','email','password']
    
    def clean(self):
        cleaned_data=super().clean()
        p1=cleaned_data.get('password')
        p2=cleaned_data.get('confirm_password')

        if p1 and p2 and p1!=p2:
            raise forms.ValidationError("Password did'nt match")

        return cleaned_data

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        
        return user
   
    
class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['text','image']

class commentform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
