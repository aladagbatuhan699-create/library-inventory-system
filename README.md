# 📚 Bakırçay Akıllı Kütüphane Yönetim Sistemi

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![UI](https://img.shields.io/badge/GUI-CustomTkinter-success.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Security](https://img.shields.io/badge/Security-SHA256%20%7C%20Touch%20ID-critical.svg)](#)

İzmir Bakırçay Üniversitesi Bilgisayar Mühendisliği proje ekibi tarafından geliştirilen; modern arayüzü, üst düzey siber güvenlik katmanları ve nesne yönelimli (OOP) mimarisi ile öne çıkan yeni nesil kütüphane otomasyon sistemi.

## 🚀 Proje Hakkında

Bu proje, geleneksel konsol tabanlı kütüphane sistemlerini modern bir masaüstü uygulamasına dönüştürmek amacıyla geliştirilmiştir. Sistem, kullanıcı dostu bir grafik arayüzün (GUI) arkasında; rol tabanlı yetkilendirme (RBAC), dinamik stok takibi, biyometrik doğrulama ve gelişmiş algoritmalara sahip bir ceza/ödünç motoru barındırmaktadır.

## ✨ Öne Çıkan Özellikler

- **🔒 Biyometrik Güvenlik ve Kriptolama:** - Yönetici (Admin) girişleri için macOS `LocalAuthentication` kütüphanesi kullanılarak **Touch ID** entegrasyonu sağlanmıştır.
  - Öğrenci ve personel şifreleri veritabanında düz metin olarak değil, `hashlib` ile **SHA-256** formatında maskelenerek saklanır.
- **👥 Rol Tabanlı Erişim Kontrolü (RBAC):** Yönetici ve standart kullanıcı (öğrenci) hesapları için dinamik arayüz. Standart kullanıcılar yalnızca kitap sorgulayabilirken, yöneticiler tam yetkiye (ödünç verme, kitap ekleme) sahiptir.
- **📊 Gerçek Zamanlı Envanter:** İşlemler yapıldıkça eşzamanlı güncellenen ve dosya sistemine kaydedilen canlı stok takibi.
- **💸 Akıllı Ceza Motoru:** Ödünç alınan kitapların iade tarihlerini otomatik hesaplayan, gecikme durumunda günlük periyotlarla TL cinsinden ceza yansıtan dinamik takip tablosu.

## 🛠️ Kullanılan Teknolojiler ve Mimari

- **Programlama Dili:** Python 3
- **Arayüz (Frontend):** CustomTkinter (Modern, karanlık tema destekli GUI)
- **Veri Kalıcılığı (Backend):** Senkronize TXT tabanlı dosya işleme mimarisi
- **Modüler Yapı:** Proje `auth.py`, `inventory.py`, `transactions.py` gibi özelleşmiş modüllere bölünerek S.O.L.I.D. prensiplerine uygun tasarlanmıştır.

## 📂 Klasör Mimarisi

\`\`\`bash
Kütüphane_Envanter_Sistemi/
└── kutuphane_sistemi/
    ├── data/
    │   └── users.txt          # Kriptolu kullanıcı veritabanı
    ├── src/
    │   ├── auth.py            # Kimlik doğrulama, Hash ve Touch ID motoru
    │   ├── inventory.py       # Envanter ve OOP tabanlı kitap sınıfları
    │   └── transactions.py    # Ödünç ve ceza hesaplama motoru
    ├── assets/                # İkonlar ve görseller
    ├── gui_test.py            # Ana arayüz ve sayfa tasarımları
    ├── main.py                # Sistemi başlatan tetikleyici dosya
    └── kitaplar.txt           # Canlı kütüphane envanteri
\`\`\`

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın:**
   \`\`\`bash
   git clone https://github.com/aladagbatuhan699-create/library-inventory-system.git
   \`\`\`
2. **Proje Dizinine Girin:**
   \`\`\`bash
   cd library-inventory-system/kutuphane_sistemi
   \`\`\`
3. **Gerekli Kütüphaneleri Yükleyin:**
   \`\`\`bash
   pip install customtkinter
   \`\`\`
4. **Uygulamayı Başlatın:**
   \`\`\`bash
   python main.py
   \`\`\`

## 👨‍💻 Geliştirici Ekip
- **Batuhan** - *Sistem Entegrasyonu, GUI Tasarımı ve Güvenlik Altyapısı*
- **Deniz** - *Backend Mantığı*
- **Elif** - *Backend Mantığı*
- **Damla** - *Backend Mantığı*

*Bu proje, takım çalışması ve ileri seviye yazılım prensipleri (Clean Code, Version Control) gözetilerek geliştirilmiştir.*
