from django import forms
from .models import DanhMucLop, DanhMucNienKhoa, ChiaLop, HuynhTruong
import datetime


def Year_Choice():
    return [(r, r) for r in range(datetime.date.today().year - 5, datetime.date.today().year+5)]

def current_year():
    return datetime.date.today().year

class DanhMucLopForm(forms.ModelForm):
    class Meta:
        model = DanhMucLop
        fields = ['MaLop', 'TenLop', 'DoTuoi', 'Is_Active', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DanhMucLopForm, self).__init__(*args, **kwargs)
        self.fields['MaLop'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Mã lớp...'})
        self.fields['TenLop'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Tên lớp...'})
        self.fields['DoTuoi'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Độ tuổi...'})
        self.fields['Is_Active'].widget.attrs.update({'class' : 'bg-white py-2 collapse-inner rounded'})

    def clean(self):
        cleaned_data = super().clean()
        id_DanhMucLop = self.instance.id_DanhMucLop
        MaLop = cleaned_data.get("MaLop")
        self.cleaned_data['Updated_by'] = self.request.user
        if DanhMucLop.objects.filter(MaLop=MaLop, Is_Active__gte=0).exclude(pk=id_DanhMucLop).exists():
            self.add_error('MaLop', 'Mã lớp "' + MaLop + '" đã tồn tại, vui lòng sử dụng mã khác')


class DanhMucNienKhoaForm(forms.ModelForm):
    NamBatDau = forms.TypedChoiceField(coerce=int, choices=Year_Choice, initial=current_year)
    NamKetThuc = forms.TypedChoiceField(coerce=int, choices=Year_Choice, initial=current_year)

    class Meta:
        model = DanhMucNienKhoa
        fields = ['NamBatDau', 'NamKetThuc', 'ChuDeNamHoc', 'BaiHatChuDe', 'KhauHieuNamHoc', 'Is_Active']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DanhMucNienKhoaForm, self).__init__(*args, **kwargs)
        self.fields['NamBatDau'].widget.attrs.update({'class' : 'bg-white py-2 collapse-inner rounded'})
        self.fields['NamKetThuc'].widget.attrs.update({'class' : 'bg-white py-2 collapse-inner rounded'})
        self.fields['ChuDeNamHoc'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Chủ đề năm học...'})
        self.fields['BaiHatChuDe'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Bài hát chủ đề...'})
        self.fields['KhauHieuNamHoc'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder': 'Khâu hiệu năm học...'})
        self.fields['Is_Active'].widget.attrs.update({'class' : 'bg-white py-2 collapse-inner rounded'})

    def clean(self):
        cleaned_data = super().clean()
        id_DanhMucNienKhoa = self.instance.id_DanhMucNienKhoa
        NamBatDau = cleaned_data.get("NamBatDau")
        NamKetThuc = cleaned_data.get("NamKetThuc")
        self.cleaned_data['Updated_by'] = self.request.user

        if NamBatDau and NamKetThuc:
            if NamBatDau >= NamKetThuc:
                self.add_error('NamBatDau', 'Năm bắt đầu phải nhỏ hơn năm kết thúc, vui lòng nhập lại')
        if DanhMucNienKhoa.objects.filter(NamBatDau=NamBatDau, NamKetThuc=NamKetThuc, Is_Active__gte=0).exclude(pk=id_DanhMucNienKhoa).exists():
                self.add_error('NamBatDau', 'Năm học '+str(NamBatDau)+'-'+str(NamKetThuc)+' đã tồn tại, vui lòng nhập năm học khác')


class ChiaLopForm(forms.ModelForm):
    class Meta:
        model = ChiaLop
        fields = ['ChiDoanTruong', 'DanhSachHuynhTruong']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChiaLopForm, self).__init__(*args, **kwargs)
        self.fields['ChiDoanTruong'].widget.attrs.update({'data-placeholder': 'Phân công huynh trưởng...', 'class':'bg-white py-2 collapse-inner rounded chosen-select'})
        self.fields['DanhSachHuynhTruong'].widget.attrs.update({'data-placeholder': 'Phân công huynh trưởng...', 'class':'form-control form-control-user chosen-select'})
        HuynhTruongChuaPhanCong = HuynhTruong.objects.filter(is_active=1, is_superuser=0).exclude(pk__in=HuynhTruong.objects.exclude(CacLopDaDay__pk=self.instance.id_ChiaLop)
                                                                                                  .filter(CacLopDaDay__DanhMucNienKhoa__Is_Active=1, CacLopDaDay__Is_Active=1))
        self.fields['ChiDoanTruong'].queryset = HuynhTruongChuaPhanCong
        self.fields['DanhSachHuynhTruong'].queryset = HuynhTruongChuaPhanCong


    def clean(self):
        cleaned_data = super().clean()
        DanhSachHuynhTruong = cleaned_data.get('DanhSachHuynhTruong')
        ChiDoanTruong = cleaned_data.get('ChiDoanTruong')
        self.cleaned_data['Updated_by'] = self.request.user

        if not HuynhTruong.objects.filter(pk__in=DanhSachHuynhTruong,pk=ChiDoanTruong.id_HuynhTruong).exists():
            self.cleaned_data['DanhSachHuynhTruong'] = DanhSachHuynhTruong | HuynhTruong.objects.filter(pk=ChiDoanTruong.id_HuynhTruong)
