import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
from src.inventory import EnvanterYonetimi, Kitap
from src.transactions import IslemYonetimi

# Ana dizini bul ve src klasörüne erişim sağla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from src.auth import gui_login
from src.inventory import EnvanterYonetimi, Kitap

FLAMINGO_PATH = os.path.join(BASE_DIR, "assets", "flamingo.png")

ctk.set_appearance_mode("Dark")  

# Veritabanı motorunu ana ekran açılmadan başlatıyoruz
kutuphane_db = EnvanterYonetimi()
kutuphane_db = EnvanterYonetimi()
islem_db = IslemYonetimi(kutuphane_db)



# ==========================================
# 2. AŞAMA: ANA YÖNETİM PANELİ (DASHBOARD)
# ==========================================
def ana_menu_ac(kullanici_adi, rol):
    dashboard = ctk.CTkToplevel() # Giriş sayfasını çökertmemek için Toplevel kullanıyoruz
    dashboard.title(f"Bakırçay Akıllı Kütüphane - {rol.capitalize()} Paneli")
    dashboard.attributes("-fullscreen", True)
    dashboard.configure(fg_color="#121212")

    def tam_ekrandan_cik(event=None):
        dashboard.attributes("-fullscreen", False)
    dashboard.bind("<Escape>", tam_ekrandan_cik)

    # --- 1. SOL MENÜ (SIDEBAR) ---
    sidebar = ctk.CTkFrame(dashboard, width=280, corner_radius=0, fg_color="#005A67")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    lbl_logo = ctk.CTkLabel(sidebar, text="BAKIRÇAY\nKÜTÜPHANE", font=("Helvetica", 24, "bold"), text_color="white")
    lbl_logo.pack(pady=(50, 40))

    # --- 2. SAĞ İÇERİK ALANI ---
    icerik_alani = ctk.CTkFrame(dashboard, corner_radius=20, fg_color="#1E1E1E")
    icerik_alani.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # --- 3. SAYFA MOTORU ---
    def sayfayi_temizle():
        for widget in icerik_alani.winfo_children():
            widget.destroy()

    def sayfa_ana_ekran():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="Kontrol Paneli", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 20), padx=40, anchor="w")
        
        kart_frame = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        kart_frame.pack(fill="x", padx=40, pady=20)

        def bilgi_karti(parent, baslik, deger, renk):
            k = ctk.CTkFrame(parent, width=220, height=120, corner_radius=15, fg_color=renk)
            k.pack(side="left", padx=(0, 20), expand=True, fill="both")
            k.pack_propagate(False)
            ctk.CTkLabel(k, text=baslik, font=("Helvetica", 14), text_color="white").pack(pady=(20, 5))
            ctk.CTkLabel(k, text=str(deger), font=("Helvetica", 32, "bold"), text_color="white").pack()

        # ==========================================
        # 🚀 DİNAMİK VERİ ÇEKİM ALANI
        # ==========================================
        # 1. Toplam Kitap (inventory.py'den anlık çeker)
        guncel_kitap_sayisi = len(kutuphane_db.envanter)

        # 2. Aktif Ödünç ve Toplam Üye (Şimdilik Sabit)
        aktif_odunc_sayisi = len(islem_db.yapilan_islemler)
        toplam_uye_sayisi = 412

        bilgi_karti(kart_frame, "📚 Toplam Kitap", guncel_kitap_sayisi, "#007A87")
        bilgi_karti(kart_frame, "🔄 Aktif Ödünç", aktif_odunc_sayisi, "#D97706") # ARTIK CANLI!
        bilgi_karti(kart_frame, "👥 Toplam Üye", toplam_uye_sayisi, "#4338CA")

        # Hoş geldin mesajı (Sadece 1 tane)
        ctk.CTkLabel(icerik_alani, text=f"Hoş geldin {kullanici_adi}. Keyifli çalışmalar!", font=("Helvetica", 16), text_color="gray").pack(pady=40)
        
    # --- POP-UP: YENİ KİTAP EKLEME FORMU ---
    def kitap_ekle_popup():
        popup = ctk.CTkToplevel(dashboard)
        popup.title("Yeni Kitap Ekle")
        popup.geometry("450x580")
        popup.configure(fg_color="#1E1E1E")
        popup.attributes("-topmost", True)
        popup.resizable(False, False)

        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (450 // 2)
        y = (popup.winfo_screenheight() // 2) - (580 // 2)
        popup.geometry(f"+{x}+{y}")

        ctk.CTkLabel(popup, text="📖 Yeni Kitap Kaydı", font=("Helvetica", 24, "bold"), text_color="white").pack(pady=(20, 15))

        entry_stil = {"width": 350, "height": 40, "font": ("Helvetica", 14), "corner_radius": 10, "fg_color": "#2A2A2A", "border_color": "#007A87"}
        
        ad_entry = ctk.CTkEntry(popup, placeholder_text="Kitap Adı", **entry_stil)
        ad_entry.pack(pady=8)
        yazar_entry = ctk.CTkEntry(popup, placeholder_text="Yazar", **entry_stil)
        yazar_entry.pack(pady=8)
        isbn_entry = ctk.CTkEntry(popup, placeholder_text="ISBN", **entry_stil)
        isbn_entry.pack(pady=8)
        stok_entry = ctk.CTkEntry(popup, placeholder_text="Stok Adedi", **entry_stil)
        stok_entry.pack(pady=8)
        konum_entry = ctk.CTkEntry(popup, placeholder_text="Raf Konumu (Örn: A-1)", **entry_stil)
        konum_entry.pack(pady=8)

        def kaydet():
            yeni_kitap = Kitap(ad_entry.get(), yazar_entry.get(), isbn_entry.get(), stok_entry.get(), konum_entry.get())
            kutuphane_db.kitap_ekle(yeni_kitap)
            popup.destroy()
            sayfa_kitap_islemleri()

        buton_frame = ctk.CTkFrame(popup, fg_color="transparent")
        buton_frame.pack(pady=(20, 10))
        ctk.CTkButton(buton_frame, text="İptal", command=popup.destroy, width=140, height=45, fg_color="transparent", border_width=2, border_color="#7F1D1D", hover_color="#7F1D1D").pack(side="left", padx=15)
        ctk.CTkButton(buton_frame, text="Kaydet", command=kaydet, width=140, height=45, fg_color="#007A87", hover_color="#0097A7").pack(side="right", padx=15)

    
    # --- SAYFA: KİTAP İŞLEMLERİ (TABLO VE ARAMA) ---
    def sayfa_kitap_islemleri():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="📚 Kitap Envanteri", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 10), padx=40, anchor="w")
        
        # --- ÜST KONTROL BARI (Arama ve Ekleme Butonları) ---
        kontrol_bar = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        kontrol_bar.pack(fill="x", padx=40, pady=10)
        
        # 1. Kriter Seçimi (Açılır Menü)
        arama_kriteri = ctk.StringVar(value="ad")
        kriter_menu = ctk.CTkOptionMenu(kontrol_bar, variable=arama_kriteri, values=["ad", "yazar", "isbn", "konum"], width=100, height=40, fg_color="#2A2A2A", button_color="#007A87", button_hover_color="#0097A7")
        kriter_menu.pack(side="left", padx=(0, 10))

        # 2. Arama Kutusu
        arama_entry = ctk.CTkEntry(kontrol_bar, placeholder_text="Kitap, Yazar vb. ara...", width=250, height=40, font=("Helvetica", 14), fg_color="#2A2A2A", border_color="#007A87")
        arama_entry.pack(side="left", padx=(0, 10))

        # 3. Arama Motoru Tetikleyicisi
        def arama_yap():
            kelime = arama_entry.get()
            kriter = arama_kriteri.get()
            # Arkadaşının OOP motorundan arama sonuçlarını çekiyoruz!
            sonuclar = kutuphane_db.kitap_ara(kelime, kriter)
            tabloyu_doldur(sonuclar) # Tabloyu yeni sonuçlarla güncelle

        ctk.CTkButton(kontrol_bar, text="🔍 Ara", command=arama_yap, width=80, height=40, fg_color="#4338CA", hover_color="#3730A3").pack(side="left")
        
        # SADECE YÖNETİCİLER KİTAP EKLEYEBİLİR
        if rol == "yonetici":
            ctk.CTkButton(kontrol_bar, text="+ Yeni Kitap Ekle", command=kitap_ekle_popup, fg_color="#007A87", height=40, hover_color="#0097A7").pack(side="right")
        # --- TABLO BAŞLIKLARI ---
        tablo_baslik = ctk.CTkFrame(icerik_alani, fg_color="#2A2A2A", height=40)
        tablo_baslik.pack(fill="x", padx=40, pady=(10, 0))
        ctk.CTkLabel(tablo_baslik, text="Kitap Adı", width=250, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(tablo_baslik, text="Yazar", width=150, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(tablo_baslik, text="Konum", width=80, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(tablo_baslik, text="Stok", width=50, font=("Helvetica", 14, "bold")).pack(side="right", padx=20)

        liste_alani = ctk.CTkScrollableFrame(icerik_alani, fg_color="transparent")
        liste_alani.pack(fill="both", expand=True, padx=40, pady=5)
        
        # --- TABLOYU DOLDURMA MOTORU ---
        def tabloyu_doldur(gosterilecek_kitaplar):
            # Önce tablodaki eski sonuçları tamamen sil
            for widget in liste_alani.winfo_children():
                widget.destroy()

            # Eğer sonuç yoksa uyarı ver
            if not gosterilecek_kitaplar:
                ctk.CTkLabel(liste_alani, text="📭 Kriterlere uygun kitap bulunamadı.", font=("Helvetica", 16), text_color="gray").pack(pady=40)
                return

            # Sonuçları ekrana bas
            for kitap in gosterilecek_kitaplar:
                satir = ctk.CTkFrame(liste_alani, fg_color="transparent")
                satir.pack(fill="x", pady=8)
                
                ctk.CTkLabel(satir, text=kitap.ad, width=250, anchor="w", font=("Helvetica", 14)).pack(side="left", padx=10)
                ctk.CTkLabel(satir, text=kitap.yazar, width=150, anchor="w", text_color="gray").pack(side="left", padx=10)
                ctk.CTkLabel(satir, text=kitap.konum, width=80, anchor="w", text_color="#007A87", font=("Helvetica", 12, "bold")).pack(side="left", padx=10)
                
                stok_renk = "green" if kitap.stok > 0 else "#7F1D1D"
                ctk.CTkLabel(satir, text=f"Adet: {kitap.stok}", fg_color=stok_renk, corner_radius=10, width=60, height=28, text_color="white", font=("Helvetica", 12, "bold")).pack(side="right", padx=20)

        # Sayfa ilk açıldığında tüm kitapları göster (Boş arama)
        tabloyu_doldur(kutuphane_db.envanter)
    # --- SAYFA 3: ÖDÜNÇ VE CEZA TAKİBİ ---
    def sayfa_odunc_takibi():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="💸 Ödünç ve Ceza Takibi", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 10), padx=40, anchor="w")

        # --- ÜST BUTON BARI ---
        islem_bar = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        islem_bar.pack(fill="x", padx=40, pady=10)

        if rol == "yonetici":
            
            def hizli_odunc_ver():
                # Üst üste açılan input bug'ını çözmek için özel pop-up tasarımı!
                odunc_popup = ctk.CTkToplevel(icerik_alani)
                odunc_popup.title("Kitap Ödünç Ver")
                odunc_popup.geometry("400x350")
                odunc_popup.configure(fg_color="#1E1E1E")
                odunc_popup.attributes("-topmost", True)
                odunc_popup.resizable(False, False)
                
                # Pop-up'ı tam ekranın ortasına al
                odunc_popup.update_idletasks()
                x = (odunc_popup.winfo_screenwidth() // 2) - (400 // 2)
                y = (odunc_popup.winfo_screenheight() // 2) - (350 // 2)
                odunc_popup.geometry(f"+{x}+{y}")

                ctk.CTkLabel(odunc_popup, text="📤 Kitap Ödünç Verme", font=("Helvetica", 22, "bold"), text_color="white").pack(pady=(25, 20))

                isbn_entry = ctk.CTkEntry(odunc_popup, placeholder_text="Kitap ISBN Numarası", width=300, height=45, font=("Helvetica", 14), fg_color="#2A2A2A", border_color="#D97706")
                isbn_entry.pack(pady=10)

                ogrenci_entry = ctk.CTkEntry(odunc_popup, placeholder_text="Öğrenci Kullanıcı Adı (Örn: batuhan)", width=300, height=45, font=("Helvetica", 14), fg_color="#2A2A2A", border_color="#D97706")
                ogrenci_entry.pack(pady=10)

                def onayla():
                    isbn = isbn_entry.get()
                    ogrenci = ogrenci_entry.get()
                    if isbn and ogrenci:
                        basari, mesaj = islem_db.odunc_ver(isbn, ogrenci_adi=ogrenci.lower().strip())
                        print(f"[SİSTEM] {mesaj}")
                        odunc_popup.destroy()
                        sayfa_odunc_takibi() # Listeyi anında yenile!

                buton_frame = ctk.CTkFrame(odunc_popup, fg_color="transparent")
                buton_frame.pack(pady=(20, 10))
                
                ctk.CTkButton(buton_frame, text="İptal", command=odunc_popup.destroy, width=120, height=40, fg_color="transparent", border_width=2, border_color="#7F1D1D", hover_color="#7F1D1D").pack(side="left", padx=10)
                ctk.CTkButton(buton_frame, text="Onayla", command=onayla, width=120, height=40, fg_color="#D97706", hover_color="#B45309").pack(side="right", padx=10)

            def hizli_iade_al():
                dialog = ctk.CTkInputDialog(text="İade edilecek kitabın ISBN numarası:", title="İade Al")
                isbn = dialog.get_input()
                if isbn:
                    basari, mesaj = islem_db.iade_al(isbn)
                    print(f"[SİSTEM] {mesaj}")
                    sayfa_odunc_takibi() 

            def gecikenler_raporu_al():
                from src.reports import RaporMotoru
                raporlayici = RaporMotoru(islem_db)
                olusan_dosya = raporlayici.gecikenler_raporu_olustur()
                print(f"[SİSTEM RAPORU] Rapor alındı:\n📁 {olusan_dosya}")

            ctk.CTkButton(islem_bar, text="📤 Ödünç Ver", command=hizli_odunc_ver, fg_color="#D97706", hover_color="#B45309", height=40).pack(side="left", padx=10)
            ctk.CTkButton(islem_bar, text="📥 İade Al", command=hizli_iade_al, fg_color="#059669", hover_color="#047857", height=40).pack(side="left")
            ctk.CTkButton(islem_bar, text="📊 Gecikenleri Raporla", command=gecikenler_raporu_al, fg_color="#4F46E5", hover_color="#3730A3", height=40).pack(side="left", padx=10)

        # Tablo Başlıkları
        tablo_baslik = ctk.CTkFrame(icerik_alani, fg_color="#2A2A2A", height=40)
        tablo_baslik.pack(fill="x", padx=40, pady=(10, 0))
        ctk.CTkLabel(tablo_baslik, text="Kitap Adı", width=220, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(tablo_baslik, text="Veriliş", width=100, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(tablo_baslik, text="Son İade", width=100, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        
        # 👑 YÖNETİCİ EKRANINA ÖĞRENCİ SÜTUNU
        if rol == "yonetici":
            ctk.CTkLabel(tablo_baslik, text="Öğrenci", width=100, anchor="w", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)

        ctk.CTkLabel(tablo_baslik, text="Durum & Ceza", width=150, font=("Helvetica", 14, "bold")).pack(side="right", padx=20)

        liste_alani = ctk.CTkScrollableFrame(icerik_alani, fg_color="transparent")
        liste_alani.pack(fill="both", expand=True, padx=40, pady=5)

        # 🎯 ROL BAZLI FİLTRELEME ALGORİTMASI
        tum_islemler = islem_db.yapilan_islemler
        if rol == "yonetici":
            gosterilecek_islemler = tum_islemler
        else:
            # Öğrenci giriş yaptıysa sadece kendi kullanıcı adına açılmış logları filtrele
            gosterilecek_islemler = [i for i in tum_islemler if i.get("ogrenci_adi") == kullanici_adi.lower().strip()]

        if not gosterilecek_islemler:
            ctk.CTkLabel(liste_alani, text="📭 Aktif ödünç işlemi bulunmuyor.", font=("Helvetica", 16), text_color="gray").pack(pady=40)
            return

        import datetime 
        simdi = datetime.datetime.now()

        for islem in gosterilecek_islemler:
            satir = ctk.CTkFrame(liste_alani, fg_color="transparent")
            satir.pack(fill="x", pady=8)

            ctk.CTkLabel(satir, text=islem["kitap_ad"], width=220, anchor="w", font=("Helvetica", 14)).pack(side="left", padx=10)

            verilis_str = islem["verilis_tarihi"].strftime("%d/%m/%Y")
            iade_str = islem["iade_tarihi"].strftime("%d/%m/%Y")

            ctk.CTkLabel(satir, text=verilis_str, width=100, anchor="w", text_color="gray").pack(side="left", padx=10)
            ctk.CTkLabel(satir, text=iade_str, width=100, anchor="w", text_color="gray").pack(side="left", padx=10)

            # 👑 YÖNETİCİ EKRANINDA HANGİ ÖĞRENCİDE OLDUĞUNU YAZ
            if rol == "yonetici":
                ctk.CTkLabel(satir, text=islem.get("ogrenci_adi", "bilinmiyor"), width=100, anchor="w", text_color="#007A87", font=("Helvetica", 13, "bold")).pack(side="left", padx=10)

            iade_vakti = islem["iade_tarihi"]
            if simdi > iade_vakti:
                gecikme = (simdi - iade_vakti).days
                ceza = gecikme * islem_db.GUNLUK_CEZA
                durum_metni = f"{gecikme} Gün Gecikti | {ceza} TL"
                renk = "#7F1D1D" 
            else:
                kalan = (iade_vakti - simdi).days
                durum_metni = f"{kalan} Gün Kaldı"
                renk = "green" 

            ctk.CTkLabel(satir, text=durum_metni, fg_color=renk, corner_radius=10, width=150, height=28, text_color="white", font=("Helvetica", 12, "bold")).pack(side="right", padx=20)
    # --- 4. SIDEBAR BUTONLARI ---
    btn_font = ("Helvetica", 16, "bold")
    
    btn_ana = ctk.CTkButton(sidebar, text="  🏠  Ana Sayfa", command=sayfa_ana_ekran, height=50, anchor="w", font=btn_font, fg_color="transparent", hover_color="#007A87")
    btn_ana.pack(fill="x", pady=10, padx=15)

    btn_kitaplar = ctk.CTkButton(sidebar, text="  📚  Kitap İşlemleri", command=sayfa_kitap_islemleri, height=50, anchor="w", font=btn_font, fg_color="transparent", hover_color="#007A87")
    btn_kitaplar.pack(fill="x", pady=10, padx=15)

    btn_odunc = ctk.CTkButton(sidebar, text="  💸  Ödünç ve Ceza", command=sayfa_odunc_takibi, height=50, anchor="w", font=btn_font, fg_color="transparent", hover_color="#007A87")
    btn_odunc.pack(fill="x", pady=10, padx=15)

    ctk.CTkLabel(sidebar, text="").pack(expand=True) # Kapat butonuyla araya boşluk atar

    # BUNDAN SONRA SENİN KODDAKİ "def tam_cikis():" KISMI DEVAM EDECEK...
    def tam_cikis():
        app.destroy()
        
    btn_kapat = ctk.CTkButton(sidebar, text="  🚪  Sistemi Kapat", command=tam_cikis, height=50, font=btn_font, fg_color="#7F1D1D", hover_color="#991B1B")
    btn_kapat.pack(fill="x", pady=30, padx=15)

    # Motoru ilk açılışta ana sayfaya yönlendir
    sayfa_ana_ekran()


# ==========================================
# 1. AŞAMA: GİRİŞ EKRANI
# ==========================================
def giris_butonuna_tiklandi(): 
    kullanici = entry_kullanici.get()
    sifre = entry_sifre.get()
    
    if not kullanici:
        messagebox.showwarning("Uyarı", "Lütfen kullanıcı adınızı girin!")
        return
        
    basarili_mi, rol, mesaj = gui_login(kullanici, sifre)
    
    if basarili_mi:
        app.withdraw() # Ana ekranı çökertmemek için destroy değil withdraw yapıyoruz
        ana_menu_ac(kullanici, rol)
    else:
        messagebox.showerror("Giriş Başarısız", mesaj)

app = ctk.CTk()
app.title("Bakırçay Akıllı Kütüphane")
app.attributes("-fullscreen", True)
app.configure(fg_color="#0097A7")

def tam_ekrandan_cik_login(event=None):
    app.attributes("-fullscreen", False)
app.bind("<Escape>", tam_ekrandan_cik_login)

merkez_kutu = ctk.CTkFrame(app, fg_color="transparent")
merkez_kutu.place(relx=0.5, rely=0.5, anchor="center")

try:
    flamingo_img = ctk.CTkImage(light_image=Image.open(FLAMINGO_PATH), dark_image=Image.open(FLAMINGO_PATH), size=(180, 180))
    ctk.CTkLabel(merkez_kutu, text="", image=flamingo_img).pack(pady=(0, 20))
except:
    pass

ctk.CTkLabel(merkez_kutu, text="BAKIRÇAY ÜNİVERSİTESİ\nAKILLI KÜTÜPHANE", font=("Helvetica", 40, "bold"), text_color="white").pack(pady=(0, 40))

entry_kullanici = ctk.CTkEntry(merkez_kutu, placeholder_text="Kullanıcı Adı", width=450, height=65, font=("Helvetica", 20), fg_color="#007A87", border_color="#00FFFF")
entry_kullanici.pack(pady=15)

sifre_frame = ctk.CTkFrame(merkez_kutu, fg_color="transparent")
sifre_frame.pack(pady=15)
entry_sifre = ctk.CTkEntry(sifre_frame, placeholder_text="Şifre", width=375, height=65, show="*", font=("Helvetica", 20), fg_color="#007A87", border_color="#00FFFF")
entry_sifre.pack(side="left", padx=(0, 10))

def sifre_toggle():
    if entry_sifre.cget("show") == "*":
        entry_sifre.configure(show="")
        btn_goz.configure(text="🙈")
    else:
        entry_sifre.configure(show="*")
        btn_goz.configure(text="👁")

btn_goz = ctk.CTkButton(sifre_frame, text="👁", command=sifre_toggle, width=65, height=65, fg_color="#007A87")
btn_goz.pack(side="left")

ctk.CTkButton(merkez_kutu, text="Giriş Yap", command=giris_butonuna_tiklandi, width=450, height=75, fg_color="black", font=("Helvetica", 28, "bold")).pack(pady=30)
ctk.CTkButton(merkez_kutu, text="Sistemden Çık", command=app.destroy, width=450, height=50, fg_color="transparent", border_width=2, border_color="black").pack(pady=10)

app.mainloop()