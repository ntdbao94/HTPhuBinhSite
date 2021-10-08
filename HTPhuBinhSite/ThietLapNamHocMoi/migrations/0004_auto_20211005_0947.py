# Generated by Django 3.2.7 on 2021-10-05 02:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ThietLapNamHocMoi', '0003_auto_20211003_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKT15_HK1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKT15_HK2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKT1T_HK1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKT1T_HK2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKTM_HK1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKTM_HK2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKTV_HK1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemKTV_HK2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemThi_HK1',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='bangdiem',
            name='DiemThi_HK2',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AlterField(
            model_name='thieunhi',
            name='Is_Active',
            field=models.IntegerField(choices=[(1, 'Đang học'), (0, 'Đang tạm nghỉ')], default=1),
        ),
        migrations.CreateModel(
            name='DiemDanh',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_DiemDanh', models.AutoField(primary_key=True, serialize=False)),
                ('NgayDiemDanh', models.DateField()),
                ('KetQuaDiemDanh', models.CharField(choices=[('C', 'Có mặt'), ('P', 'Vắng có phép'), ('V', 'Vắng không phép')], default=1, max_length=1)),
                ('ChiaLop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChiaLop_DiemDanh', to='ThietLapNamHocMoi.chialop')),
                ('ThieuNhi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ThieuNhi_DiemDanh', to='ThietLapNamHocMoi.thieunhi')),
                ('Updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'table_DiemDanh',
            },
        ),
        migrations.AddField(
            model_name='chialop',
            name='ChuyenCanThieuNhi',
            field=models.ManyToManyField(blank=True, related_name='ChuyenCanThieuNhi', through='ThietLapNamHocMoi.DiemDanh', to='ThietLapNamHocMoi.ThieuNhi'),
        ),
        migrations.AddField(
            model_name='thieunhi',
            name='ThongTinChuyenCan',
            field=models.ManyToManyField(blank=True, related_name='ThongTinChuyenCan', through='ThietLapNamHocMoi.DiemDanh', to='ThietLapNamHocMoi.ChiaLop'),
        ),
    ]