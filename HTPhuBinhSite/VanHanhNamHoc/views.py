from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from ThietLapNamHocMoi.apps import ThietlapnamhocmoiConfig as VanhanhnamhocConfig
from ThietLapNamHocMoi.models import ThieuNhi, BangDiem, ChiaLop, PhanCong, DiemDanh
from .forms import ThieuNhiForm, BangDiemForm, DiemDanhForm
import pandas, datetime
from .resources import ThieuNhiResource
from tablib import Dataset
from django.contrib import messages

def Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi, id_HuynhTruong):
    return ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1, DanhSachHuynhTruong__id_HuynhTruong=id_HuynhTruong, BangDiemThieuNhi__id_ThieuNhi=id_ThieuNhi).exists()

# Create your views here.
class ThieuNhiView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(VanhanhnamhocConfig.name+'.view_thieunhi') & PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__DanhMucNienKhoa__Is_Active=1).exists():
            currentPhanCong = PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__DanhMucNienKhoa__Is_Active=1).select_related('ChiaLop__DanhMucNienKhoa', 'ChiaLop__DanhMucLop')
            list = ThieuNhi.objects.filter(Is_Active__gte=0,CacLopDaHoc__DanhSachHuynhTruong__id_HuynhTruong=request.user.id_HuynhTruong)
            return render(request, 'VanHanhNamHoc/ThieuNhiList.html', {"list": list, "currentPhanCong": currentPhanCong})
        return render(request, 'HomePage/404.html')

    def create(request):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.add_thieunhi'):
            if request.method == 'POST':
                form = ThieuNhiForm(request.POST, request=request)
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    objBangDiem = BangDiem.objects.get_or_create(ChiaLop=request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1), ThieuNhi=savedObj)
                    objBangDiem[0].Is_Active = savedObj.Is_Active
                    objBangDiem[0].Updated_by = request.user
                    objBangDiem[0].save()
                    return redirect(reverse('VanHanhNamHoc:thieunhi'))
            else:
                form = ThieuNhiForm()
            return render(request, 'VanHanhNamHoc/ThieuNhiDetail.html', {'form': form})
        return render(request, 'HomePage/404.html')

    def update(request, id_ThieuNhi):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.change_thieunhi') & Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong):
            thieunhi = ThieuNhi.objects.get(pk=id_ThieuNhi)
            if request.method == 'POST':
                form = ThieuNhiForm(request.POST, instance=thieunhi, request=request)
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    objBangDiem = BangDiem.objects.get_or_create(ChiaLop=request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1), ThieuNhi=savedObj)
                    objBangDiem[0].Is_Active = savedObj.Is_Active
                    objBangDiem[0].Updated_by = request.user
                    objBangDiem[0].save()
                    return redirect(reverse('VanHanhNamHoc:thieunhi'))
            else:
                form = ThieuNhiForm(instance=thieunhi)
            return render(request, 'VanHanhNamHoc/ThieuNhiDetail.html', {"form": form, "Old_id_ThieuNhi": id_ThieuNhi})
        return render(request, 'HomePage/404.html')

    def delete(request, id_ThieuNhi):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.delete_thieunhi') & Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong):
            ThieuNhi.objects.filter(pk=id_ThieuNhi).update(Is_Active=-1, Updated_by=request.user)
            BangDiem.objects.filter(ThieuNhi=id_ThieuNhi).update(Is_Active=-1, Updated_by=request.user)
            return redirect(reverse('VanHanhNamHoc:thieunhi'))
        return render(request, 'HomePage/404.html')

    def upload(request):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.add_thieunhi'):
            if request.method == 'POST':
                thieunhiResouce = ThieuNhiResource()
                dataset = Dataset()
                new_ThieuNhi = request.FILES['UploadFile']

                if not new_ThieuNhi.name.endswith('xlsx'):
                    messages.info(request, 'Sai định dạng file, vui lòng chọn file .xlsx')
                else:
                    imported_data = dataset.load(new_ThieuNhi.read(), format='xlsx')
                    for data in imported_data:
                        print(data)
                        thieunhiResouce.import_data(dataset)
                return ThieuNhiView.get(ThieuNhiView, request)
        return render(request, 'HomePage/404.html')

class BangDiemView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(VanhanhnamhocConfig.name+'.view_bangdiem') & PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__DanhMucNienKhoa__Is_Active=1).exists():
            currentPhanCong = PhanCong.objects.filter(HuynhTruong=request.user,ChiaLop__DanhMucNienKhoa__Is_Active=1).select_related('ChiaLop__DanhMucNienKhoa', 'ChiaLop__DanhMucLop')
            listinfo = BangDiem.objects.filter(ChiaLop__DanhMucNienKhoa__Is_Active__gte=0, Is_Active__gte=0, ChiaLop__DanhSachHuynhTruong__id_HuynhTruong=request.user.id_HuynhTruong).select_related("ThieuNhi")
            list = []
            for item in listinfo:
                list.append({'info': item ,'form': BangDiemForm(instance=item, request=request)})
            return render(request, 'VanHanhNamHoc/BangDiemList.html', {"list": list, 'currentPhanCong': currentPhanCong})
        return render(request, 'HomePage/404.html')

    def update1row(request, id_BangDiem):
        objBangDiem = BangDiem.objects.get(pk=id_BangDiem)
        if request.user.has_perm(VanhanhnamhocConfig.name + '.change_bangdiem') & Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=objBangDiem.ThieuNhi.id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong):
            form = BangDiemForm(request.POST, instance=objBangDiem, request=request)
            if request.method == 'POST':
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
            return redirect(reverse('VanHanhNamHoc:bangdiem'))
        else:
            return render(request, 'HomePage/404.html')


class DiemDanhView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(VanhanhnamhocConfig.name+'.view_diemdanh') & PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__DanhMucNienKhoa__Is_Active=1).exists():
            currentPhanCong = PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__DanhMucNienKhoa__Is_Active=1).select_related('ChiaLop__DanhMucNienKhoa', 'ChiaLop__DanhMucLop')
            list = DiemDanh.objects.filter(Is_Active__gte=0
                                           , ChiaLop__DanhMucNienKhoa__Is_Active__gte=0
                                           , ChiaLop__DanhSachHuynhTruong__id_HuynhTruong=request.user.id_HuynhTruong).exclude(KetQuaDiemDanh=None).order_by('NgayDiemDanh', 'ThieuNhi__id_ThieuNhi')\
                .values('ThieuNhi__id_ThieuNhi', 'ThieuNhi__TenThanh', 'ThieuNhi__HoTen', 'NgayDiemDanh', 'KetQuaDiemDanh')
            data = pandas.DataFrame(list)
            data = data.rename(columns={'ThieuNhi__id_ThieuNhi': 'Id Thiếu Nhi', 'ThieuNhi__TenThanh': 'Tên Thánh', 'ThieuNhi__HoTen': 'Họ và tên'
                                        , 'NgayDiemDanh': 'Ngày điểm danh'
                                        })
            data['Ngày điểm danh'] = pandas.to_datetime(data['Ngày điểm danh'])
            data['Tháng'] = data['Ngày điểm danh'].dt.strftime('%Y-%m')
            data['Ngày điểm danh'] = '<a href="' + reverse('VanHanhNamHoc:creatediemdanh') + data['Ngày điểm danh'].dt.strftime('%Y/%m/%d') + '">' + data['Ngày điểm danh'].dt.strftime('%d/%m/%Y') + '</a>'
            # set color for KetQuaDiemDanh
            colors = {'C': '#1cc88a', 'P': '#f6c23e', 'V': '#e74a3b'}
            data['KetQuaDiemDanh'] = '<b style="color:' + data['KetQuaDiemDanh'].apply(lambda x: colors[x]) + ';">' + data['KetQuaDiemDanh'] + '</b>'
            pivot = pandas.pivot_table(data, index=['Id Thiếu Nhi', 'Tên Thánh', 'Họ và tên'], columns=['Tháng', 'Ngày điểm danh'], values='KetQuaDiemDanh'
                                        , observed=False, aggfunc='min', fill_value='').reset_index(level=0, drop=True)
            return render(request, 'VanHanhNamHoc/DiemDanhList.html', {"list": pivot.to_html(classes='table table-bordered',escape=False), "currentPhanCong": currentPhanCong})
        return render(request, 'HomePage/404.html')

    def create(request):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.add_diemdanh'):
            currentPhanCong = PhanCong.objects.filter(HuynhTruong=request.user,ChiaLop__DanhMucNienKhoa__Is_Active=1).select_related('ChiaLop__DanhMucNienKhoa', 'ChiaLop__DanhMucLop')
            return render(request, 'VanHanhNamHoc/DiemDanhDetail.html', {'currentPhanCong': currentPhanCong})
        return render(request, 'HomePage/404.html')

    def update(request, year, month, day):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.change_diemdanh'):
            if request.method == 'POST':
                pass
            else:
                currentPhanCong = PhanCong.objects.filter(HuynhTruong=request.user,ChiaLop__DanhMucNienKhoa__Is_Active=1).select_related('ChiaLop__DanhMucNienKhoa', 'ChiaLop__DanhMucLop')
                listinfo = BangDiem.objects.filter(ChiaLop__DanhMucNienKhoa__Is_Active__gte=0, Is_Active__gte=0, ChiaLop__DanhSachHuynhTruong__id_HuynhTruong=request.user.id_HuynhTruong).select_related("ThieuNhi")
                list = []
                for item in listinfo:
                    objDiemDanh = DiemDanh.objects.get_or_create(ChiaLop=item.ChiaLop, ThieuNhi=item.ThieuNhi, NgayDiemDanh= datetime.date(year, month, day))
                    list.append({'info': item, 'form': DiemDanhForm(instance=objDiemDanh[0], request=request)})
            return render(request, 'VanHanhNamHoc/DiemDanhDetail.html', {"list": list, 'currentPhanCong': currentPhanCong, 'NgayDiemDanh':datetime.date(year, month, day).strftime('%d/%m/%Y')})
        return render(request, 'HomePage/404.html')

    def update1row(request, id_ThieuNhi, id_ChiaLop):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.change_diemdanh') & Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong):
            objDiemDanh = DiemDanh.objects.get_or_create(ChiaLop=ChiaLop.objects.get(pk=id_ChiaLop), ThieuNhi=ThieuNhi.objects.get(pk=id_ThieuNhi), NgayDiemDanh=request.POST.get('NgayDiemDanh'))
            form = DiemDanhForm(request.POST, instance=objDiemDanh[0], request=request)
            if request.method == 'POST':
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
            return redirect(reverse('VanHanhNamHoc:diemdanh'))
        else:
            return render(request, 'HomePage/404.html')