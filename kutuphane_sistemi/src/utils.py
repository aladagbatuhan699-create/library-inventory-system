import os
from datetime import datetime

def proje_kok_dizini_bul():
    """Projenin ana klasör yolunu (Kütüphane_Envanter_Sistemi) dinamik olarak bulur."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def veri_dosyasi_yolu(dosya_adi):
    """'data' klasörü içindeki dosyaların tam yolunu güvenli bir şekilde oluşturur."""
    kok_dizin = proje_kok_dizini_bul()
    veri_klasoru = os.path.join(kok_dizin, "data")
    
    # Eğer data klasörü yoksa otomatik oluştur
    if not os.path.exists(veri_klasoru):
        os.makedirs(veri_klasoru)
        
    return os.path.join(veri_klasoru, dosya_adi)

def turkce_tarih_formati(tarih_objesi):
    """Tarihleri Türkiye standartlarına (Gün/Ay/Yıl) çevirir."""
    if isinstance(tarih_objesi, datetime):
        return tarih_objesi.strftime("%d/%m/%Y")
    return "Tarih Yok"

def terminal_temizle():
    """İşletim sistemine göre (Mac/Windows) terminal ekranını temizler."""
    os.system('clear' if os.name == 'posix' else 'cls')