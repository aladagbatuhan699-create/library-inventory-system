import datetime
import os
from src.utils import proje_kok_dizini_bul

class RaporMotoru:
    def __init__(self, islem_veritabani):
        self.islem_db = islem_veritabani

    def gecikenleri_listele(self):
        """Teslim tarihi geçmiş kitapları tespit eder."""
        gecikenler = []
        simdi = datetime.datetime.now()
        
        for islem in self.islem_db.yapilan_islemler:
            if simdi > islem["iade_tarihi"]:
                gecikme_gun = (simdi - islem["iade_tarihi"]).days
                ceza = gecikme_gun * self.islem_db.GUNLUK_CEZA
                gecikenler.append({
                    "isbn": islem["isbn"],
                    "kitap_ad": islem["kitap_ad"],
                    "gecikme": gecikme_gun,
                    "ceza": ceza
                })
        return gecikenler

    def gecikenler_raporu_olustur(self):
        """Geciken kitapları bir TXT dosyası olarak dışa aktarır."""
        geciken_listesi = self.gecikenleri_listele()
        
        # Raporu 'docs' klasörüne kaydedelim
        docs_klasoru = os.path.join(proje_kok_dizini_bul(), "docs")
        if not os.path.exists(docs_klasoru):
            os.makedirs(docs_klasoru)
            
        dosya_adi = os.path.join(docs_klasoru, f"Geciken_Kitaplar_Raporu_{datetime.datetime.now().strftime('%Y%m%d')}.txt")
        
        with open(dosya_adi, "w", encoding="utf-8") as dosya:
            dosya.write("="*50 + "\n")
            dosya.write(" 🚨 GECİKEN KİTAPLAR VE CEZA RAPORU 🚨\n")
            dosya.write("="*50 + "\n")
            dosya.write(f"Tarih: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            if not geciken_listesi:
                dosya.write("Harika! Şu an gecikmiş hiçbir kitap bulunmuyor.\n")
            else:
                for item in geciken_listesi:
                    dosya.write(f"Kitap: {item['kitap_ad'][:20]:<20} | ISBN: {item['isbn']:<10} | Gecikme: {item['gecikme']} Gün | Ceza: {item['ceza']:.2f} TL\n")
            
            dosya.write("-" * 50 + "\n")
            toplam_ceza = sum(item['ceza'] for item in geciken_listesi)
            dosya.write(f"TOPLAM BEKLENEN TAHSİLAT: {toplam_ceza:.2f} TL\n")
            dosya.write("="*50 + "\n")
            
        return dosya_adi