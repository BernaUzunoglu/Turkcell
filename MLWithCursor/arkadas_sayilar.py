def bolenler_toplami(sayi):
    toplam = 0
    for i in range(1, sayi):
        if sayi % i == 0:
            toplam += i
    return toplam

def arkadas_sayi_mi(sayi1, sayi2):
    if bolenler_toplami(sayi1) == sayi2 and bolenler_toplami(sayi2) == sayi1:
        return True
    return False

# Kullanıcıdan iki sayı al
sayi1 = int(input("Birinci sayıyı girin: "))
sayi2 = int(input("İkinci sayıyı girin: "))

# Arkadaş sayı kontrolü
if arkadas_sayi_mi(sayi1, sayi2):
    print(f"{sayi1} ve {sayi2} arkadaş sayılardır!")
else:
    print(f"{sayi1} ve {sayi2} arkadaş sayılar değildir.") 