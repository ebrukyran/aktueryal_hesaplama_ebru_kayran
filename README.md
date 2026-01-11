# Aktüeryal Hayat Sigortası Hesaplayıcı

## Proje Geliştiricisi

Ad Soyad: **[EBRU KAYRAN]**
Ders: **Aktüerya Bilimleri**

## Projenin Amacı ve Kapsamı

Bu proje, kullanıcı tarafından verilen bir **mortalite tablosu (qx)** ve **faiz oranı** kullanarak temel aktüeryal hayat sigortası hesaplamalarını Python ile yapmayı amaçlar.
Kod yapısı sade tutulmuş, fonksiyon isimleri **Türkçe** olarak yazılmıştır.

Projede aşağıdaki ürünlerin bugünkü değerleri hesaplanabilmektedir:

* Hayat boyu (Whole Life) vefat sigortası
* Dönemsel (Term) vefat sigortası
* Ertelenmiş (Deferred) hayat boyu vefat sigortası
* Ertelenmiş + dönemsel (birlikte) (Deferred Term) vefat sigortası

Ayrıca kullanıcı kendi mortalite tablosunu sisteme ekleyebilir ve hesaplamaları bu tabloya göre yaptırabilir.
Eğer kullanıcı bir tablo girmezse, sistem otomatik olarak 1980 CSO (Male) tablosunu kullanır.

---

## Kurulum / Çalıştırma

Bu proje herhangi bir özel paket gerektirmez. Sadece aşağıdaki kütüphaneler kullanılmaktadır:

```bash
pip install numpy pandas
```

Dosya yapısı örneği:

```
proje_klasoru/
│
├── src/
│   └── aktüeryal_hesaplayici.py
├── examples/
│   └── ornek_kullanim.py
└── README.md
```

`src` klasörü ana hesaplama kodlarını, `examples` klasörü ise kullanım örneklerini içerir.

---

## Örnek Kullanım

Aşağıdaki örnek, 5% faiz oranı ile 30 yaşındaki bir kişi için 100.000 TL teminatlı sigorta değerlerinin nasıl hesaplandığını göstermektedir.

```python
from src.aktüeryal_hesaplayici import AktueryalHesaplayici

# Hesaplayıcı oluştur
hesaplayici = AktueryalHesaplayici(faiz_orani=0.05)

# Hayat boyu vefat sigortası
prim1 = hesaplayici.hayat_boyu_vefat(yas=30, teminat=100000)
print("Hayat Boyu Vefat Sigortası:", prim1)

# 10 yıllık dönemsel vefat sigortası
prim2 = hesaplayici.donemsel_vefat(yas=30, teminat=100000, sure=10)
print("Dönemsel Vefat Sigortası:", prim2)

# 5 yıl ertelenmiş hayat boyu vefat sigortası
prim3 = hesaplayici.ertelenmis_hayat_boyu(yas=30, teminat=100000, erteleme=5)
print("Ertelenmiş Hayat Boyu Vefat Sigortası:", prim3)

# 5 yıl ertelenmiş, 10 yıl süreli vefat sigortası
prim4 = hesaplayici.ertelenmis_donemsel_vefat(yas=30, teminat=100000, erteleme=5, sure=10)
print("Ertelenmiş + Dönemsel Vefat Sigortası:", prim4)
```

---

## Kullanıcı Tarafından Mortalitenin Girilmesi

Kullanıcı, kendi mortalite tablosunu (qx değerleri) aşağıdaki şekilde ekleyebilir:

```python
kendi_qx = [0.001, 0.0011, 0.0012, 0.0013, ..., 1.0]

hesaplayici = AktueryalHesaplayici(faiz_orani=0.05, qx_tablosu=kendi_qx)
```

Eğer son yaş için qx değeri 1 değilse, program otomatik olarak son değeri 1 kabul eder ve kullanıcıyı uyarır.

---

## Fonksiyonlar ve Açıklamaları

### 1) `hayat_boyu_vefat(yas, teminat)`

Hayat boyu vefat sigortasının bugünkü değerini hesaplar.
Formül:
Aₓ = Mₓ / Dₓ

---

### 2) `donemsel_vefat(yas, teminat, sure)`

Belirli süre (n yıl) için dönemsel vefat sigortasının bugünkü değerini hesaplar.
Formül:
Aₓ:n = (Mₓ − Mₓ₊ₙ) / Dₓ

---

### 3) `ertelenmis_hayat_boyu(yas, teminat, erteleme)`

Belirli bir süre ertelenmiş hayat boyu vefat sigortasını hesaplar.
Formül:
n|Aₓ = Mₓ₊ₙ / Dₓ

---

### 4) `ertelenmis_donemsel_vefat(yas, teminat, erteleme, sure)`

Hem ertelenmiş hem de dönemsel olan (birlikte) vefat sigortasını hesaplar.
Formül:
n|Aₓ:m = (Mₓ₊ₙ − Mₓ₊ₙ₊ₘ) / Dₓ

---

## Ek Özellik: Excel Çıktısı

Komütasyon tablosu aşağıdaki fonksiyon ile Excel dosyası olarak kaydedilebilir:

```python
hesaplayici.excel_kaydet("komutasyon_tablosu.xlsx")
```

Bu dosya içinde yaş, lx, dx, Dx, Cx, Nx ve Mx sütunları yer alır.

---

## Not

Bu proje, ders kapsamında öğrenilen aktüeryal hesaplama yöntemlerini uygulamak amacıyla hazırlanmıştır. Eğitim amaçlıdır ve ticari kullanım için tasarlanmamıştır.