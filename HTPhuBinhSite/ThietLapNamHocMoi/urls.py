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

app_name = 'ThietLapNamHocMoi'

urlpatterns = [

    path('viewLop/', views.DanhMucLopView.as_view(), name="lop"),
    path('detailLop/<int:id_Lop>', views.DanhMucLopView.update, name="updatelop"),
    path('detailLop/', views.DanhMucLopView.create, name="createlop"),
    path('deleteLop/<int:id_Lop>', views.DanhMucLopView.delete, name="deletelop"),

    path('viewNienKhoa/', views.DanhMucNienKhoaView.as_view(), name="nienkhoa"),
    path('detailNienKhoa/<int:id_NienKhoa>', views.DanhMucNienKhoaView.update, name="updatenienkhoa"),
    path('detailNienKhoa/', views.DanhMucNienKhoaView.create, name="createnienkhoa"),
    path('deleteNienKhoa/<int:id_NienKhoa>', views.DanhMucNienKhoaView.delete, name="deletenienkhoa"),

    path('viewChiaLop/', views.ChiaLopView.as_view(), name="chialop"),
    path('syncChiaLop/', views.ChiaLopView.sync, name="syncchialop"),
    path('updateChiaLop/<int:id_ChiaLop>', views.ChiaLopView.update, name="updatechialop"),

]
