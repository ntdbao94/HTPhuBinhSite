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
from django.core import serializers

def Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi, id_HuynhTruong):
    return ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1, DanhSachHuynhTruong__id_HuynhTruong=id_HuynhTruong, BangDiemThieuNhi__id_ThieuNhi=id_ThieuNhi).exists()

# Create your views here.
class ThieuNhiView(LoginRequiredMixin, View):
    login_url = '/logout/'

    def getByChiaLop(request, id_ChiaLop):
        if request.user.has_perm(VanhanhnamhocConfig.name+'.view_thieunhi') & (PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__id_ChiaLop=id_ChiaLop).exists() | request.user.groups.filter(name='BQT').exists()):
            currentChiaLop = ChiaLop.objects.get(pk=id_ChiaLop)
            list = ThieuNhi.objects.filter(Is_Active__gte=0, CacLopDaHoc=currentChiaLop)
            if request.user.groups.filter(name='BQT').exists():
                listChiaLop = ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1).order_by('DanhMucLop__DoTuoi, DanhMucLop__id_DanhMucLop')
            else:
                listChiaLop = [currentChiaLop]
            return render(request, 'VanHanhNamHoc/ThieuNhiList.html', {"list": list, "listChiaLop": listChiaLop, "currentChiaLop": currentChiaLop})
        return render(request, 'HomePage/404.html')

    def get(self, request):
        return ThieuNhiView.getByChiaLop(request, request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1).id_ChiaLop)

    def create(request):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.add_thieunhi'):
            if request.POST.get('ChiaLop') is None:
                currentChiaLop = request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1)
            else:
                currentChiaLop = ChiaLop.objects.get(pk=request.POST.get('ChiaLop'))
            if request.user.groups.filter(name='BQT').exists():
                listChiaLop = ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1).order_by('DanhMucLop__DoTuoi, DanhMucLop__id_DanhMucLop')
            else:
                listChiaLop = [request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1)]
            if request.method == 'POST':
                form = ThieuNhiForm(request.POST, request=request)
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    if BangDiem.objects.filter(ThieuNhi=ThieuNhi.objects.filter(TenThanh=form.cleaned_data['TenThanh'], HoTen=form.cleaned_data['HoTen'], NgaySinh= str(form.cleaned_data['NgaySinh'])[0:10]).first(), ChiaLop__DanhMucNienKhoa__Is_Active=1).exclude(ChiaLop__id_ChiaLop=request.POST.get('ChiaLop')).exists():
                        messages.info(request, 'Em: ' + savedObj.TenThanh + ' ' + savedObj.HoTen + ', hiện đang học ở lớp khác, vui lòng liên hệ BQT để kiểm tra tình hình học tập')
                    else:
                        savedObj = form.save()
                        objBangDiem = BangDiem.objects.get_or_create(ChiaLop=ChiaLop.objects.get(pk=request.POST.get('ChiaLop')), ThieuNhi=savedObj)
                        objBangDiem[0].Is_Active = savedObj.Is_Active
                        objBangDiem[0].Updated_by = request.user
                        objBangDiem[0].save()
                        return ThieuNhiView.getByChiaLop(request, request.POST.get('ChiaLop'))
            else:
                form = ThieuNhiForm()
            return render(request, 'VanHanhNamHoc/ThieuNhiDetail.html', {'form': form, "listChiaLop": listChiaLop, "currentChiaLop": currentChiaLop})
        return render(request, 'HomePage/404.html')

    def update(request, id_ThieuNhi):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.change_thieunhi') & (Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong) | request.user.groups.filter(name='BQT').exists()):
            objThieuNhi = ThieuNhi.objects.get(pk=id_ThieuNhi)
            if request.POST.get('ChiaLop') is None:
                currentChiaLop = ThieuNhi.objects.get(pk=id_ThieuNhi).CacLopDaHoc.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1)
            else:
                currentChiaLop = ChiaLop.objects.get(pk=request.POST.get('ChiaLop'))
            if request.user.groups.filter(name='BQT').exists():
                listChiaLop = ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1).order_by('DanhMucLop__DoTuoi, DanhMucLop__id_DanhMucLop')
            else:
                listChiaLop = [request.user.CacLopDaDay.get(DanhMucNienKhoa__Is_Active=1, Is_Active=1)]
            if request.method == 'POST':
                form = ThieuNhiForm(request.POST, instance=objThieuNhi, request=request)
                if form.is_valid():
                    savedObj = form.save()
                    objBangDiem = BangDiem.objects.get(ChiaLop__DanhMucNienKhoa__Is_Active=1, ThieuNhi=savedObj)
                    objBangDiem.ChiaLop = ChiaLop.objects.get(pk=request.POST.get('ChiaLop'))
                    objBangDiem.Is_Active = savedObj.Is_Active
                    objBangDiem.Updated_by = request.user
                    objBangDiem.save()
                    return ThieuNhiView.getByChiaLop(request, request.POST.get('ChiaLop'))
            else:
                form = ThieuNhiForm(instance=objThieuNhi)
            return render(request, 'VanHanhNamHoc/ThieuNhiDetail.html', {"form": form, "Old_id_ThieuNhi": id_ThieuNhi, "listChiaLop": listChiaLop, "currentChiaLop": currentChiaLop})
        return render(request, 'HomePage/404.html')

    def delete(request, id_ThieuNhi):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.delete_thieunhi') & Check_HuynhTruong_quan_ly_ThieuNhi(id_ThieuNhi=id_ThieuNhi, id_HuynhTruong=request.user.id_HuynhTruong):
            ThieuNhi.objects.filter(pk=id_ThieuNhi).update(Is_Active=-1, Updated_by=request.user)
            BangDiem.objects.filter(ThieuNhi=id_ThieuNhi).update(Is_Active=-1, Updated_by=request.user)
            return redirect(reverse('VanHanhNamHoc:thieunhi'))
        return render(request, 'HomePage/404.html')

    def upload(request):
        if request.user.has_perm(VanhanhnamhocConfig.name + '.add_thieunhi') & request.user.has_perm(VanhanhnamhocConfig.name + '.change_thieunhi'):
            if request.method == 'POST':
                dataset = Dataset()
                new_ThieuNhi = request.FILES['UploadFile']

                if not new_ThieuNhi.name.endswith('xlsx'):
                    messages.info(request, 'Sai định dạng file, vui lòng chọn file .xlsx')
                else:
                    imported_data = dataset.load(new_ThieuNhi.read(), format='xlsx')
                    for inx, data in enumerate(imported_data):
                        if str(data[1]).isnumeric():
                            try:
                                if data[5] is not None:
                                    datetime.datetime.strptime(str(data[5])[0:10], '%Y-%m-%d')
                                if data[4] is not None:
                                    datetime.datetime.strptime(str(data[4])[0:10], '%Y-%m-%d')
                            except:
                                messages.info(request, 'Sai định dạng ngày tháng tại dòng ' + str(inx + 2) + ', em: ' + data[2] + ' ' + data[3] + ', vui lòng sửa đúng định dạng ngày tháng và import lại')
                                break

                            if ThieuNhi.objects.filter(TenThanh=data[2].title(), HoTen=data[3].title(), NgaySinh= str(data[4])[0:10]).exists():
                                objThieuNhi = ThieuNhi.objects.get(TenThanh=data[2].title().strip(), HoTen=data[3].title().strip(), NgaySinh= str(data[4])[0:10])
                            else:
                                objThieuNhi = ThieuNhi()

                            data = {'TenThanh': data[2], 'HoTen': data[3], 'NgaySinh': str(data[4])[0:10], 'NgayRuaToi': str(data[5])[0:10],
                                    'HoTenCha': data[6], 'HoTenMe': data[7], 'DiaChi': data[8], 'KhuDao': data[9], 'Sdt1': data[10], 'Is_Active': '1',}
                            if objThieuNhi.id_ThieuNhi is not None:
                                data.update({'Is_Active': objThieuNhi.Is_Active})
                            form = ThieuNhiForm(data, instance=objThieuNhi, request=request)
                            if form.is_valid():
                                if BangDiem.objects.filter(ThieuNhi=objThieuNhi, ChiaLop__DanhMucNienKhoa__Is_Active=1).exclude(ChiaLop__id_ChiaLop=request.POST.get('ChiaLop')).exists():
                                    messages.info(request, 'Tại dòng ' + str(inx + 2) + ', em: ' + objThieuNhi.TenThanh + ' ' + objThieuNhi.HoTen + ', hiện đang học ở lớp khác, vui lòng liên hệ BQT để kiểm tra tình hình học tập')
                                else:
                                    savedObj = form.save()
                                    objBangDiem = BangDiem.objects.get_or_create(ChiaLop=request.POST.get('ChiaLop'), ThieuNhi=savedObj)
                                    objBangDiem[0].Is_Active = savedObj.Is_Active
                                    objBangDiem[0].Updated_by = request.user
                                    objBangDiem[0].save()
                return ThieuNhiView.getByChiaLop(request, request.POST.get('ChiaLop'))
        return render(request, 'HomePage/404.html')

    def export(request, id_ChiaLop):
        if request.user.has_perm(VanhanhnamhocConfig.name+'.view_thieunhi') & (PhanCong.objects.filter(HuynhTruong=request.user, ChiaLop__id_ChiaLop=id_ChiaLop).exists() | request.user.groups.filter(name='BQT').exists()):
            resourceThieuNhi = ThieuNhiResource()
            list = ThieuNhi.objects.filter(Is_Active__gte=0, CacLopDaHoc=ChiaLop.objects.get(pk=id_ChiaLop))
            dataset = resourceThieuNhi.export(list)
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="DanhSachThieuNhi.xlsx"'
            return response
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
                    form.save()
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
                    form.save()
            return redirect(reverse('VanHanhNamHoc:diemdanh'))
        else:
            return render(request, 'HomePage/404.html')