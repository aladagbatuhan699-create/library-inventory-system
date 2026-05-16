import datetime

# --- 1. AYARLAR VE GLOBAL DEĞİŞKENLER ---
kitaplar_listesi = []
yapilan_islemler = []
GECIKME_SINIRI = 15  # Gün
GUNLUK_CEZA = 1.5    # TL

# --- 2. ÇEKİRDEK FONKSİYONLAR ---

def kitaplari_yukle():
    """Dosyadan kitapları okur ve bir sözlük yapısında listeye ekler."""
    try:
        with open("kitaplar.txt", "r", encoding="utf-8") as dosya:
            for index, satir in enumerate(dosya, start=1):
                kitap_adi = satir.strip()
                if kitap_adi:
                    # Her kitabı ID, Ad ve Stok bilgisiyle tutuyoruz
                    kitaplar_listesi.append({
                        "id": index, 
                        "ad": kitap_adi, 
                        "stok": 3
                    })
        print(f">>> Sistem aktif: {len(kitaplar_listesi)} kitap veri tabanına yüklendi.")
    except FileNotFoundError:
        print("Hata: 'kitaplar.txt' dosyası bulunamadı! Lütfen dosyayı oluşturun.")

def odunc_ver(kitap_id, kac_gun_once):
    """Kitabı verir ve iade tarihini otomatik hesaplayıp kaydeder."""
    for kitap in kitaplar_listesi:
        if kitap["id"] == kitap_id:
            if kitap["stok"] > 0:
                kitap["stok"] -= 1
                
                # Tarih hesaplamaları
                verilis = datetime.datetime.now() - datetime.timedelta(days=kac_gun_once)
                iade_hedef = verilis + datetime.timedelta(days=GECIKME_SINIRI)
                
                yapilan_islemler.append({
                    "kitap_ad": kitap["ad"],
                    "verilis_tarihi": verilis,
                    "iade_tarihi": iade_hedef
                })
                print(f"[İŞLEM] {kitap['ad']} verildi. Son iade: {iade_hedef.strftime('%d-%m-%Y')}")
                return
            else:
                print(f"[UYARI] {kitap['ad']} şu an stokta yok.")
                return
    print(f"[HATA] ID:{kitap_id} bulunamadı.")

def analiz_raporu():
    """Tüm işlemleri kontrol edip, gecikmeleri ve cezaları satır satır yazdırır."""
    print("\n---KÜTÜPHANE YÖNETİM VE ANALİZ RAPORU---\n")
    
    toplam_ceza = 0
    simdi = datetime.datetime.now()
    
    for islem in yapilan_islemler:
        kitap_adi = islem["kitap_ad"]
        iade_vakti = islem["iade_tarihi"]
        
        if simdi > iade_vakti:
            gecikme_gun = (simdi - iade_vakti).days
            ceza = gecikme_gun * GUNLUK_CEZA
            toplam_ceza += ceza
            durum = f"{gecikme_gun} Gün Gecikti"
        else:
            kalan_gun = (iade_vakti - simdi).days
            durum = f"{kalan_gun} Gün Kaldı"
            ceza = 0.0

        # Satır satır yazdırma bölümü
        print(f"Kitap Adı : {kitap_adi}")
        print(f"Durum     : {durum}")
        print(f"Ceza      : {ceza:.2f} TL")
        print("-" * 40)
            
    print(f"TOPLAM CEZA: {toplam_ceza:.2f} TL\n")

# --- 3. ANA DÖNGÜ ---

# Adım 1: Verileri yükle
kitaplari_yukle()

# Adım 2: Örnek Senaryoları Çalıştır
if kitaplar_listesi:
    # 1. Kitabı 20 gün önce ver (5 gün gecikmiş olmalı)
    odunc_ver(1, 20)
    
    # 2. Kitabı 5 gün önce ver (Süresi var)
    odunc_ver(2, 5)
    
    # 5. Kitabı 40 gün önce ver (Ciddi gecikmiş)
    odunc_ver(5, 40)

# Adım 3: Sonucu raporla
analiz_raporu()