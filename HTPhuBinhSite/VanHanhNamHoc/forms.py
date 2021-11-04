from django import forms
from ThietLapNamHocMoi.models import ThieuNhi, BangDiem, DiemDanh, DiemSo
from django.contrib import messages

class ThieuNhiForm(forms.ModelForm):
    class Meta:
        model = ThieuNhi
        fields = ['TenThanh', 'HoTen', 'NgaySinh', 'NgayRuaToi', 'TenThanhCha', 'HoTenCha', 'TenThanhMe', 'HoTenMe', 'DiaChi', 'KhuDao', 'Sdt1', 'Sdt2', 'Is_Active']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ThieuNhiForm, self).__init__(*args, **kwargs)
        self.fields['TenThanh'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên Thánh...'})
        self.fields['HoTen'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Họ và tên...'})
        self.fields['NgaySinh'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Ngày sinh...', 'readonly': 'readonly'})
        self.fields['NgayRuaToi'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Ngày rửa tội...', 'readonly': 'readonly'})
        self.fields['TenThanhCha'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên Thánh cha...'})
        self.fields['HoTenCha'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Họ và tên Cha...'})
        self.fields['TenThanhMe'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Tên Thánh mẹ...'})
        self.fields['HoTenMe'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Họ và tên mẹ...'})
        self.fields['DiaChi'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Địa chỉ...'})
        self.fields['KhuDao'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Khu đạo (nếu có)...'})
        self.fields['Sdt1'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Sdt1...'})
        self.fields['Sdt2'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Sdt2 (nếu có)...'})
        self.fields['Is_Active'].widget.attrs.update({'class': 'form-control form-control-user bg-white py-2 collapse-inner rounded'})

    def clean(self):
        super().clean()
        self.cleaned_data['TenThanh'] = self.cleaned_data['TenThanh'].title().strip()
        self.cleaned_data['HoTen'] = self.cleaned_data['HoTen'].title().strip()
        self.cleaned_data['TenThanhCha'] = self.cleaned_data['TenThanhCha'].title().strip()
        self.cleaned_data['HoTenCha'] = self.cleaned_data['HoTenCha'].title().strip()
        self.cleaned_data['TenThanhMe'] = self.cleaned_data['TenThanhMe'].title().strip()
        self.cleaned_data['HoTenMe'] = self.cleaned_data['HoTenMe'].title().strip()
        self.cleaned_data['DiaChi'] = self.cleaned_data['DiaChi'].title().strip()
        self.cleaned_data['KhuDao'] = self.cleaned_data['KhuDao'].title().strip()
        self.cleaned_data['Updated_by'] = self.request.user
        print(self.cleaned_data['HoTen'] == 'Lại Là Bảo Đây')
        if ThieuNhi.objects.filter(TenThanh=self.cleaned_data['TenThanh'], HoTen=self.cleaned_data['HoTen'], NgaySinh=self.cleaned_data['NgaySinh'], Is_Active=-1).exists():
            messages.info(self.request, 'Thiếu nhi: ' + self.cleaned_data['TenThanh'] + ' ' + self.cleaned_data['HoTen'] + ' đã nghỉ học trước đó, vui lòng liên hệ BQT để kiểm tra tình hình học tập.')
            self.add_error('HoTen', '')


class DiemDanhForm(forms.ModelForm):
    class Meta:
        model = DiemDanh
        fields = ['NgayDiemDanh', 'KetQuaDiemDanh']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DiemDanhForm, self).__init__(*args, **kwargs)
        self.fields['NgayDiemDanh'].widget.attrs.update({'hidden': 'hidden'})

    def clean(self):
        super().clean()
        self.cleaned_data['Updated_by'] = self.request.user


class DiemSoForm(forms.ModelForm):
    class Meta:
        model = DiemSo
        fields = ['HocKy', 'LoaiCotDiem', 'DiemSo']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DiemSoForm, self).__init__(*args, **kwargs)
        self.fields['DiemSo'].widget.attrs.update({'class': 'form-control form-control-sm'})

    def clean(self):
        super().clean()
        self.cleaned_data['Updated_by'] = self.request.user