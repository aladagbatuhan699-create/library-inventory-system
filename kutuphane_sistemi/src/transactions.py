import datetime
import os
from src.utils import veri_dosyasi_yolu

class IslemYonetimi:
    GECIKME_SINIRI = 15
    GUNLUK_CEZA = 5

    def __init__(self, kutuphane_db):
        self.kutuphane_db = kutuphane_db
        self.yapilan_islemler = []
        self.dosya_yolu = veri_dosyasi_yolu("islemler.txt")
        self.islemleri_yukle()

    def islemleri_yukle(self):
        if not os.path.exists(self.dosya_yolu):
            return
        with open(self.dosya_yolu, "r", encoding="utf-8") as f:
            for satir in f:
                temiz_satir = satir.strip()
                if temiz_satir:
                    parcalar = temiz_satir.split(",")
                    # Defansif kontrol: Artık satırda 5 parça bekliyoruz (Öğrenci adı dahil)
                    if len(parcalar) == 5:
                        isbn, kitap_ad, verilis_str, iade_str, ogrenci_adi = parcalar
                        try:
                            self.yapilan_islemler.append({
                                "isbn": isbn,
                                "kitap_ad": kitap_ad,
                                "verilis_tarihi": datetime.datetime.strptime(verilis_str, "%Y-%m-%d"),
                                "iade_tarihi": datetime.datetime.strptime(iade_str, "%Y-%m-%d"),
                                "ogrenci_adi": ogrenci_adi
                            })
                        except:
                            pass

    def islemleri_kaydet(self):
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            for islem in self.yapilan_islemler:
                v_str = islem["verilis_tarihi"].strftime("%Y-%m-%d")
                i_str = islem["iade_tarihi"].strftime("%Y-%m-%d")
                f.write(f"{islem['isbn']},{islem['kitap_ad']},{v_str},{i_str},{islem['ogrenci_adi']}\n")

    def odunc_ver(self, isbn, ogrenci_adi="bilinmiyor", gecmis_gun=0):
        """Kitabı ismi verilen öğrenciye ödünç kaydeder."""
        for kitap in self.kutuphane_db.envanter:
            if kitap.isbn == isbn:
                if kitap.stok > 0:
                    kitap.stok -= 1
                    verilis = datetime.datetime.now() - datetime.timedelta(days=gecmis_gun)
                    iade_hedef = verilis + datetime.timedelta(days=self.GECIKME_SINIRI)
                    
                    self.yapilan_islemler.append({
                        "isbn": kitap.isbn,
                        "kitap_ad": kitap.ad,
                        "verilis_tarihi": verilis,
                        "iade_tarihi": iade_hedef,
                        "ogrenci_adi": ogrenci_adi
                    })
                    self.islemleri_kaydet()
                    self.kutuphane_db.veriyi_kaydet() # Envanter stok güncellemesi diskte kalıcı olsun
                    return True, f"'{kitap.ad}' başarıyla {ogrenci_adi} kullanıcısına ödünç verildi."
                else:
                    return False, f"'{kitap.ad}' stokta kalmamış!"
        return False, "Bu ISBN numarasına ait kitap bulunamadı."

    def iade_al(self, isbn):
        for islem in self.yapilan_islemler:
            if islem["isbn"] == isbn:
                for kitap in self.kutuphane_db.envanter:
                    if kitap.isbn == isbn:
                        kitap.stok += 1
                        break
                self.yapilan_islemler.remove(islem)
                self.islemleri_kaydet()
                self.kutuphane_db.veriyi_kaydet()
                return True, "Kitap başarıyla iade alındı."
        return False, "Bu ISBN'e ait aktif ödünç işlemi bulunamadı."