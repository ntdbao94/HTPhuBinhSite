from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from .models import DanhMucLop, DanhMucNienKhoa, ChiaLop, PhanCong
from django.urls import reverse
from .apps import ThietlapnamhocmoiConfig
from .forms import DanhMucLopForm, DanhMucNienKhoaForm, ChiaLopForm

class DanhMucLopView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.view_danhmuclop'):
            list = DanhMucLop.objects.filter(Is_Active__gte=0)
            return render(request, 'ThietLapNamHocMoi/DanhMucLopList.html', {"list": list})
        return render(request, 'HomePage/404.html')

    def create(request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.add_danhmuclop'):
            if request.method == 'POST':
                form = DanhMucLopForm(request.POST, request=request)
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    return redirect(reverse('ThietLapNamHocMoi:lop'))
            else:
                form = DanhMucLopForm()
            return render(request, 'ThietLapNamHocMoi/DanhMucLopDetail.html', {'form': form})
        return render(request, 'HomePage/404.html')

    def update(request, id_Lop):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.change_danhmuclop'):
            if request.method == 'POST':
                form = DanhMucLopForm(request.POST, instance=DanhMucLop.objects.get(pk=id_Lop), request=request)
                if form.is_valid():
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    return redirect(reverse('ThietLapNamHocMoi:lop'))
            else:
                form = DanhMucLopForm(instance=DanhMucLop.objects.get(pk=id_Lop))
            return render(request, 'ThietLapNamHocMoi/DanhMucLopDetail.html', {"form": form, "Old_id_DanhMucLop": id_Lop})
        return render(request, 'HomePage/404.html')
#
    def delete(request, id_Lop):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.delete_danhmuclop'):
            try:
                DanhMucLop.objects.filter(pk=id_Lop).update(Is_Active=-1)
            except:
                return render(request, 'HomePage/404.html')
            return redirect(reverse('ThietLapNamHocMoi:lop'))
        return render(request, 'HomePage/404.html')

class DanhMucNienKhoaView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.view_danhmucnienkhoa'):
            list = DanhMucNienKhoa.objects.filter(Is_Active__gte=0)
            return render(request, 'ThietLapNamHocMoi/DanhMucNienKhoaList.html', {"list": list})
        return render(request, 'HomePage/404.html')

    def create(request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.add_danhmucnienkhoa'):
            if request.method == 'POST':
                form = DanhMucNienKhoaForm(request.POST, request=request)
                if form.is_valid():
                    if form.data['Is_Active'] == '1':
                        DanhMucNienKhoa.objects.filter(Is_Active__gte=0).update(Is_Active=0)
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    return redirect(reverse('ThietLapNamHocMoi:nienkhoa'))
            else:
                form = DanhMucNienKhoaForm()
            return render(request, 'ThietLapNamHocMoi/DanhMucNienKhoaDetail.html', {'form': form})
        return render(request, 'HomePage/404.html')

    def update(request, id_NienKhoa):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.change_danhmucnienkhoa'):
            if request.method == 'POST':
                form = DanhMucNienKhoaForm(request.POST,instance=DanhMucNienKhoa.objects.get(pk=id_NienKhoa), request=request)
                if form.is_valid():
                    if form.data['Is_Active'] == '1':
                        DanhMucNienKhoa.objects.filter(Is_Active__gte=0).update(Is_Active=0)
                    savedObj = form.save(commit=False)
                    savedObj.Updated_by = request.user
                    savedObj.save()
                    return redirect(reverse('ThietLapNamHocMoi:nienkhoa'))
            else:
                form = DanhMucNienKhoaForm(instance=DanhMucNienKhoa.objects.get(pk=id_NienKhoa))

            return render(request, 'ThietLapNamHocMoi/DanhMucNienKhoaDetail.html', {'form': form, 'Old_id_DanhMucNienKhoa': id_NienKhoa})
        return render(request, 'HomePage/404.html')

    def delete(request, id_NienKhoa):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name+'.delete_danhmucnienkhoa'):
            try:
                DanhMucNienKhoa.objects.filter(pk=id_NienKhoa).update(Is_Active=-1)
            except:
                return render(request, 'HomePage/404.html')
            return redirect(reverse('ThietLapNamHocMoi:nienkhoa'))
        return render(request, 'HomePage/404.html')

class ChiaLopView(LoginRequiredMixin, View):
    login_url = '/logout/'
    def get(self, request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name + '.view_chialop'):
            currentNienKhoa = DanhMucNienKhoa.objects.get(Is_Active=1)
            list = ChiaLop.objects.filter(DanhMucNienKhoa__Is_Active=1,Is_Active__gte=0)\
                        .select_related('DanhMucNienKhoa', 'DanhMucLop', 'ChiDoanTruong').order_by('DanhMucLop__DoTuoi','DanhMucLop__MaLop')
            return render(request, 'ThietLapNamHocMoi/ChiaLopList.html', {"list": list, 'currentNienKhoa':currentNienKhoa})
        return render(request, 'HomePage/404.html')

    def sync(request):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name + '.add_chialop'):
            currentNienKhoa = DanhMucNienKhoa.objects.get(Is_Active=1)
            listLop = DanhMucLop.objects.filter(Is_Active=1)
            ChiaLop.objects.filter(Is_Active__gte=0).update(Is_Active=-1)
            for lop in listLop:
                objChiaLop = ChiaLop.objects.get_or_create(DanhMucNienKhoa=currentNienKhoa, DanhMucLop=lop)
                for ht in objChiaLop[0].DanhSachHuynhTruong.all():
                    ht.CacLopDaDay.exclude(pk=objChiaLop[0].id_ChiaLop).filter(DanhMucLop__in=listLop, ChiaLop__Updated_at__lt=PhanCong.objects.get(HuynhTruong=ht, ChiaLop=objChiaLop[0]).Updated_at).update(ChiDoanTruong=None)
                    PhanCong.objects.filter(HuynhTruong=ht, ChiaLop__DanhMucLop__in=listLop, Updated_at__lt=PhanCong.objects.get(HuynhTruong=ht, ChiaLop=objChiaLop[0]).Updated_at).delete()
                objChiaLop[0].Is_Active=1
                objChiaLop[0].Updated_by = request.user
                objChiaLop[0].save()
            return redirect(reverse('ThietLapNamHocMoi:chialop'))
        return render(request, 'HomePage/404.html')

    def update(request, id_ChiaLop):
        if request.user.has_perm(ThietlapnamhocmoiConfig.name + '.change_chialop'):
            obj = ChiaLop.objects.filter(pk=id_ChiaLop).select_related('DanhMucNienKhoa', 'DanhMucLop')
            if request.method == 'POST':
                form = ChiaLopForm(request.POST, instance=ChiaLop.objects.get(pk=id_ChiaLop), request=request)
                if form.is_valid():
                    savedObj = form.save()
                    savedObj.Updated_by = request.user
                    PhanCong.objects.filter(ChiaLop=savedObj).update(Updated_by = request.user)
                    savedObj.save()
                    return redirect(reverse('ThietLapNamHocMoi:chialop'))
            else:
                form = ChiaLopForm(instance=ChiaLop.objects.get(pk=id_ChiaLop))
            return render(request, 'ThietLapNamHocMoi/ChiaLopDetail.html', {'form': form, 'obj':obj[0]})
        return render(request, 'HomePage/404.html')