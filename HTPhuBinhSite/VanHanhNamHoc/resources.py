from import_export import resources
from ThietLapNamHocMoi.models import ThieuNhi

class ThieuNhiResource(resources.ModelResource):
    class meta:
        model = ThieuNhi
        fields = ('TenThanh', 'HoTen', 'NgaySinh', 'NgayRuaToi', 'HoTenCha', 'HoTenMe', 'DiaChi', 'KhuDao', 'Sdt1', 'Sdt2', )