import os

# مسار مجلد المشروع
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# قائمة الملفات المطلوبة داخل static
required_files = {
    "css": ["style.css", "responsive.css"],
    "js": ["main.js"],
    "images": ["logo.png", "coffee1.jpg", "coffee2.jpg"]
}

missing_files = []

for folder, files in required_files.items():
    folder_path = os.path.join(PROJECT_ROOT, "static", folder)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            missing_files.append(f"static/{folder}/{file}")

if missing_files:
    print("❌ الملفات التالية مفقودة:")
    for f in missing_files:
        print(f" - {f}")
else:
    print("✅ كل الملفات موجودة في مكانها الصحيح.")
