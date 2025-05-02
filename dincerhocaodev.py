import numpy  as np
# SymPy kütüphanesini ekle
import sympy as sp
# SciPy integral fonksiyonunu ekle
from scipy import integrate
# Uyarıları yönetmek için (isteğe bağlı)
import warnings

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

# --- İntegral Bölümü 1 ---
# SORU: integral 1'den 2 ye giderken e^(x+ln(x^2)).dx

print("\n--- Belirli İntegral Hesabı 1 ---")

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

# --- İntegral Bölümü 2 ---
# SORU: integral -1'den 2 ye giderken (4x^3 - 3x^2 + 2).dx

print("\n--- Belirli İntegral Hesabı 2 ---")

# --- Sembolik Çözüm (SymPy) ---
print(">>> Sembolik Çözüm (SymPy):")
# Sembolik değişken zaten tanımlı (x_sym)

# İntegrali alınacak yeni fonksiyonu tanımla
f_integral_2_sym = 4*x_sym**3 - 3*x_sym**2 + 2

# Belirli integrali hesapla (-1'den 2'ye)
integral_sonucu_2_sym = sp.integrate(f_integral_2_sym, (x_sym, -1, 2))

# Sonucu ve sayısal değerini yazdır
print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_2_sym}")
print(f"İntegral sınırlar: x = -1'den x = 2'ye")
# SymPy genellikle polinom integrallerini doğrudan sayısal olarak hesaplar
print(f"Belirli integralin sonucu (SymPy): {integral_sonucu_2_sym}")
print("-" * 15)

# --- Sayısal Çözüm (SciPy) ---
print(">>> Sayısal Çözüm (SciPy Quad):")

# İntegrali alınacak yeni fonksiyonu NumPy kullanarak tanımla
def f_integral_2_num(x):
    return 4*x**3 - 3*x**2 + 2

# SciPy quad fonksiyonu ile integrali hesapla
integral_sonucu_2_num, hata_tahmini_2 = integrate.quad(f_integral_2_num, -1, 2)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: 4*x**3 - 3*x**2 + 2")
print(f"İntegral sınırlar: x = -1'den x = 2'ye")
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_2_num}")
print(f"Tahmini sayısal hata: {hata_tahmini_2}")

print("-" * 30) # Ayırıcı

# --- İntegral Bölümü 3 ---
# SORU: integral 0'dan 1'e giderken (x^4 * e^-x).dx

print("\n--- Belirli İntegral Hesabı 3 ---")

# --- Sembolik Çözüm (SymPy) ---
print(">>> Sembolik Çözüm (SymPy):")
# Sembolik değişken zaten tanımlı (x_sym)

# İntegrali alınacak yeni fonksiyonu tanımla
f_integral_3_sym = x_sym**4 * sp.exp(-x_sym)

# Belirli integrali hesapla (0'dan 1'e) - Sınırlara dikkat!
integral_sonucu_3_sym = sp.integrate(f_integral_3_sym, (x_sym, 0, 1))

# Sonucu ve sayısal değerini yazdır
print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_3_sym}")
print(f"İntegral sınırlar: x = 0'den x = 1'e") # Sınırları belirt
print(f"Belirli integralin sembolik sonucu: {integral_sonucu_3_sym}")
print(f"Belirli integralin sembolik sonucunun sayısal değeri: {integral_sonucu_3_sym.evalf()}")
print("-" * 15)

# --- Sayısal Çözüm (SciPy) ---
print(">>> Sayısal Çözüm (SciPy Quad):")

# İntegrali alınacak yeni fonksiyonu NumPy kullanarak tanımla
def f_integral_3_num(x):
    return x**4 * np.exp(-x)

# SciPy quad fonksiyonu ile integrali hesapla (0'dan 1'e)
# quad(func, a, b) a'dan b'ye integrali hesaplar. a > b ise sonuç negatif olur.
integral_sonucu_3_num, hata_tahmini_3 = integrate.quad(f_integral_3_num, 0, 1)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: x**4 * np.exp(-x)")
print(f"İntegral sınırlar: x = 0'dan x = 1'e") # Sınırları belirt
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_3_num}")
print(f"Tahmini sayısal hata: {hata_tahmini_3}")

print("-" * 30) # Ayırıcı

# --- İntegral Bölümü 4 ---
# SORU: integral 0'dan 3'e giderken (1/(x^2 - 6x + 5)).dx
# DİKKAT: Paydada x=1 noktasında (integrasyon aralığında) tekillik var!

print("\n--- Belirli İntegral Hesabı 4 (Tekillik İçeren) ---")

# --- Sembolik Çözüm (SymPy) ---
print(">>> Sembolik Çözüm (SymPy):")
# Sembolik değişken zaten tanımlı (x_sym)

# İntegrali alınacak yeni fonksiyonu tanımla
f_integral_4_sym = 1 / (x_sym**2 - 6*x_sym + 5)

# Belirli integrali hesapla (0'dan 3'e)
# SymPy, tekillik durumunda Cauchy esas değerini hesaplamaya çalışabilir
try:
    integral_sonucu_4_sym = sp.integrate(f_integral_4_sym, (x_sym, 0, 3))
    print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_4_sym}")
    print(f"İntegral sınırlar: x = 0'dan x = 3'e")
    print(f"Belirli integralin sembolik sonucu (Esas Değer?): {integral_sonucu_4_sym}")
    # Sonuç sonsuz veya tanımsız olabilir (zoo, nan, oo)
    if integral_sonucu_4_sym.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
         print("Uyarı: Sembolik integral sonucu sonsuz veya tanımsız.")
    else:
         print(f"Belirli integralin sembolik sonucunun sayısal değeri: {integral_sonucu_4_sym.evalf()}")
except Exception as e:
    print(f"SymPy ile sembolik integral hesaplanırken hata oluştu: {e}")
print("-" * 15)

# --- Sayısal Çözüm (SciPy) ---
print(">>> Sayısal Çözüm (SciPy Quad):")

# İntegrali alınacak yeni fonksiyonu NumPy kullanarak tanımla
def f_integral_4_num(x):
    # Sıfıra bölme hatasını önlemek için küçük bir kontrol (isteğe bağlı)
    # if np.isclose(x, 1.0) or np.isclose(x, 5.0):
    #     return np.inf # Veya başka bir uygun değer
    return 1 / (x**2 - 6*x + 5)

# SciPy quad fonksiyonu ile integrali hesapla (0'dan 3'e)
# Tekillik nedeniyle uyarı verebilir (IntegrationWarning)
print("Not: İntegrasyon aralığında (x=1) tekillik olduğundan SciPy uyarı verebilir.")
# Uyarıları geçici olarak bastırmak için (isteğe bağlı):
# with warnings.catch_warnings():
#     warnings.filterwarnings('error', category=integrate.IntegrationWarning)
try:
    integral_sonucu_4_num, hata_tahmini_4 = integrate.quad(f_integral_4_num, 0, 3) # points=[1] argümanı denenebilir
    print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: 1 / (x**2 - 6*x + 5)")
    print(f"İntegral sınırlar: x = 0'dan x = 3'e")
    print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_4_num}")
    print(f"Tahmini sayısal hata: {hata_tahmini_4}")
except integrate.IntegrationWarning as w:
     print(f"Sayısal integral hesaplanırken uyarı alındı: {w}")
     print("Sonuç, Cauchy Esas Değeri olabilir veya yakınsama başarısız olmuş olabilir.")
except Exception as e:
     print(f"Sayısal integral hesaplanırken hata oluştu: {e}")


print("-" * 30) # Ayırıcı
