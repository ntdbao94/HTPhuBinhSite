# Generated by Django 3.2.7 on 2021-10-29 04:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ThietLapNamHocMoi', '0005_alter_diemdanh_ketquadiemdanh'),
    ]

    operations = [
        migrations.CreateModel(
            name='CotDiem',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_CotDiem', models.AutoField(primary_key=True, serialize=False)),
                ('HocKy', models.IntegerField(choices=[(1, 'Học kỳ I'), (2, 'Học kỳ II')], default=1)),
                ('LoaiCotDiem', models.IntegerField(choices=[(0, 'Hệ số 01'), (1, 'KT 15'), (2, 'KT 1 Tiết'), (3, 'Thi Học kỳ')])),
                ('DiemSo', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('BangDiem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BangDiem_CotDiem', to='ThietLapNamHocMoi.bangdiem')),
                ('Updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'table_CotDiem',
            },
        ),
    ]
