import requests

from app.bunnycdn_setup import BUNNY_STORAGE_ZONE, BUNNY_API_KEY, BUNNY_STORAGE_HOST

# def upload_to_bunnycdn(filename: str, file_bytes: bytes):
#     url = f"{BUNNY_STORAGE_HOST}/{BUNNY_STORAGE_ZONE}/{filename}"
    
#     headers = {
#         "AccessKey": BUNNY_API_KEY,
#         "Content-Type": "application/octet-stream"
#     }

#     try:
#         response = requests.put(url, headers=headers, data=file_bytes)

#         if response.status_code == 201:
#             return True, "Yuklandi"
#         else:
#             return False, f"Xato: {response.status_code} - {response.text}"

#     except Exception as e:
#         return False, f"Exception: {str(e)}"


def upload_to_bunnycdn(filename: str, file_bytes: bytes):
    import os

    print("📤 [BUNNY UPLOAD] Fayl yuklanmoqda...")

    # Log uchun barcha kerakli ma'lumotlar
    print("📄 Fayl nomi:", filename)
    print("📦 Storage host:", BUNNY_STORAGE_HOST)
    print("📁 Storage zone:", BUNNY_STORAGE_ZONE)
    print("🔑 Access key (birinchi 6ta harf):", BUNNY_API_KEY[:6] + "...")  # butun API keyni chiqarma
    print("🔗 URL:", f"{BUNNY_STORAGE_HOST}/{BUNNY_STORAGE_ZONE}/{filename}")

    url = f"{BUNNY_STORAGE_HOST}/{BUNNY_STORAGE_ZONE}/{filename}"
    headers = {
        "AccessKey": BUNNY_API_KEY,
        "Content-Type": "application/octet-stream"
    }

    try:
        response = requests.put(url, headers=headers, data=file_bytes)

        print("📥 Response status:", response.status_code)
        print("📥 Response text:", response.text)

        if response.status_code == 201:
            print("✅ Yuklash muvaffaqiyatli!")
            return True, "Yuklandi"
        else:
            print("❌ Xatolik yuz berdi:", response.status_code)
            return False, f"Xato: {response.status_code} - {response.text}"

    except Exception as e:
        print("💥 Istisno:", str(e))
        return False, f"Exception: {str(e)}"
