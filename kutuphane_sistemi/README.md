# library-inventory-system
📚 Kütüphane Envanter Yönetim Sistemi
İzmir Bakırçay Üniversitesi

BIL1203 Mühendislikte Proje Yönetimi - Dönem Sonu Projesi

Bu proje, bir kütüphanenin kitap envanterini, kullanıcı yetkilendirmelerini ve ödünç alma/iade süreçlerini yönetmek amacıyla geliştirilmiş modüler bir Python uygulamasıdır.

🚀 Özellikler (İş Paketleri)
Proje, "WhatsApp Image 2026-05-04 at 15.07.01.jpeg" dosyasında belirtilen tüm akademik gereksinimleri karşılamaktadır:

Güvenli Giriş Sistemi: Yönetici, Personel ve Öğrenci rolleri için farklı yetkilendirme seviyeleri.

Envanter Yönetimi: Kitap ekleme, silme ve güncelleme (ISBN, stok ve konum takibi).

Gelişmiş Arama: Çok kriterli filtreleme ve detaylı sonuç gösterme algoritması.

Ödünç İşlemleri: Süre takibi, iade yönetimi ve gecikme hesaplamaları.

Raporlama: Popüler kitaplar ve envanter özetleri için istatistiksel analizler.

📂 Proje Yapısı
Sistem, sürdürülebilirlik ve ekip çalışması için modüler bir mimariyle tasarlanmıştır:

Plaintext
kutuphane_sistemi/
├── main.py             # Uygulama giriş noktası
├── src/                # Mantıksal modüller
│   ├── auth.py         # Giriş ve yetki kontrolü
│   ├── inventory.py    # Kitap yönetimi
│   ├── transactions.py # Ödünç/İade işlemleri
│   └── reports.py      # İstatistik ve raporlama
├── data/               # .txt tabanlı kalıcı veri depolama
└── docs/               # Proje dokümantasyonu ve raporlar
🛠️ Kurulum
Projeyi yerelinizde çalıştırmak için:

Repoyu klonlayın: git clone [https://github.com/aladagbatuhan699-create/library-inventory-system.git]

Sanal ortamı oluşturun: python3 -m venv venv

Aktif edin: source venv/bin/activate

Uygulamayı başlatın: python3 main.py
👥 Ekip ve Rol Dağılımı
Batuhan Aladağ: Proje Yöneticisi & Güvenlik Mimarı