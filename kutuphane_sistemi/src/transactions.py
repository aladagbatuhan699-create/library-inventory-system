

import datetime
import os

class IslemYonetimi:
    def __init__(self, envanter_yoneticisi):
        self.kutuphane_db = envanter_yoneticisi
        self.yapilan_islemler = []
        self.GECIKME_SINIRI = 15  # Gün
        self.GUNLUK_CEZA = 1.5    # TL
        
        # İşlemleri kaydedeceğimiz dosyanın yolunu belirliyoruz
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dosya_yolu = os.path.join(BASE_DIR, "data", "islemler.txt")
        self.islemleri_yukle()

    def islemleri_yukle(self):
        """islemler.txt dosyasından aktif ödünçleri okur."""
        self.yapilan_islemler = []
        if not os.path.exists(self.dosya_yolu):
            return
            
        with open(self.dosya_yolu, "r", encoding="utf-8") as dosya:
            for satir in dosya:
                temiz_satir = satir.strip()
                if not temiz_satir:
                    continue
                parcalar = temiz_satir.split(",")
                if len(parcalar) == 4:
                    isbn, kitap_ad, verilis_str, iade_str = parcalar
                    self.yapilan_islemler.append({
                        "isbn": isbn,
                        "kitap_ad": kitap_ad,
                        "verilis_tarihi": datetime.datetime.strptime(verilis_str, "%Y-%m-%d"),
                        "iade_tarihi": datetime.datetime.strptime(iade_str, "%Y-%m-%d")
                    })

    def islemleri_kaydet(self):
        """Aktif ödünçleri islemler.txt dosyasına yazar."""
        # data klasörü yoksa oluştur
        os.makedirs(os.path.dirname(self.dosya_yolu), exist_ok=True)
        with open(self.dosya_yolu, "w", encoding="utf-8") as dosya:
            for islem in self.yapilan_islemler:
                verilis_str = islem["verilis_tarihi"].strftime("%Y-%m-%d")
                iade_str = islem["iade_tarihi"].strftime("%Y-%m-%d")
                dosya.write(f"{islem['isbn']},{islem['kitap_ad']},{verilis_str},{iade_str}\n")

    def odunc_ver(self, isbn, gecmis_gun=0):
        """Kitabı ödünç verir, stoğunu düşürür ve dosyaya kaydeder. 
        gecmis_gun parametresi ile test amaçlı geçmiş tarihe işlem yapılabilir."""
        import datetime # Garanti olsun diye ekledik
        
        for kitap in self.kutuphane_db.envanter:
            if kitap.isbn == isbn:
                if kitap.stok > 0:
                    kitap.stok -= 1
                    
                    # 🔥 İŞTE ZAMAN YOLCULUĞU BURADA: Bugünden gecmis_gun kadar geriye gidiyoruz
                    verilis = datetime.datetime.now() - datetime.timedelta(days=gecmis_gun)
                    iade_hedef = verilis + datetime.timedelta(days=self.GECIKME_SINIRI)
                    
                    self.yapilan_islemler.append({
                        "isbn": kitap.isbn,
                        "kitap_ad": kitap.ad,
                        "verilis_tarihi": verilis,
                        "iade_tarihi": iade_hedef
                    })
                    self.islemleri_kaydet()
                    return True, f"'{kitap.ad}' başarıyla ödünç verildi."
                else:
                    return False, f"'{kitap.ad}' stokta kalmamış!"
        return False, "Bu ISBN numarasına ait kitap bulunamadı."

    def iade_al(self, isbn):
        """Kitabı iade alır, cezayı hesaplar, stoğu artırır ve dosyadan siler."""
        for islem in self.yapilan_islemler:
            if islem["isbn"] == isbn:
                simdi = datetime.datetime.now()
                ceza = 0
                if simdi > islem["iade_tarihi"]:
                    gecikme = (simdi - islem["iade_tarihi"]).days
                    ceza = gecikme * self.GUNLUK_CEZA
                
                # İşlemi listeden çıkar ve kaydet
                self.yapilan_islemler.remove(islem)
                self.islemleri_kaydet()
                
                # Stoğu geri ekle
                for kitap in self.kutuphane_db.envanter:
                    if kitap.isbn == isbn:
                        kitap.stok += 1
                        # self.kutuphane_db.veriyi_kaydet() # Stok güncellemesini kaydet
                        break
                        
                mesaj = f"İade başarılı! Kesilen Ceza: {ceza} TL" if ceza > 0 else "İade başarılı, ceza yok. Teşekkürler!"
                return True, mesaj
        return False, "Bu ISBN numarasıyla aktif bir ödünç işlemi bulunamadı."