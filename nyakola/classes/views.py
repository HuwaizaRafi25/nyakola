from django.shortcuts import render, redirect
from modules.views import manage_modules 
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db_connection import classes_collection, modules_collection, users_collection
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
            "nama_kelas": request.POST.get('class_name'),
            "id_teacher": request.POST.get('mentor'),
            "status": request.POST.get('status'),
            "daftar_siswa": int(request.POST.get('total_students') or 0),
            "daftar_modul": []
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
    if request.method == "POST":
        try:
            # Hapus dari MongoDB
            result = classes_collection.delete_one({"_id": ObjectId(class_id)})
            
            if result.deleted_count > 0:
                return JsonResponse({'success': True, 'message': 'Kelas berhasil dihapus'})
            else:
                return JsonResponse({'success': False, 'message': 'Kelas tidak ditemukan'}, status=404)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=400)


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
    print(f"DEBUG: Menerima ID: {class_id}") # Cek di terminal Django
    try:
        # Konversi class_id ke ObjectId untuk pencarian
        obj_id = ObjectId(class_id)
        
        # Mengambil data kelas
        kelas = classes_collection.find_one({"_id": obj_id})
        
        # Pengecekan jika kelas tidak ada (dari kode lama)
        if not kelas:
            return JsonResponse({"error": "Kelas tidak ditemukan"}, status=404)

        # Penanganan tipe data ObjectId agar tidak error saat dikirim ke JSON
        mentor = kelas.get('id_teacher', 'Unknown')
        if isinstance(mentor, ObjectId):
            mentor = str(mentor)

        # Tambahkan Logika Detail Siswa
        siswa_ids = kelas.get('daftar_siswa', [])
        siswa_details = []

        for s_id in siswa_ids:
            # Cari ke users_collection berdasarkan ID
            # Pastikan s_id dikonversi ke ObjectId jika di database users menggunakan ObjectId
            try:
                user_obj_id = ObjectId(s_id) if isinstance(s_id, str) else s_id
                user_data = users_collection.find_one({"_id": user_obj_id})
                
                if user_data:
                    siswa_details.append({
                        "id": str(s_id),
                        "nama": user_data.get('nama_lengkap', user_data.get('username', 'Tanpa Nama'))
                    })
                else:
                    siswa_details.append({"id": str(s_id), "nama": f"ID: {s_id}"})
            except:
                siswa_details.append({"id": str(s_id), "nama": f"ID: {s_id}"})

        modul_query = list(modules_collection.find({
            "$or": [
                {"id_class": str(obj_id)},
                {"id_class": obj_id}
            ]
        }))
        
        data = {
            "judul_kelas": kelas.get('nama_kelas', 'Unnamed Class'),
            "nama_mentor": mentor,
            "siswa": siswa_details, # Kirim objek detail, bukan cuma list ID
            "modul": [
                {"judul": m.get('judul_modul', 'Untitled Module')} for m in modul_query
            ]
        }
        
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)