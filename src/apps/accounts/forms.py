from django import forms

from apps.accounts.models import Profile


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('پسوورد مشترک نیست')
        else:
            return password




class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())





class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Phone Number', widget=forms.TextInput(),required=False)
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(),required=False)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(),required=False)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(),required=False)
    address = forms.CharField(label='Address', widget=forms.TextInput(),required=False)


    bio = forms.CharField(label='Bio', widget=forms.Textarea(),required=False)


    class Meta:
        model = Profile
        fields = ['bio',]

    def __init__(self, *args, **kwargs):
        # به دست آوردن پروفایل و کاربر مربوطه
        profile = kwargs.get('instance')  # دریافت پروفایل فعلی
        user = profile.user if profile else None  # دریافت کاربر مربوط به پروفایل
        super().__init__(*args, **kwargs)

        # پر کردن فیلدهای User با مقادیر موجود
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)

        # ذخیره تغییرات در پروفایل
        if commit:
            profile.save()

        # ذخیره تغییرات در مدل User
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        return profile



