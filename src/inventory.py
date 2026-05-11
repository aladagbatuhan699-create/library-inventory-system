class kitap:
    def __init__(self, ad, yazar, isbn):
        self.ad = ad
        self.yazar = yazar
        self.isbn = isbn

    def __str__(self):
            return f"{self.ad} by {self.yazar} (ISBN: {self.isbn})"

def kitap_ekle(inventory, kitap):
    inventory.append(kitap)

def kitap_sil(inventory, isbn):
    for kitap in inventory:
        if kitap.isbn == isbn: 
            inventory.remove(kitap)
            break
envanter = [
      kitap("sefiller", "Yazar 1", "1234567890"),
      kitap("Kitap 2", "Yazar 2", "0987654321"),
      kitap("Kitap 3", "Yazar 3", "1122334455")
      ]
def kitaplari_goster(envanter):
    print("Mevcut Kitaplar:") 
    for kitap in envanter:
        print(kitap)  