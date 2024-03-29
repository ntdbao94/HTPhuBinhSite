# Generated by Django 3.2.7 on 2021-09-29 08:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChiaLop',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_ChiaLop', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'table_ChiaLop',
            },
        ),
        migrations.CreateModel(
            name='DanhMucLop',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_DanhMucLop', models.AutoField(primary_key=True, serialize=False)),
                ('MaLop', models.CharField(default='', max_length=45)),
                ('TenLop', models.CharField(default='', max_length=45)),
                ('DoTuoi', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'table_DanhMucLop',
                'ordering': ['DoTuoi', 'MaLop'],
            },
        ),
        migrations.CreateModel(
            name='PhanCong',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_PhanCong', models.AutoField(primary_key=True, serialize=False)),
                ('ChiaLop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChiaLop', to='ThietLapNamHocMoi.chialop')),
            ],
            options={
                'db_table': 'table_PhanCong',
            },
        ),
        migrations.CreateModel(
            name='HuynhTruong',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_HuynhTruong', models.AutoField(primary_key=True, serialize=False)),
                ('TenThanh', models.CharField(blank=True, default='', max_length=45)),
                ('NgaySinh', models.DateField(blank=True, null=True)),
                ('NgayBonMang', models.DateField(blank=True, null=True)),
                ('DiaChi', models.CharField(blank=True, default='', max_length=100)),
                ('Sdt1', models.CharField(blank=True, default='', max_length=15)),
                ('Sdt2', models.CharField(blank=True, default='', max_length=15)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, default=None, upload_to='%Y/%m')),
                ('PhanCong_HuynhTruong', models.ManyToManyField(related_name='PhanCong_HuynhTruong', through='ThietLapNamHocMoi.PhanCong', to='ThietLapNamHocMoi.ChiaLop')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'table_HuynhTruong',
                'ordering': ['NgaySinh', 'id_HuynhTruong'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='phancong',
            name='HuynhTruong',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HuynhTruong', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='phancong',
            name='Updated_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DanhMucNienKhoa',
            fields=[
                ('Is_Active', models.IntegerField(choices=[(1, 'Đang sử dụng'), (0, 'Không còn sử dụng')], default=1)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
                ('id_DanhMucNienKhoa', models.AutoField(primary_key=True, serialize=False)),
                ('NamBatDau', models.IntegerField()),
                ('NamKetThuc', models.IntegerField()),
                ('ChuDeNamHoc', models.CharField(default='', max_length=255)),
                ('BaiHatChuDe', models.CharField(blank=True, default='', max_length=45)),
                ('KhauHieuNamHoc', models.CharField(blank=True, default='', max_length=255)),
                ('ChiaLop_NienKhoa', models.ManyToManyField(related_name='ChiaLop_NienKhoa', through='ThietLapNamHocMoi.ChiaLop', to='ThietLapNamHocMoi.DanhMucLop')),
                ('Updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'table_DanhMucNienKhoa',
                'ordering': ['-NamBatDau', '-NamKetThuc'],
            },
        ),
        migrations.AddField(
            model_name='danhmuclop',
            name='ChiaLop_Lop',
            field=models.ManyToManyField(related_name='ChiaLop_Lop', through='ThietLapNamHocMoi.ChiaLop', to='ThietLapNamHocMoi.DanhMucNienKhoa'),
        ),
        migrations.AddField(
            model_name='danhmuclop',
            name='Updated_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chialop',
            name='ChiDoanTruong',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ChiDoanTruong', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chialop',
            name='DanhMucLop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DanhMucLop', to='ThietLapNamHocMoi.danhmuclop'),
        ),
        migrations.AddField(
            model_name='chialop',
            name='DanhMucNienKhoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DanhMucNienKhoa', to='ThietLapNamHocMoi.danhmucnienkhoa'),
        ),
        migrations.AddField(
            model_name='chialop',
            name='PhanCong_ChiaLop',
            field=models.ManyToManyField(related_name='PhanCong_ChiaLop', through='ThietLapNamHocMoi.PhanCong', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chialop',
            name='Updated_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='phancong',
            unique_together={('ChiaLop', 'HuynhTruong')},
        ),
        migrations.AlterUniqueTogether(
            name='danhmuclop',
            unique_together={('MaLop', 'Is_Active')},
        ),
        migrations.AlterUniqueTogether(
            name='chialop',
            unique_together={('DanhMucNienKhoa', 'DanhMucLop')},
        ),
    ]
