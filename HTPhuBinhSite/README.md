# HTPhuBinh

## About the project
This website helps managing data and stuff relating to catechism class.

## Features
- Base: Tạo user, đăng nhập, đăng ký tài khoản, sửa thông tin cá nhân
- ThietLapNamHoc: BQT thiết lập các thông tin cần thiết cho năm học mới, phân công, phân nhiệm, chia lớp…
- VanHanhNamHoc: anh/chị HT-GLV thêm thiếu nhi, chỉnh sửa điểm số, điểm danh thiếu nhi…

## Tech
- Django
- Bootstrap 4
- jQuery

## Getting started
### Prerequisites 
- Python3
- Pip3
- MySQL

### Installation
1. Going to base directory
```cd HTPhuBinhSite```
2. Creating an virtual environment (Optional)
[virutalenv](https://virtualenv.pypa.io/en/latest/)
3. Install dependencies
``` pip3 install requirements.txt```
4. Starting MySQL server
```mysql -u root -p HTPhuBinh```
References: [MySQL](https://dev.mysql.com/doc/refman/8.0/en/tutorial.html)
5. Applying DB changes
```python3 manage.py migrate```
6. Starting the development server
```python3 manage.py runserver```

### Development
- Update depencies when installing new libraries: ```pip freeze > requirements.txt```

### Note
You might found trouble with library ```django-keyboard-shortcuts```. Follow the instructions here [django-keyboard-shortcuts-error](https://stackoverflow.com/questions/57995209/django-keyboard-shortcuts).