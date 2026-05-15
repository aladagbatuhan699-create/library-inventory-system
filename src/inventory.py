import os

class Kitap:
    def __init__(self, ad, yazar, isbn, stok, konum):
        self.ad = ad
        self.yazar = yazar
        self.isbn = isbn
        self.stok = int(stok)
        self.konum = konum

    def __str__(self):
        return f"📖 {self.ad} - {self.yazar} | ISBN: {self.isbn} | Stok: {self.stok} | Konum: {self.konum}"

    # Dosyaya yazmak için veriyi formata sokar (Satır tabanlı depolama)
    def formatla(self):
        return f"{self.ad},{self.yazar},{self.isbn},{self.stok},{self.konum}\n"


class EnvanterYonetimi:
    def __init__(self, dosya_adi="kitaplar.txt"):
        self.dosya_adi = dosya_adi
        self.envanter = []
        self.veriyi_yukle()

    # Görev Tanımı: Metin dosyası aracılığıyla kalıcı depolama (Okuma)
    def veriyi_yukle(self):
        if not os.path.exists(self.dosya_adi):
            return
        with open(self.dosya_adi, "r", encoding="utf-8") as f:
            for satir in f:
                if satir.strip():
                    ad, yazar, isbn, stok, konum = satir.strip().split(",")
                    self.envanter.append(Kitap(ad, yazar, isbn, stok, konum))

    # Görev Tanımı: Metin dosyasına kalıcı kaydetme (Yazma)
    def veriyi_kaydet(self):
        with open(self.dosya_adi, "w", encoding="utf-8") as f:
            for kitap in self.envanter:
                f.write(kitap.formatla())

    # İP 2: Kitap Ekleme
    def kitap_ekle(self, kitap):
        # Eğer aynı ISBN varsa eklemek yerine stoku artırabiliriz (Hassas kontrol)
        for k in self.envanter:
            if k.isbn == kitap.isbn:
                k.stok += kitap.stok
                self.veriyi_kaydet()
                print("⚠️ Bu kitap zaten var, stoku artırıldı!")
                return
        self.envanter.append(kitap)
        self.veriyi_kaydet()
        print(f"✅ '{kitap.ad}' başarıyla eklendi.")

    # İP 2: Kitap Güncelleme
    def kitap_guncelle(self, isbn, yeni_stok=None, yeni_konum=None):
        for kitap in self.envanter:
            if kitap.isbn == isbn:
                if yeni_stok is not None: kitap.stok = yeni_stok
                if yeni_konum: kitap.konum = yeni_konum
                self.veriyi_kaydet()
                print(f"🔄 ISBN: {isbn} güncellendi.")
                return True
        print("❌ Kitap bulunamadı.")
        return False

    # İP 2: Kitap Silme
    def kitap_sil(self, isbn):
        for kitap in self.envanter:
            if kitap.isbn == isbn:
                self.envanter.remove(kitap)
                self.veriyi_kaydet()
                print(f"🗑️ ISBN: {isbn} olan kitap silindi.")
                return True
        print("❌ Silinecek kitap bulunamadı.")
        return False

    # İP 5: Çok Kriterli Kitap Arama ve Listeleme
    def kitap_ara(self, anahtar_kelime=None, kriter="ad"):
        # kriter: "ad", "yazar", "isbn" veya "konum" olabilir
        sonuclar = []
        if not anahtar_kelime:
            return self.envanter

        for kitap in self.envanter:
            #getattr() dinamik olarak kitap.ad, kitap.yazar gibi alanlara erişmeyi sağlar
            deger = getattr(kitap, kriter, "").lower()
            if anahtar_kelime.lower() in deger:
                sonuclar.append(kitap)
        return sonuclar

    def kitaplari_goster(self, liste=None):
        gosterilecek_liste = liste if liste is not None else self.envanter
        if not gosterilecek_liste:
            print("📭 Gösterilecek kitap bulunamadı.")
            return
        print("\n--- KÜTÜPHANE ENVANTERİ ---")
        for kitap in gosterilecek_liste:
            print(kitap)
        print("---------------------------\n")


# ---- KULLANIM ÖRNEĞİ (Test Etmek İçin) ----
if __name__ == "__main__":
    # Sistem başlatılıyor (Dosyadan veriler otomatik yüklenir)
    yonetici = EnvanterYonetimi()

    # Eğer dosya boşsa test verileri ekleyelim
    if not yonetici.envanter:
        yonetici.kitap_ekle(Kitap("Sefiller", "Victor Hugo", "12345", 5, "A-3"))
        yonetici.kitap_ekle(Kitap("Suç ve Ceza", "Dostoyevski", "67890", 3, "B-1"))
        yonetici.kitap_ekle(Kitap("Simyacı", "Paulo Coelho", "11223", 7, "A-1"))

    # 1. Listeleme
    yonetici.kitaplari_goster()

    # 2. Güncelleme Testi
    yonetici.kitap_guncelle("12345", yeni_stok=10, yeni_konum="A-4")

    # 3. Çok Kriterli Arama Testi (Örn: Yazara göre arama)
    print("🔎 'Hugo' yazarına göre arama sonuçları:")
    sonuclar = yonetici.kitap_ara("Hugo", kriter="yazar")
    yonetici.kitaplari_goster(sonuclar)