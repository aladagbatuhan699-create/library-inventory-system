import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
import threading

# Ana dizini bul ve src klasörüne erişim sağla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from src.auth import gui_login
from src.assistant import flamingo_konus

FLAMINGO_PATH = os.path.join(BASE_DIR, "assets", "flamingo.png")

ctk.set_appearance_mode("Dark")  

# ==========================================
# 2. AŞAMA: ANA YÖNETİM PANELİ (DASHBOARD)
# ==========================================
def ana_menu_ac(kullanici_adi, rol):
    dashboard = ctk.CTk()
    dashboard.title(f"Bakırçay Akıllı Kütüphane - {rol.capitalize()} Paneli")
    dashboard.attributes("-fullscreen", True)
    dashboard.configure(fg_color="#121212") # Ana arka plan koyu gri/siyah

    def tam_ekrandan_cik(event=None):
        dashboard.attributes("-fullscreen", False)
    dashboard.bind("<Escape>", tam_ekrandan_cik)

    # --- 1. SOL MENÜ (SIDEBAR) ---
    sidebar = ctk.CTkFrame(dashboard, width=280, corner_radius=0, fg_color="#005A67")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    lbl_logo = ctk.CTkLabel(sidebar, text="BAKIRÇAY\nKÜTÜPHANE", font=("Helvetica", 24, "bold"), text_color="white")
    lbl_logo.pack(pady=(50, 40))

    # --- 2. SAĞ İÇERİK ALANI (Burası siyah olan yerdi, şimdi canlanacak) ---
    icerik_alani = ctk.CTkFrame(dashboard, corner_radius=20, fg_color="#1E1E1E")
    icerik_alani.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # --- 3. SAYFA MOTORU (Fonksiyonlar) ---
    def sayfayi_temizle():
        for widget in icerik_alani.winfo_children():
            widget.destroy()

    def sayfa_ana_ekran():
        sayfayi_temizle()
        # Başlık Bölümü
        ctk.CTkLabel(icerik_alani, text="Kontrol Paneli", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 20), padx=40, anchor="w")
        
        # Kartlar için taşıyıcı
        kart_frame = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        kart_frame.pack(fill="x", padx=40, pady=20)

        def bilgi_karti(parent, baslik, deger, renk):
            k = ctk.CTkFrame(parent, width=220, height=120, corner_radius=15, fg_color=renk)
            k.pack(side="left", padx=(0, 20), expand=True, fill="both")
            k.pack_propagate(False)
            ctk.CTkLabel(k, text=baslik, font=("Helvetica", 14), text_color="white").pack(pady=(20, 5))
            ctk.CTkLabel(k, text=deger, font=("Helvetica", 32, "bold"), text_color="white").pack()

        bilgi_karti(kart_frame, "📚 Toplam Kitap", "1,248", "#007A87")
        bilgi_karti(kart_frame, "🔄 Aktif Ödünç", "34", "#D97706")
        bilgi_karti(kart_frame, "👥 Toplam Üye", "412", "#4338CA")

        ctk.CTkLabel(icerik_alani, text=f"Hoş geldin {kullanici_adi}. Keyifli çalışmalar!", font=("Helvetica", 16), text_color="gray").pack(pady=40)

    def sayfa_kitap_islemleri():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="📚 Kitap Envanteri", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 20), padx=40, anchor="w")
        
        # Basit Tablo İskeleti
        tablo_frame = ctk.CTkFrame(icerik_alani, fg_color="#2A2A2A")
        tablo_frame.pack(fill="both", expand=True, padx=40, pady=20)
        ctk.CTkLabel(tablo_frame, text="Veriler yükleniyor... (inventory.py bekleniyor)", font=("Helvetica", 14), text_color="gray").place(relx=0.5, rely=0.5, anchor="center")

    # --- 4. SIDEBAR BUTONLARI ---
    btn_params = {
        "height": 55, "corner_radius": 12, "anchor": "w", 
        "font": ("Helvetica", 15, "bold"), "fg_color": "#007A87", 
        "hover_color": "#0097A7", "text_color": "white"
    }

    btn_ana = ctk.CTkButton(sidebar, text="🏠   Ana Sayfa", command=sayfa_ana_ekran, **btn_params)
    btn_ana.pack(fill="x", pady=(0, 12), padx=15)

    btn_kitaplar = ctk.CTkButton(sidebar, text="📚   Kitap İşlemleri", command=sayfa_kitap_islemleri, **btn_params)
    btn_kitaplar.pack(fill="x", pady=12, padx=15)

    ctk.CTkLabel(sidebar, text="").pack(expand=True) # Esnek boşluk

    btn_kapat = ctk.CTkButton(sidebar, text="🚪   Sistemi Kapat", command=dashboard.destroy, 
                              height=55, corner_radius=12, fg_color="#991B1B", hover_color="#B91C1C", font=("Helvetica", 15, "bold"))
    btn_kapat.pack(fill="x", pady=30, padx=15)

    # --- 5. BAŞLANGIÇ ---
    sayfa_ana_ekran() # Program açılınca sağ taraf boş kalmasın!
    dashboard.mainloop()
    # --- SAYFA: KİTAP İŞLEMLERİ (TABLO) ---
    def sayfa_kitap_islemleri():
        sayfayi_temizle()
        
        ust_bar = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        ust_bar.pack(fill="x", padx=40, pady=(30, 10))
        ctk.CTkLabel(ust_bar, text="📚 Kitap Envanteri", font=("Helvetica", 28, "bold"), text_color="white").pack(side="left")
        
        # Arama ve Ekle
        kontrol_bar = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        kontrol_bar.pack(fill="x", padx=40, pady=10)
        ctk.CTkEntry(kontrol_bar, placeholder_text="Kitap veya yazar ara...", width=350, height=40).pack(side="left")
        ctk.CTkButton(kontrol_bar, text="+ Yeni Kitap Ekle", fg_color="#007A87", height=40).pack(side="right")

        # Tablo Başlıkları
        tablo_baslik = ctk.CTkFrame(icerik_alani, fg_color="#2A2A2A", height=40)
        tablo_baslik.pack(fill="x", padx=40, pady=(20, 0))
        ctk.CTkLabel(tablo_baslik, text="Kitap Adı", width=300, anchor="w", font=("Helvetica", 13, "bold")).pack(side="left", padx=20)
        ctk.CTkLabel(tablo_baslik, text="Durum", width=100, font=("Helvetica", 13, "bold")).pack(side="right", padx=20)

        # Liste Alanı
        liste = ctk.CTkScrollableFrame(icerik_alani, fg_color="transparent")
        liste.pack(fill="both", expand=True, padx=40, pady=5)
        
        ornekler = [("Python Programlama", "Rafta", "green"), ("C++ Pro", "Ödünçte", "orange"), ("Algoritmalar", "Rafta", "green")]
        for ad, durum, renk in ornekler:
            satir = ctk.CTkFrame(liste, fg_color="transparent")
            satir.pack(fill="x", pady=5)
            ctk.CTkLabel(satir, text=ad, width=300, anchor="w").pack(side="left", padx=20)
            ctk.CTkLabel(satir, text=durum, fg_color=renk, corner_radius=10, width=80).pack(side="right", padx=20)

    # --- SIDEBAR BUTONLARI ---
    btn_font = ("Helvetica", 16, "bold")
    
    btn_ana = ctk.CTkButton(sidebar, text="  🏠  Ana Sayfa", command=sayfa_ana_ekran, 
                            height=50, anchor="w", font=btn_font, fg_color="transparent", hover_color="#007A87")
    btn_ana.pack(fill="x", pady=10, padx=15)

    btn_kitaplar = ctk.CTkButton(sidebar, text="  📚  Kitap İşlemleri", command=sayfa_kitap_islemleri, 
                                 height=50, anchor="w", font=btn_font, fg_color="transparent", hover_color="#007A87")
    btn_kitaplar.pack(fill="x", pady=10, padx=15)

    ctk.CTkLabel(sidebar, text="").pack(expand=True) # Boşluk bırakır

    btn_kapat = ctk.CTkButton(sidebar, text="  🚪  Sistemi Kapat", command=dashboard.destroy, 
                              height=50, font=btn_font, fg_color="#7F1D1D", hover_color="#991B1B")
    btn_kapat.pack(fill="x", pady=30, padx=15)

    sayfa_ana_ekran()
    dashboard.mainloop()

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
        threading.Thread(target=flamingo_konus, args=(kullanici, rol)).start()
        app.destroy()
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

# Flamingo Logo
try:
    flamingo_img = ctk.CTkImage(light_image=Image.open(FLAMINGO_PATH), dark_image=Image.open(FLAMINGO_PATH), size=(180, 180))
    ctk.CTkLabel(merkez_kutu, text="", image=flamingo_img).pack(pady=(0, 20))
except:
    pass

ctk.CTkLabel(merkez_kutu, text="BAKIRÇAY ÜNİVERSİTESİ\nAKILLI KÜTÜPHANE", font=("Helvetica", 40, "bold"), text_color="white").pack(pady=(0, 40))

entry_kullanici = ctk.CTkEntry(merkez_kutu, placeholder_text="Kullanıcı Adı", width=450, height=65, font=("Helvetica", 20), fg_color="#007A87", border_color="#00FFFF")
entry_kullanici.pack(pady=15)

# Şifre Alanı
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