from django import forms
from ThietLapNamHocMoi.models import HuynhTruong

class RegistrationForm(forms.ModelForm):
    rpassword = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = HuynhTruong
        fields = ['TenThanh', 'last_name', 'email', 'password']
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['TenThanh'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên Thánh...'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Họ và tên...'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Email...'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Mật khẩu...'})
        self.fields['rpassword'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Nhập lại mật khẩu...'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        rpassword = cleaned_data.get("rpassword")
        email = cleaned_data.get("email")
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].title()
        self.cleaned_data['first_name'] = self.cleaned_data['last_name'][self.cleaned_data['last_name'].rfind(' ', 0) + 1:]
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'][0:self.cleaned_data['last_name'].rfind(' ', 0)]
        if password != rpassword:
            return self.add_error('password', 'Mật khẩu nhập không trùng nhau, vui lòng nhập lại')
        if HuynhTruong.objects.filter(email=email).exists():
            return self.add_error('email', 'Email "' + email + '" đã được đăng ký, vui lòng nhập lại')