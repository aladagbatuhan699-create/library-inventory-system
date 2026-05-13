import subprocess
import sys
import os

if __name__ == "__main__":
    print(">>> Bakırçay Akıllı Kütüphane Arayüzü Yükleniyor... 🦩")
    
    # main.py dosyasının bulunduğu tam klasör yolunu otomatik bul
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # gui_test.py'nin tam adresini oluştur
    gui_dosyasi = os.path.join(BASE_DIR, "gui_test.py")
    
    # Tam adresi vererek çalıştır, böylece terminal nerede olursa olsun dosyayı şıp diye bulur!
    subprocess.run([sys.executable, gui_dosyasi])