"""HTPhuBinhSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'VanHanhNamHoc'

urlpatterns = [
    path('viewThieuNhi/', views.ThieuNhiView.as_view(), name="thieunhi"),
    path('viewThieuNhi/<int:id_ChiaLop>', views.ThieuNhiView.getByChiaLop, name="thieunhiByChiaLop"),
    path('detailThieuNhi/<int:id_ThieuNhi>', views.ThieuNhiView.update, name="updatethieunhi"),
    path('detailThieuNhi/', views.ThieuNhiView.create, name="createthieunhi"),
    path('deleteThieuNhi/<int:id_ThieuNhi>', views.ThieuNhiView.delete, name="deletethieunhi"),
    path('uploadThieuNhi/', views.ThieuNhiView.upload, name="uploadthieunhi"),
    path('exportThieuNhi/<int:id_ChiaLop>', views.ThieuNhiView.export, name="exportthieunhi"),

    path('viewBangDiem/', views.BangDiemView.as_view(), name="bangdiem"),
    path('detailBangDiem/<int:id_BangDiem>', views.BangDiemView.update1row, name="updatebangdiem"),

    path('viewDiemDanh/', views.DiemDanhView.as_view(), name="diemdanh"),
    path('detailDiemDanh/', views.DiemDanhView.create, name="creatediemdanh"),
    path('detailDiemDanh/<int:year>/<int:month>/<int:day>', views.DiemDanhView.update, name="updatediemdanh"),
    path('detailDiemDanh/<int:id_ThieuNhi>/<int:id_ChiaLop>', views.DiemDanhView.update1row, name="updatediemdanh1row"),

]
