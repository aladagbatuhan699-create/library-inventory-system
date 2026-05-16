import datetime

class IslemYonetimi:
    def __init__(self, envanter_yoneticisi):
        # Envanter motorunu buraya bağlayarak ortak veritabanı kullanmalarını sağlıyoruz
        self.kutuphane_db = envanter_yoneticisi
        self.yapilan_islemler = []
        self.GECIKME_SINIRI = 15  # Gün
        self.GUNLUK_CEZA = 1.5    # TL

    def odunc_ver(self, isbn, kac_gun_once):
        """Kitabı ödünç verir, stoğunu düşürür ve işlemi listeye kaydeder."""
        for kitap in self.kutuphane_db.envanter:
            if kitap.isbn == isbn:
                if kitap.stok > 0:
                    kitap.stok -= 1
                    self.kutuphane_db.veriyi_kaydet() # kitaplar.txt anlık güncellenir
                    
                    # Arkadaşının tarih simülasyon motoru
                    verilis = datetime.datetime.now() - datetime.timedelta(days=kac_gun_once)
                    iade_hedef = verilis + datetime.timedelta(days=self.GECIKME_SINIRI)
                    
                    self.yapilan_islemler.append({
                        "isbn": kitap.isbn,
                        "kitap_ad": kitap.ad,
                        "verilis_tarihi": verilis,
                        "iade_tarihi": iade_hedef
                    })
                    print(f"[İŞLEM] '{kitap.ad}' ödünç verildi. Son İade: {iade_hedef.strftime('%d-%m-%Y')}")
                    return True
                else:
                    print(f"[UYARI] {kitap.ad} şu an stokta yok.")
                    return False
        print(f"[HATA] ISBN: {isbn} olan kitap bulunamadı.")
        return False

    def analiz_raporu(self):
        """Konsola rapor yazdırmak için (Arkadaşının yazdığı orijinal analiz şovu)"""
        print("\n" + "="*60)
        print(f"{'KÜTÜPHANE YÖNETİM VE ANALİZ RAPORU':^60}")
        print("="*60)
        print(f"{'Kitap Adı':<30} | {'Durum':<12} | {'Ceza':<10}")
        print("-" * 60)
        
        toplam_ceza = 0
        simdi = datetime.datetime.now()
        
        for islem in self.yapilan_islemler:
            kitap_adi = islem["kitap_ad"]
            iade_vakti = islem["iade_tarihi"]
            
            if simdi > iade_vakti:
                gecikme_gun = (simdi - iade_vakti).days
                ceza = gecikme_gun * self.GUNLUK_CEZA
                toplam_ceza += ceza
                durum = f"{gecikme_gun} Gün Gecikti"
                print(f"{kitap_adi[:30]:<30} | {durum:<12} | {ceza:>6.2f} TL")
            else:
                kalan_gun = (iade_vakti - simdi).days
                durum = f"{kalan_gun} Gün Kaldı"
                print(f"{kitap_adi[:30]:<30} | {durum:<12} | {'0.00':>6} TL")
                
        print("-" * 60)
        print(f"{'TOPLAM CEZA:':<45} {toplam_ceza:>8.2f} TL")
        print("="*60)
        return toplam_ceza