import pyttsx3

def flamingo_konus(kullanici_adi, rol):
    """Flamingo'nun asenkron olarak konuşmasını sağlar."""
    # Ses motorunu başlat
    engine = pyttsx3.init()
    
    # Konuşma hızını biraz daha insani bir seviyeye çekelim
    engine.setProperty('rate', 160) 
    
    # Şimdilik örnek bir rapor verisi oluşturuyoruz (İleride transactions'dan çekeceğiz)
    ornek_odunc = 12
    ornek_iade = 5
    
    mesaj = f"Hoş geldin {kullanici_adi}. Sisteme {rol} yetkisi ile giriş yaptın. Dün toplam {ornek_odunc} kitap ödünç alındı, {ornek_iade} kitap iade edildi. İyi çalışmalar dilerim."
    
    print(f"🦩 Flamingo: {mesaj}")
    
    engine.say(mesaj)
    engine.runAndWait()
    