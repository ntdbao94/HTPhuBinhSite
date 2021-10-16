from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from ThietLapNamHocMoi.models import ThieuNhi

class ThieuNhiResource(resources.ModelResource):
    TenThanh = Field(attribute='TenThanh', column_name='Tên Thánh')
    HoTen = Field(attribute='HoTen', column_name='Họ tên')
    NgaySinh = Field(attribute='NgayRuaToi', widget=DateWidget(format='%d/%m/%Y'), column_name='Ngày sinh')
    NgayRuaToi = Field(attribute='NgayRuaToi', widget=DateWidget(format='%d/%m/%Y'), column_name='Ngày rửa tội')
    TenThanhCha = Field(attribute='TenThanhCha', column_name='Tên Thánh cha')
    HoTenCha = Field(attribute='HoTenCha', column_name='Họ tên cha')
    TenThanhMe = Field(attribute='TenThanhMe', column_name='Tên Thánh mẹ')
    HoTenMe = Field(attribute='HoTenMe', column_name='Họ tên Mẹ')
    DiaChi = Field(attribute='DiaChi', column_name='Địa chỉ')
    KhuDao = Field(attribute='KhuDao', column_name='Khu đạo')
    Sdt1 = Field(attribute='Sdt1', column_name='Số điện thoại 1')
    Sdt2 = Field(attribute='Sdt2', column_name='Số điện thoại 2(nếu có)')

    class Meta:
        model = ThieuNhi
        fields = ('TenThanh', 'HoTen', 'NgaySinh', 'NgayRuaToi', 'TenThanhCha', 'HoTenCha', 'TenThanhMe', 'HoTenMe', 'DiaChi', 'KhuDao', 'Sdt1', 'Sdt2', )