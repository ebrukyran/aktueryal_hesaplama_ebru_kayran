
"""
AktueryalHesaplayici sınıfı için örnek kullanım dosyası.
Bu dosya, kütüphanenin nasıl kullanılacağını göstermektedir.
"""

from src.aktueryal_hesaplayici import AktueryalHesaplayici


def main():
    print("=== AKTÜERYAL HAYAT SİGORTASI HESAPLAMA ===")

    # Kullanıcıdan girdiler
    faiz_orani = float(input("Teknik faiz oranını giriniz (örn: 0.05): "))
    yas = int(input("Sigortalının yaşı: "))
    teminat = float(input("Sigorta teminat tutarı (örn: 100000): "))

    erteleme = int(input("Ertelenmiş sigorta için erteleme süresi (yıl): "))
    sure = int(input("Dönemsel sigorta için süre (yıl): "))

    # Hesaplayıcı oluştur
    hesaplayici = AktueryalHesaplayici(faiz_orani)

    print("\n--- HESAPLAMA SONUÇLARI ---")

    # 1) Hayat Boyu Vefat Sigortası
    prim_hayat_boyu = hesaplayici.hayat_boyu_vefat(yas, teminat)
    print(f"Hayat Boyu Vefat Sigortası Tek Prim: {prim_hayat_boyu:,.2f} TL")

    # 2) Dönemsel Vefat Sigortası
    prim_donemsel = hesaplayici.donemsel_vefat(yas, teminat, sure)
    print(f"{sure} Yıllık Dönemsel Vefat Sigortası Tek Prim: {prim_donemsel:,.2f} TL")

    # 3) Ertelenmiş Hayat Boyu Vefat Sigortası
    prim_ertelenmis = hesaplayici.ertelenmis_hayat_boyu(yas, teminat, erteleme)
    print(f"{erteleme} Yıl Ertelenmiş Hayat Boyu Vefat Sigortası Tek Prim: {prim_ertelenmis:,.2f} TL")

    # 4) Ertelenmiş + Dönemsel (Birlikte) Vefat Sigortası
    prim_ertelenmis_donemsel = hesaplayici.ertelenmis_donemsel_vefat(
        yas, teminat, erteleme, sure
    )
    print(f"{erteleme} Yıl Ertelenmiş + {sure} Yıllık Dönemsel Vefat Sigortası Tek Prim: "
          f"{prim_ertelenmis_donemsel:,.2f} TL")

    # Excel çıktısı
    kaydet = input("\nKomütasyon tablosunu Excel olarak kaydetmek ister misiniz? (e/h): ")
    if kaydet.lower() == "e":
        dosya_adi = input("Dosya adı giriniz (örn: komutasyon_tablosu.xlsx): ")
        hesaplayici.excel_kaydet(dosya_adi)


if __name__ == "__main__":
    main()
