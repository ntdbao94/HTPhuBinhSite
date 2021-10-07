from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

Active_Choice = [
    (1, 'Đang sử dụng'),
    (0, 'Không còn sử dụng')
]

class BaseModel(models.Model):
    class Meta:
        abstract = True
    Is_Active = models.IntegerField(choices=Active_Choice, default=1)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    Updated_by = models.ForeignKey('ThietLapNamHocMoi.HuynhTruong', on_delete=models.SET_NULL, null=True, default=None)

# Create your models here.
class HuynhTruong(AbstractUser):
    class Meta:
        db_table = "table_HuynhTruong"
        ordering = ["NgaySinh", "id_HuynhTruong"]

    id_HuynhTruong = models.AutoField(primary_key=True)
    TenThanh = models.CharField(max_length=45, blank=True, default='')
    NgaySinh = models.DateField(blank=True, null=True)
    NgayBonMang = models.DateField(blank=True, null=True)
    DiaChi = models.CharField(max_length=100, blank=True, default='')
    Sdt1 = models.CharField(max_length=15, blank=True, default='')
    Sdt2 = models.CharField(max_length=15, blank=True, default='')
    Updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='%Y/%m', default=None, blank=True)
    CacLopDaDay = models.ManyToManyField('ChiaLop', related_name='CacLopDaDay', through='PhanCong', through_fields=('HuynhTruong', 'ChiaLop'))

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class DanhMucNienKhoa(BaseModel):
    class Meta:
        db_table = "table_DanhMucNienKhoa"
        ordering = ["-NamBatDau", "-NamKetThuc"]
    id_DanhMucNienKhoa = models.AutoField(primary_key=True)
    NamBatDau = models.IntegerField()
    NamKetThuc = models.IntegerField()
    ChuDeNamHoc = models.CharField(max_length=255, default='')
    BaiHatChuDe = models.CharField(max_length=45, blank=True, default='')
    KhauHieuNamHoc = models.CharField(max_length=255, blank=True, default='')
    CacLopTrongNienKhoa = models.ManyToManyField('DanhMucLop', related_name='CacLopTrongNienKhoa', through='ChiaLop')


class DanhMucLop(BaseModel):
    class Meta:
        db_table = "table_DanhMucLop"
        ordering = ["DoTuoi", "MaLop"]
        unique_together = [["MaLop","Is_Active"]]
    id_DanhMucLop= models.AutoField(primary_key=True)
    MaLop = models.CharField(max_length=45, default='')
    TenLop = models.CharField(max_length=45, default='')
    DoTuoi = models.IntegerField(default=0)
    CacNienKhoaTungTaoLop = models.ManyToManyField(DanhMucNienKhoa, related_name='CacNienKhoaTungTaoLop', through='ChiaLop')


class ChiaLop(BaseModel):
    class Meta:
        db_table = "table_ChiaLop"
        unique_together = (("DanhMucNienKhoa", "DanhMucLop"),)
    id_ChiaLop = models.AutoField(primary_key=True)
    DanhMucNienKhoa = models.ForeignKey(DanhMucNienKhoa, on_delete=models.CASCADE, related_name='DanhMucNienKhoa')
    DanhMucLop = models.ForeignKey(DanhMucLop, on_delete=models.CASCADE, related_name='DanhMucLop')
    ChiDoanTruong = models.ForeignKey(HuynhTruong, on_delete=models.SET_NULL, related_name='ChiDoanTruong', null=True)
    DanhSachHuynhTruong = models.ManyToManyField(HuynhTruong, related_name='DanhSachHuynhTruong', through='PhanCong', through_fields=('ChiaLop', 'HuynhTruong'), blank=True)
    BangDiemThieuNhi = models.ManyToManyField('ThietLapNamHocMoi.ThieuNhi', related_name='BangDiemThieuNhi', through='BangDiem', through_fields=('ChiaLop', 'ThieuNhi'), blank=True)
    ChuyenCanThieuNhi = models.ManyToManyField('ThietLapNamHocMoi.ThieuNhi', related_name='ChuyenCanThieuNhi', through='DiemDanh', through_fields=('ChiaLop', 'ThieuNhi'), blank=True)


class PhanCong(BaseModel):
    class Meta:
        db_table = "table_PhanCong"
        unique_together = (("ChiaLop", "HuynhTruong"),)

    id_PhanCong = models.AutoField(primary_key=True)
    ChiaLop = models.ForeignKey(ChiaLop, on_delete=models.CASCADE, related_name='ChiaLop')
    HuynhTruong = models.ForeignKey(HuynhTruong, on_delete=models.CASCADE, related_name='HuynhTruong')


class ThieuNhi(BaseModel):
    class Meta:
        db_table = "table_ThieuNhi"

    id_ThieuNhi = models.AutoField(primary_key=True)
    TenThanh = models.CharField(max_length=45, blank=True, default='')
    HoTen = models.CharField(max_length=100, blank=True, default='')
    NgaySinh = models.DateField(blank=True, null=True)
    NgayRuaToi = models.DateField(blank=True, null=True)
    TenThanhCha = models.CharField(max_length=45, blank=True, default='')
    HoTenCha = models.CharField(max_length=100, blank=True, default='')
    TenThanhMe = models.CharField(max_length=45, blank=True, default='')
    HoTenMe = models.CharField(max_length=100, blank=True, default='')
    DiaChi = models.CharField(max_length=100, blank=True, default='')
    KhuDao = models.CharField(max_length=45, blank=True, default='')
    Sdt1 = models.CharField(max_length=15, blank=True, default='')
    Sdt2 = models.CharField(max_length=15, blank=True, default='')
    CacLopDaHoc = models.ManyToManyField(ChiaLop, related_name='CacLopDaHoc', through='BangDiem', through_fields=('ThieuNhi', 'ChiaLop'), blank=True)
    ThongTinChuyenCan = models.ManyToManyField(ChiaLop, related_name='ThongTinChuyenCan', through='DiemDanh', through_fields=('ThieuNhi', 'ChiaLop'), blank=True)
    Active_Choice = [(1, 'Đang học'), (0, 'Đang tạm nghỉ')]
    Is_Active = models.IntegerField(choices=Active_Choice, default=1)

    def __str__(self):
        return self.HoTen


class BangDiem(BaseModel):
    class Meta:
        db_table = "table_BangDiem"

    id_BangDiem = models.AutoField(primary_key=True)
    ChiaLop = models.ForeignKey(ChiaLop, on_delete=models.CASCADE, related_name='ChiaLop_BangDiem')
    ThieuNhi = models.ForeignKey(ThieuNhi, on_delete=models.CASCADE, related_name='ThieuNhi')
    DiemKTM_HK1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKTV_HK1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKT15_HK1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKT1T_HK1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemThi_HK1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKTM_HK2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKTV_HK2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKT15_HK2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemKT1T_HK2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    DiemThi_HK2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])


class DiemDanh(BaseModel):
    class Meta:
        db_table = "table_DiemDanh"

    id_DiemDanh = models.AutoField(primary_key=True)
    ChiaLop = models.ForeignKey(ChiaLop, on_delete=models.CASCADE, related_name='ChiaLop_DiemDanh')
    ThieuNhi = models.ForeignKey(ThieuNhi, on_delete=models.CASCADE, related_name='ThieuNhi_DiemDanh')
    NgayDiemDanh = models.DateField()
    KetQuaDiemDanh = models.CharField(choices=[('C', 'Có mặt'), ('P', 'Vắng có phép'), ('V', 'Vắng không phép')], null=True, max_length=1)