from django.shortcuts import render, redirect
from modules.views import manage_modul 
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db_connection import classes_collection, modules_collection
from django.http import JsonResponse


def manage_classes(request):
    # 1. Ambil raw data dari database
    raw_classes = list(classes_collection.find())
    daftar_kelas = []

    for cls in raw_classes:
        # 2. Ambil referensi modul (berupa list of string ID)
        modul_ids_str = cls.get('daftar_modul', [])
        
        # Konversi string ke ObjectId yang valid agar bisa di-query
        modul_object_ids = []
        for mid in modul_ids_str:
            try:
                modul_object_ids.append(ObjectId(mid))
            except Exception:
                pass # Abaikan jika format string bukan ObjectId yang valid
        
        # 3. Lakukan "Join" manual dengan in-query ke collection modules
        modules_data = list(modules_collection.find({"_id": {"$in": modul_object_ids}}))
        
        # 4. Format data modul sesuai ekspektasi template
        modul_list = []
        for mod in modules_data:
            sub_modul_arr = mod.get('sub_modul', [])
            total_chapters = sum(len(sm.get('bab', [])) for sm in sub_modul_arr)
            
            # TAMBAHKAN INI UNTUK DEBUGGING
            print(f"Modul: {mod.get('judul_modul')}, Chapters: {total_chapters}") 
            
            modul_list.append({
                'id': str(mod['_id']),
                'judul': mod.get('judul_modul', 'Untitled Module'),
                'submodul': len(sub_modul_arr),
                'chapters': total_chapters, # Pastikan ini konsisten
            })

        # 5. Rangkai data kelas
        kelas_dict = {
            'id': str(cls['_id']),
            'nama_kelas': cls.get('nama_kelas', 'Unnamed Class'),
            # Jika 'id_teacher' mereferensi ke collection users, idealnya Anda lookup lagi.
            # Di sini kita lempar langsung value-nya sebagai mentor.
            'mentor': cls.get('id_teacher', 'Unknown'), 
            'jumlah_siswa': len(cls.get('daftar_siswa', [])),
            'total_modul': len(modul_ids_str),
            'status': cls.get('status', 'Active'),        # Default (tidak terlihat di skema)
            'modul_list': modul_list
        }
        
        daftar_kelas.append(kelas_dict)

    # Kirim variabel dengan nama 'daftar_kelas' agar dikenali template
    return render(request, 'manage_class.html', {'daftar_kelas': daftar_kelas})


# 🔹 TAMBAH CLASS
def add_class(request):
    if request.method == "POST":
        data = {
            "class_name": request.POST.get('class_name'),
            "mentor": request.POST.get('mentor'),
            "status": request.POST.get('status'),
            "total_students": int(request.POST.get('total_students') or 0),
            "modules": []
        }

        classes_collection.insert_one(data)

    return redirect('manage_class')


# 🔹 EDIT CLASS
def edit_class(request, class_id):
    if request.method == "POST":
        classes_collection.update_one(
            {"_id": ObjectId(class_id)},
            {"$set": {
                "class_name": request.POST.get('class_name'),
                "mentor": request.POST.get('mentor'),
                "status": request.POST.get('status')
            }}
        )

    return redirect('manage_class')


# 🔹 DELETE CLASS
def delete_class(request, class_id):
    classes_collection.delete_one({"_id": ObjectId(class_id)})
    return redirect('manage_class')


# 🔹 TAMBAH MODULE
def add_module(request, class_id):
    if request.method == "POST":
        module_name = request.POST.get("module_name")

        classes_collection.update_one(
            {"_id": ObjectId(class_id)},
            {"$push": {"modules": {"module_name": module_name}}}
        )

    return redirect('manage_class')

from bson.errors import InvalidId

def get_class_details(request, class_id):
    try:
        obj_id = ObjectId(class_id)
        kelas = classes_collection.find_one({"_id": obj_id})

        if not kelas:
            return JsonResponse({"error": "Kelas tidak ditemukan"}, status=404)

        # FIX DI SINI
        mentor = kelas.get('id_teacher')
        if isinstance(mentor, ObjectId):
            mentor = str(mentor)

        siswa = kelas.get('daftar_siswa', [])
        siswa = [str(s) if isinstance(s, ObjectId) else s for s in siswa]

        data = {
            "judul_kelas": kelas.get('nama_kelas', 'Unnamed Class'),
            "nama_mentor": mentor,
            "siswa": siswa
        }

        return JsonResponse(data)

    except Exception as e:
        print("ERROR ASLI:", e)
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
    