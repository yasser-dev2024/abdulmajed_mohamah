import os

# المجلدات الرئيسية
folders = [
    "templates",
    "static",
    "static/css",
    "static/uploads"
]

# الملفات الفارغة المطلوبة
files = {
    "app.py": "",
    "users.json": "{}",
    "inquiries.json": "[]",
    "templates/index.html": "",
    "templates/register.html": "",
    "templates/login.html": "",
    "templates/user_home.html": "",
    "templates/my_inquiries.html": "",
    "templates/admin_dashboard.html": "",
    "static/css/style.css": ""
}

# إنشاء المجلدات
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# إنشاء الملفات
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ تم إنشاء جميع المجلدات والملفات المطلوبة.")
