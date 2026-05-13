import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
import threading
from src.assistant import flamingo_konus

# Ana dizini bul ve src klasörüne erişim sağla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from src.auth import gui_login

FLAMINGO_PATH = os.path.join(BASE_DIR, "assets", "flamingo.png")

ctk.set_appearance_mode("Dark")  

# ==========================================
# 2. AŞAMA: ANA YÖNETİM PANELİ (TAM EKRAN & MODERN DASHBOARD)
# ==========================================
def ana_menu_ac(kullanici_adi, rol):
    dashboard = ctk.CTk()
    dashboard.title(f"Bakırçay Akıllı Kütüphane - {rol.capitalize()} Paneli")
    
    # Tam Ekran Ayarları
    dashboard.attributes("-fullscreen", True)
    dashboard.configure(fg_color="#121212") # İçerik arkaplanı (Koyu Gri/Siyah)

    def tam_ekrandan_cik(event=None):
        dashboard.attributes("-fullscreen", False)
    dashboard.bind("<Escape>", tam_ekrandan_cik)

    # --- SOL MENÜ (SIDEBAR) ---
    # Sidebar rengini giriş ekranıyla uyumlu Koyu Turkuaz yaptık
    sidebar = ctk.CTkFrame(dashboard, width=280, corner_radius=0, fg_color="#005A67")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False) # Genişliği sabit tutar

    lbl_logo = ctk.CTkLabel(sidebar, text="BAKIRÇAY\nKÜTÜPHANE", font=("Helvetica", 26, "bold"), text_color="white")
    lbl_logo.pack(pady=(50, 40))

    # --- SAĞ İÇERİK ALANI ---
    icerik_alani = ctk.CTkFrame(dashboard, corner_radius=20, fg_color="#1E1E1E")
    icerik_alani.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # --- SAYFA MOTORU ---
    def sayfayi_temizle():
        for widget in icerik_alani.winfo_children():
            widget.destroy()

    def sayfa_ana_ekran():
        sayfayi_temizle()
        
        # Üst Başlık Kısmı
        ust_frame = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        ust_frame.pack(fill="x", padx=40, pady=(40, 20))
        
        ctk.CTkLabel(ust_frame, text="Kontrol Paneli", font=("Helvetica", 32, "bold"), text_color="white").pack(side="left")
        
        kullanici_bilgi = f"👤 {kullanici_adi} ({rol.capitalize()})"
        ctk.CTkLabel(ust_frame, text=kullanici_bilgi, font=("Helvetica", 18), text_color="#A0C4FF").pack(side="right")

        # Özet Kartları İçin Taşıyıcı
        kart_frame = ctk.CTkFrame(icerik_alani, fg_color="transparent")
        kart_frame.pack(fill="x", padx=40, pady=20)

        # Kart Üretici Fonksiyon
        def bilgi_karti_olustur(parent, baslik, deger, renk):
            kart = ctk.CTkFrame(parent, width=250, height=120, corner_radius=15, fg_color=renk)
            kart.pack(side="left", padx=(0, 20), expand=True, fill="both")
            kart.pack_propagate(False)
            ctk.CTkLabel(kart, text=baslik, font=("Helvetica", 16), text_color="white").pack(pady=(20, 5))
            ctk.CTkLabel(kart, text=deger, font=("Helvetica", 36, "bold"), text_color="white").pack()

        # Modern Renkli Kartlar
        bilgi_karti_olustur(kart_frame, "📚 Toplam Kitap", "1,248", "#007A87")
        bilgi_karti_olustur(kart_frame, "🔄 Aktif Ödünç", "34", "#D97706")
        bilgi_karti_olustur(kart_frame, "👥 Toplam Üye", "412", "#4338CA")
        
        # Alt Bilgi Alanı
        ctk.CTkLabel(icerik_alani, text="Son İşlemler buraya listelenecek...", font=("Helvetica", 16), text_color="gray").pack(pady=50)

    def sayfa_kitap_islemleri():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="📚 Kitap Envanteri", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 20), padx=40, anchor="w")
        ctk.CTkLabel(icerik_alani, text="Kitap ekleme, silme ve arama modülleri buraya entegre edilecek.", font=("Helvetica", 16), text_color="gray").pack(padx=40, anchor="w")

    def sayfa_kullanici_yonetimi():
        sayfayi_temizle()
        ctk.CTkLabel(icerik_alani, text="👥 Kullanıcı Yönetimi", font=("Helvetica", 32, "bold"), text_color="white").pack(pady=(40, 20), padx=40, anchor="w")
        ctk.CTkLabel(icerik_alani, text="Kullanıcı veritabanı bağlantısı bekleniyor.", font=("Helvetica", 16), text_color="gray").pack(padx=40, anchor="w")

    def cikis_yap():
        dashboard.destroy()
        # İstenirse burada tekrar ana login ekranı (app) çağrılabilir, şimdilik programı kapatıyor.

    # --- YAN MENÜ BUTONLARI ---
    # Buton tasarımlarını daha ferah ve hover efektli yaptık
    btn_ana = ctk.CTkButton(sidebar, text="   🏠 Ana Sayfa", command=sayfa_ana_ekran, height=50, anchor="w", 
                            font=("Helvetica", 16, "bold"), fg_color="transparent", text_color="white", hover_color="#004652")
    btn_ana.pack(fill="x", pady=5, padx=15)

    btn_kitaplar = ctk.CTkButton(sidebar, text="   📚 Kitap İşlemleri", command=sayfa_kitap_islemleri, height=50, anchor="w", 
                                 font=("Helvetica", 16, "bold"), fg_color="transparent", text_color="white", hover_color="#004652")
    btn_kitaplar.pack(fill="x", pady=5, padx=15)

    btn_kullanicilar = ctk.CTkButton(sidebar, text="   👥 Kullanıcı Yönetimi", command=sayfa_kullanici_yonetimi, height=50, anchor="w", 
                                     font=("Helvetica", 16, "bold"), fg_color="transparent", text_color="white", hover_color="#004652")
    btn_kullanicilar.pack(fill="x", pady=5, padx=15)

    btn_odunc = ctk.CTkButton(sidebar, text="   🔄 Ödünç / İade", height=50, anchor="w", 
                              font=("Helvetica", 16, "bold"), fg_color="transparent", text_color="white", hover_color="#004652")
    btn_odunc.pack(fill="x", pady=5, padx=15)

    # En alta güvenli çıkış butonu
    btn_kapat = ctk.CTkButton(sidebar, text="🚪 Sistemi Kapat", command=cikis_yap, height=50, 
                              font=("Helvetica", 16, "bold"), fg_color="#7F1D1D", text_color="white", hover_color="#991B1B")
    btn_kapat.pack(side="bottom", fill="x", pady=30, padx=20)

    sayfa_ana_ekran() # İlk açılış
    dashboard.mainloop()


# ==========================================
# 1. AŞAMA: GİRİŞ EKRANI (TAM EKRAN & CYAN KONSEPT)
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

def tam_ekrandan_cik(event=None):
    app.attributes("-fullscreen", False)

app = ctk.CTk()
app.title("Bakırçay Akıllı Kütüphane")

app.attributes("-fullscreen", True)
app.configure(fg_color="#0097A7") 
app.bind("<Escape>", tam_ekrandan_cik)

merkez_kutu = ctk.CTkFrame(app, fg_color="transparent")
merkez_kutu.place(relx=0.5, rely=0.5, anchor="center")

# --- FLAMINGO GÖRSELİ ---
try:
    flamingo_img = ctk.CTkImage(light_image=Image.open(FLAMINGO_PATH),
                                dark_image=Image.open(FLAMINGO_PATH),
                                size=(180, 180)) 
    lbl_resim = ctk.CTkLabel(merkez_kutu, text="", image=flamingo_img)
    lbl_resim.pack(pady=(0, 20))
except Exception as e:
    lbl_resim = ctk.CTkLabel(merkez_kutu, text="[Flamingo Görseli Bulunamadı!]", text_color="red")
    lbl_resim.pack(pady=(0, 20))

# --- BÜYÜK BAŞLIK ---
lbl_baslik = ctk.CTkLabel(merkez_kutu, text="BAKIRÇAY ÜNİVERSİTESİ\nAKILLI KÜTÜPHANE", font=("Helvetica", 40, "bold"), text_color="white")
lbl_baslik.pack(pady=(0, 40))

# --- GİRİŞ KUTULARI ---
entry_kullanici = ctk.CTkEntry(merkez_kutu, placeholder_text="Kullanıcı Adı", 
                               placeholder_text_color="white",
                               width=450, height=65, font=("Helvetica", 20), 
                               text_color="white", fg_color="#007A87", 
                               border_color="#00FFFF", border_width=2)
entry_kullanici.pack(pady=15)

sifre_frame = ctk.CTkFrame(merkez_kutu, fg_color="transparent")
sifre_frame.pack(pady=15)

entry_sifre = ctk.CTkEntry(sifre_frame, placeholder_text="Şifre", 
                           placeholder_text_color="white",
                           width=375, height=65, show="*", font=("Helvetica", 20), 
                           text_color="white", fg_color="#007A87", 
                           border_color="#00FFFF", border_width=2)
entry_sifre.pack(side="left", padx=(0, 10))

def sifre_goster_gizle():
    if entry_sifre.cget("show") == "*":
        entry_sifre.configure(show="")
        btn_goz.configure(text="🙈") 
    else:
        entry_sifre.configure(show="*")
        btn_goz.configure(text="👁") 

btn_goz = ctk.CTkButton(sifre_frame, text="👁", command=sifre_goster_gizle,
                        width=65, height=65, fg_color="#007A87", 
                        hover_color="#005A67", border_color="#00FFFF", border_width=2,
                        font=("Helvetica", 24))
btn_goz.pack(side="left")

# --- SİYAH BUTON ---
btn_giris = ctk.CTkButton(merkez_kutu, text="Giriş Yap", command=giris_butonuna_tiklandi, 
                          width=450, height=75, 
                          fg_color="black", hover_color="#222222", 
                          font=("Helvetica", 28, "bold"), text_color="white")
btn_giris.pack(pady=30)

# --- ÇIKIŞ BUTONU ---
btn_cikis = ctk.CTkButton(merkez_kutu, text="Sistemden Çık", command=app.destroy, 
                          width=450, height=50, 
                          fg_color="transparent", border_width=2, border_color="black", hover_color="black",
                          font=("Helvetica", 18, "bold"), text_color="white")
btn_cikis.pack(pady=10)

lbl_alt_bilgi = ctk.CTkLabel(merkez_kutu, text="Touch ID ile giriş yapmak için kullanıcı adına 'admin' yazın.\nTam ekrandan çıkmak için ESC tuşunu kullanabilirsiniz.", font=("Helvetica", 15), text_color="#E0FFFF")
lbl_alt_bilgi.pack(pady=30)

app.mainloop()