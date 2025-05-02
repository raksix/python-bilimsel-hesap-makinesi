import numpy  as np
# SymPy kütüphanesini ekle
import sympy as sp
# SciPy integral fonksiyonunu ekle
from scipy import integrate

# --- Newton-Raphson Bölümü ---
# SORU e üssü x - 3x denklemini [0,1] aralığındaki kökünü Newton- Raphson yöntemi ile bulan python programını 3 adımda yazınız.

def f(x):
   # Denklemi düzelt: e^x - 3x
   return np.exp(x) - 3 * x

def df(x):
   # Türevi düzelt: e^x - 3
   return np.exp(x) - 3

# Fonksiyonu 3 adımda çalışacak şekilde ayarla (max_iter=3) ve toleransı kaldır veya çok küçük yap
def newton_raphson(f, df, x0, max_iter=3): # df fonksiyonunu parametre olarak ekle
    print(f"Başlangıç değeri: x0 = {x0}")
    xn = x0
    for i in range(1, max_iter + 1):
        fxn = f(xn)
        dfxn = df(xn)
        print(f"Adım {i} öncesi: x = {xn}, f(x) = {fxn}, df(x) = {dfxn}")
        if dfxn == 0:
            print("Türev sıfır, Yöntem durduruldu.")
            return None
        xn_plus_1 = xn - fxn / dfxn
        print(f"Adım {i} sonrası: x = {xn_plus_1}")
        xn = xn_plus_1 # Update xn for the next iteration

    print(f"\n3 adım sonunda bulunan değer: x ≈ {xn}")
    print(f"Bu noktadaki fonksiyon değeri: f(x) ≈ {f(xn)}")
    return xn

# Başlangıç noktası seçimi (örneğin aralığın ortası)
x_baslangic = 0.5

# Newton-Raphson fonksiyonunu çağır
print("--- Newton-Raphson Yöntemi ---")
kok_yaklasimi = newton_raphson(f, df, x_baslangic, max_iter=3)
print("-" * 30) # Ayırıcı

# --- İntegral Bölümü ---
# SORU: integral 1'den 2 ye giderken e^(x+ln(x^2)).dx

print("\n--- Belirli İntegral Hesabı ---")

# --- Sembolik Çözüm (SymPy) ---
print(">>> Sembolik Çözüm (SymPy):")
# Sembolik değişkeni tanımla
x_sym = sp.symbols('x') # NumPy'ın x'i ile karışmaması için farklı isim

# İntegrali alınacak fonksiyonu tanımla ve basitleştir
f_integral_sym = x_sym**2 * sp.exp(x_sym)

# Belirli integrali hesapla (1'den 2'ye)
integral_sonucu_sym = sp.integrate(f_integral_sym, (x_sym, 1, 2))

# Sonucu ve sayısal değerini yazdır
print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_sym}")
print(f"İntegral sınırlar: x = 1'den x = 2'ye")
print(f"Belirli integralin sembolik sonucu: {integral_sonucu_sym}")
print(f"Belirli integralin sembolik sonucunun sayısal değeri: {integral_sonucu_sym.evalf()}")
print("-" * 15)

# --- Sayısal Çözüm (SciPy) ---
print(">>> Sayısal Çözüm (SciPy Quad):")

# İntegrali alınacak fonksiyonu NumPy kullanarak tanımla (sayısal hesaplama için)
def f_integral_num(x):
    return x**2 * np.exp(x)

# SciPy quad fonksiyonu ile integrali hesapla
# quad fonksiyonu (fonksiyon, alt_sınır, üst_sınır) parametrelerini alır
# Geriye (integral_değeri, tahmini_hata) şeklinde bir tuple döndürür
integral_sonucu_num, hata_tahmini = integrate.quad(f_integral_num, 1, 2)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: x**2 * np.exp(x)")
print(f"İntegral sınırlar: x = 1'den x = 2'ye")
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_num}")
print(f"Tahmini sayısal hata: {hata_tahmini}")

print("-" * 30) # Ayırıcı
