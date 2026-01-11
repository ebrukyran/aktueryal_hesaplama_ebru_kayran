import pandas as pd
import numpy as np


class AktueryalHesaplayici:
    """
    Kullanıcının verdiği mortalite tablosu ile
    hayat sigortası prim hesapları yapar.
    """

    def __init__(self, faiz_orani, qx_tablosu=None):
        if faiz_orani <= 0:
            raise ValueError("Faiz oranı pozitif olmalıdır.")

        self.faiz = faiz_orani
        self.iskonto = 1 / (1 + faiz_orani)

        # Eğer kullanıcı tablo vermezse varsayılan tablo kullanılır
        if qx_tablosu is None:
            self.qx = self.varsayilan_qx()
        else:
            self.qx = np.array(qx_tablosu, dtype=float)

        # Son yaşta ölüm olasılığı 1 değilse zorla 1 yapılır
        if self.qx[-1] != 1:
            print("Uyarı: Son yaş için qx = 1 değil. Son yaşta ölüm olasılığı 1 kabul edildi.")
            self.qx[-1] = 1

        self.komutasyon = self.komutasyon_tablosu_olustur()

    def varsayilan_qx(self):
        """Varsayılan: 1980 CSO Male mortalite tablosu"""
        return np.array([
            0.00263, 0.00103, 0.00099, 0.00096, 0.00093, 0.00090, 0.00088, 0.00086, 0.00084, 0.00082,
            0.00081, 0.00082, 0.00085, 0.00091, 0.00101, 0.00114, 0.00129, 0.00144, 0.00159, 0.00173,
            0.00186, 0.00196, 0.00203, 0.00207, 0.00208, 0.00207, 0.00204, 0.00200, 0.00196, 0.00193,
            0.00191, 0.00193, 0.00198, 0.00207, 0.00221, 0.00240, 0.00264, 0.00293, 0.00327, 0.00366,
            0.00411, 0.00461, 0.00516, 0.00576, 0.00641, 0.00711, 0.00787, 0.00869, 0.00958, 0.01054,
            0.01158, 0.01271, 0.01394, 0.01529, 0.01676, 0.01838, 0.02016, 0.02212, 0.02427, 0.02664,
            0.02925, 0.03211, 0.03525, 0.03869, 0.04246, 0.04658, 0.05108, 0.05599, 0.06134, 0.06716,
            0.07348, 0.08035, 0.08781, 0.09591, 0.10471, 0.11425, 0.12458, 0.13576, 0.14785, 0.16091,
            0.17500, 0.19018, 0.20651, 0.22405, 0.24287, 0.26301, 0.28453, 0.30748, 0.33189, 0.35780,
            0.38523, 0.41419, 0.44467, 0.47665, 0.50998, 0.54443, 0.57959, 0.61482, 0.64916, 1.00000
        ])

    def komutasyon_tablosu_olustur(self):
        yas_sayisi = len(self.qx)
        yaslar = np.arange(yas_sayisi)

        lx = np.zeros(yas_sayisi)
        dx = np.zeros(yas_sayisi)

        lx[0] = 1000000  

        for x in range(yas_sayisi):
            dx[x] = lx[x] * self.qx[x]
            if x < yas_sayisi - 1:
                lx[x + 1] = lx[x] - dx[x]

        Dx = lx * (self.iskonto ** yaslar)
        Cx = dx * (self.iskonto ** (yaslar + 1))

        Nx = np.flip(np.cumsum(np.flip(Dx)))
        Mx = np.flip(np.cumsum(np.flip(Cx)))

        tablo = pd.DataFrame({
            "yas": yaslar,
            "lx": lx,
            "dx": dx,
            "Dx": Dx,
            "Cx": Cx,
            "Nx": Nx,
            "Mx": Mx
        })

        tablo = tablo.set_index("yas")
        return tablo

    def yas_kontrol(self, yas):
        if yas < 0 or yas >= len(self.qx):
            raise ValueError("Yaş, tablo aralığında olmalıdır.")

    # 1) Hayat Boyu (Whole Life) Vefat Sigortası
    def hayat_boyu_vefat(self, yas, teminat):
        """A_x = M_x / D_x"""
        self.yas_kontrol(yas)
        Mx = self.komutasyon.at[yas, "Mx"]
        Dx = self.komutasyon.at[yas, "Dx"]
        return (Mx / Dx) * teminat

    # 2) Dönemsel (Term) Vefat Sigortası
    def donemsel_vefat(self, yas, teminat, sure):
        """A_{x:n} = (M_x - M_{x+n}) / D_x"""
        self.yas_kontrol(yas)
        bitis_yasi = min(yas + sure, len(self.qx) - 1)

        Mx = self.komutasyon.at[yas, "Mx"]
        M_xn = self.komutasyon.at[bitis_yasi, "Mx"]
        Dx = self.komutasyon.at[yas, "Dx"]

        return ((Mx - M_xn) / Dx) * teminat

    # 3) Ertelenmiş (Deferred) Hayat Boyu Vefat Sigortası
    def ertelenmis_hayat_boyu(self, yas, teminat, erteleme):
        """n|A_x = M_{x+n} / D_x"""
        self.yas_kontrol(yas)
        baslangic = min(yas + erteleme, len(self.qx) - 1)

        M_xn = self.komutasyon.at[baslangic, "Mx"]
        Dx = self.komutasyon.at[yas, "Dx"]

        return (M_xn / Dx) * teminat

    # 4) Ertelenmiş + Dönemsel (Birlikte) (Deferred Term) Sigorta
    def ertelenmis_donemsel_vefat(self, yas, teminat, erteleme, sure):
        """
        n yıl ertelenmiş m yıllık dönemsel vefat sigortası
        Formül: n|A_{x:m} = (M_{x+n} - M_{x+n+m}) / D_x
        """
        self.yas_kontrol(yas)

        baslangic_yasi = min(yas + erteleme, len(self.qx) - 1)
        bitis_yasi = min(yas + erteleme + sure, len(self.qx) - 1)

        M_xn = self.komutasyon.at[baslangic_yasi, "Mx"]
        M_xn_m = self.komutasyon.at[bitis_yasi, "Mx"]
        Dx = self.komutasyon.at[yas, "Dx"]

        return ((M_xn - M_xn_m) / Dx) * teminat

    def excel_kaydet(self, dosya_adi):
        self.komutasyon.to_excel(dosya_adi)
        print("Komütasyon tablosu Excel dosyasına kaydedildi.")