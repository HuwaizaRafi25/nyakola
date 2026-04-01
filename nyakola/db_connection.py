# db_connection.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

# Load environment variables
load_dotenv()

# Ambil MONGO_URI dari .env
MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI tidak ditemukan di file .env!")

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,   # Timeout 5 detik
        tls=True                         # Pastikan SSL/TLS aktif
    )
    
    # Test koneksi
    client.server_info()
    
    db = client['db_nyakola']
    users_collection = db['users']
    
    print("✅ Berhasil terhubung ke MongoDB Atlas")

except ConnectionFailure:
    print("❌ Gagal terhubung ke MongoDB Atlas - Periksa internet atau URI")
    users_collection = None
except ConfigurationError as e:
    print(f"❌ Konfigurasi MongoDB salah: {e}")
    users_collection = None
except Exception as e:
    print(f"❌ Error tidak terduga: {e}")
    users_collection = None