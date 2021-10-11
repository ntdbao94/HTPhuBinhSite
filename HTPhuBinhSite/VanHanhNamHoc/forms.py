from django import forms
from ThietLapNamHocMoi.models import ThieuNhi, BangDiem, DiemDanh
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
        self.fields['Is_Active'].widget.attrs.update({'class': 'bg-white py-2 collapse-inner rounded'})

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

class BangDiemForm(forms.ModelForm):
    class Meta:
        model = BangDiem
        fields = ['DiemKTM_HK1', 'DiemKTV_HK1', 'DiemKT15_HK1', 'DiemKT1T_HK1', 'DiemThi_HK1', 'DiemKTM_HK2', 'DiemKTV_HK2', 'DiemKT15_HK2', 'DiemKT1T_HK2', 'DiemThi_HK2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BangDiemForm, self).__init__(*args, **kwargs)
        self.fields['DiemKTM_HK1'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKTV_HK1'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKT15_HK1'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKT1T_HK1'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemThi_HK1'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKTM_HK2'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKTV_HK2'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKT15_HK2'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemKT1T_HK2'].widget.attrs.update({'min': '0', 'min': '10'})
        self.fields['DiemThi_HK2'].widget.attrs.update({'min': '0', 'min': '10'})

    def clean(self):
        super().clean()
        self.cleaned_data['Updated_by'] = self.request.user


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