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

class UpdateHTForm(forms.ModelForm):
    class Meta:
        model = HuynhTruong
        fields = ['TenThanh', 'last_name', 'first_name', 'email', 'DiaChi', 'Sdt1', 'Sdt2', 'avatar', 'NgaySinh', 'NgayBonMang']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UpdateHTForm, self).__init__(*args, **kwargs)
        self.fields['TenThanh'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên Thánh...'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Họ và tên lót...'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên...'})
        self.fields['NgaySinh'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Ngày sinh...'})
        self.fields['NgayBonMang'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Ngày bổn mạng...'})
        self.fields['DiaChi'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Địa chỉ...'})
        self.fields['Sdt1'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Số điện thoại 1...'})
        self.fields['Sdt2'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Số điện thoại 2(nếu có)...'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Email...'})

    def clean(self):
        super().clean()
        self.cleaned_data['last_name'] = self.cleaned_data['last_name'].title()
        self.cleaned_data['first_name'] = self.cleaned_data['first_name'].title()
        self.cleaned_data['DiaChi'] = self.cleaned_data['DiaChi'].title()
        if HuynhTruong.objects.filter(email=self.cleaned_data['email']).exclude(pk=self.request.user.id_HuynhTruong).exists():
            return self.add_error('email', 'Email "' + self.cleaned_data['email'] + '" đã được sử dụng bởi huynh trưởng khác, vui lòng nhập lại')


class UpdateLoginInfoForm(forms.Form):
    rpassword = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UpdateLoginInfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên dăng nhập', 'value': self.request.user.username})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Mật khẩu...'})
        self.fields['rpassword'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Nhập lại mật khẩu...'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        rpassword = cleaned_data.get("rpassword")
        username = cleaned_data.get("username")
        if HuynhTruong.objects.filter(username=username).exclude(pk=self.request.user.id_HuynhTruong).exists():
            return self.add_error('username', 'Tên đăng nhập "' + username + '" đã được có người sử dụng, vui lòng nhập lại')
        if password != rpassword:
            return self.add_error('password', 'Mật khẩu nhập không trùng nhau, vui lòng nhập lại')