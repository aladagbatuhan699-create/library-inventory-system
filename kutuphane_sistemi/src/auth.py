import hashlib
import os
import LocalAuthentication
import threading

# Dosya yolları için ana dizini bul
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSYA_YOLU = os.path.join(BASE_DIR, "data", "users.txt")

def hash_password(sifre):
    """Şifreleri SHA-256 ile maskeler."""
    return hashlib.sha256(sifre.encode()).hexdigest()

def admin_touch_id_dogrula():
    """Doğrudan MacBook Touch ID sensörünü tetikler."""
    context = LocalAuthentication.LAContext.new()
    policy = 1  # LAPolicyDeviceOwnerAuthenticationWithBiometrics
    sebep = "Kütüphane Yönetici Paneline Güvenli Erişim"
    
    # Cihazda Touch ID var mı kontrol et
    can_evaluate, error = context.canEvaluatePolicy_error_(policy, None)
    
    if not can_evaluate:
        # Sensör yoksa veya kapalıysa klasik şifreye düşmemek için False döner
        return False
        
    sonuc = [False]
    bekleme_olayi = threading.Event()
    
    def dogrulama_sonucu(basari, hata):
        sonuc[0] = basari
        bekleme_olayi.set()
        
    # Sensörü çalıştır
    context.evaluatePolicy_localizedReason_reply_(policy, sebep, dogrulama_sonucu)
    bekleme_olayi.wait()
    
    return sonuc[0]

def login_user():
    """Giriş mekanizması: Admin için parmak izi, diğerleri için şifre."""
    print("\n" + "="*40)
    print(" KÜTÜPHANE SİSTEMİ - GÜVENLİ GİRİŞ")
    print("="*40)
    
    kullanici_adi = input("Kullanıcı Adı: ")
    
    # YÖNETİCİ GİRİŞİ (TOUCH ID)
    if kullanici_adi == "admin":
        print("\n[!] Yönetici yetkisi algılandı. Lütfen parmağınızı sensöre okutun...")
        if admin_touch_id_dogrula():
            print(f"\n[+] Parmak izi onaylandı. Hoş geldin, {kullanici_adi}!")
            return {"username": kullanici_adi, "role": "yonetici"}
        else:
            print("\n[-] Yetkisiz Erişim: Touch ID doğrulaması başarısız!")
            return None

    # PERSONEL VE ÖĞRENCİ GİRİŞİ (KLASİK ŞİFRE)
    sifre = input("Şifre: ")
    hashed_sifre = hash_password(sifre)
    
    if not os.path.exists(DOSYA_YOLU):
        print("[-] Hata: Kullanıcı veritabanı bulunamadı!")
        return None

    with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            bilgiler = satir.strip().split(',')
            if len(bilgiler) == 3:
                db_kullanici, db_sifre, db_rol = bilgiler
                if kullanici_adi == db_kullanici and hashed_sifre == db_sifre:
                    print(f"\n[+] Giriş başarılı! Yetki: {db_rol}")
                    return {"username": kullanici_adi, "role": db_rol}
                    
    print("\n[-] Hata: Kullanıcı adı veya şifre yanlış!")
    return None

# Kullanıcı ekleme ve silme fonksiyonları aynen korunuyor...
def kullanici_ekle():
    print("\n--- YENİ KULLANICI EKLE ---")
    kullanici_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")
    rol = input("Rol (yonetici/personel/ogrenci): ").lower()
    hashed_sifre = hash_password(sifre)
    with open(DOSYA_YOLU, "a", encoding="utf-8") as dosya:
        dosya.write(f"{kullanici_adi},{hashed_sifre},{rol}\n")
    print(f"[+] '{kullanici_adi}' başarıyla eklendi.")

def kullanici_sil():
    print("\n--- KULLANICI SİL ---")
    silinecek = input("Silinecek Kullanıcı: ")
    if silinecek == "admin": return
    with open(DOSYA_YOLU, "r", encoding="utf-8") as f: satirlar = f.readlines()
    with open(DOSYA_YOLU, "w", encoding="utf-8") as f:
        for s in satirlar:
            if not s.startswith(silinecek + ","): f.write(s)
    print(f"[+] '{silinecek}' sistemden temizlendi.")

def gui_login(kullanici_adi, sifre):
    """Arayüzden (UI) gelen verilerle arka plan doğrulamasını yapar."""
    
    # ==========================================
    # 👑 YÖNETİCİ KADROSU (EKİP ARKADAŞLARIN)
    # ==========================================
    # Kendi grubunuzdaki isimleri buraya küçük harflerle ekle
    yoneticiler = ["admin", "elif", "deniz", "damla"]
    
    # Kullanıcı yanlışlıkla büyük harf veya boşluk girerse diye temizliyoruz
    girilen_ad = kullanici_adi.lower().strip()

    # YÖNETİCİ KONTROLÜ (TOUCH ID)
    if girilen_ad in yoneticiler:
        if admin_touch_id_dogrula():
            # İsimle karşılama mesajı eklendi
            return True, "yonetici", f"Hoş geldin {kullanici_adi.capitalize()}!"
        else:
            return False, None, "Touch ID reddedildi veya iptal edildi!"

    # ==========================================
    # 👥 DİĞER KULLANICILAR İÇİN ŞİFRE KONTROLÜ
    # ==========================================
    hashed_sifre = hash_password(sifre)
    
    if not os.path.exists(DOSYA_YOLU):
        return False, None, "Sistem veritabanı bulunamadı!"

    with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
        for satir in dosya:
            bilgiler = satir.strip().split(',')
            if len(bilgiler) == 3:
                db_kullanici, db_sifre, db_rol = bilgiler
                if kullanici_adi == db_kullanici and hashed_sifre == db_sifre:
                    return True, db_rol, "Şifre doğrulandı!"
                    
    return False, None, "Kullanıcı adı veya şifre yanlış!"