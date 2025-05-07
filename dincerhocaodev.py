# Furkan Ermağ BM 1 Matematik İntegral Ödevi


import numpy  as np
import sympy as sp
from scipy import integrate
import warnings

def f(x):
   return np.exp(x) - 3 * x

def df(x):
   return np.exp(x) - 3

def newton_raphson(f, df, x0, max_iter=3):
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
        xn = xn_plus_1

    print(f"\n3 adım sonunda bulunan değer: x ≈ {xn}")
    print(f"Bu noktadaki fonksiyon değeri: f(x) ≈ {f(xn)}")
    return xn

x_baslangic = 0.5

print("--- Newton-Raphson Yöntemi ---")
kok_yaklasimi = newton_raphson(f, df, x_baslangic, max_iter=3)
print("-" * 30)


## 1. Soru
print("\n--- Belirli İntegral Hesabı 1 ---")

print(">>> Sembolik Çözüm (SymPy):")
x_sym = sp.symbols('x')

f_integral_sym = x_sym**2 * sp.exp(x_sym)
# x ^ 2 * e^x

integral_sonucu_sym = sp.integrate(f_integral_sym, (x_sym, 1, 2))

print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_sym}")
print(f"İntegral sınırlar: x = 1'den x = 2'ye")
print(f"Belirli integralin sembolik sonucu: {integral_sonucu_sym}")
print(f"Belirli integralin sembolik sonucunun sayısal değeri: {integral_sonucu_sym.evalf()}")
print("-" * 15)

print(">>> Sayısal Çözüm (SciPy Quad):")

def f_integral_num(x):
    return x**2 * np.exp(x)
    # x ^ 2 * e^x

integral_sonucu_num, hata_tahmini = integrate.quad(f_integral_num, 1, 2)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: x**2 * np.exp(x)")
print(f"İntegral sınırlar: x = 1'den x = 2'ye")
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_num}")
print(f"Tahmini sayısal hata: {hata_tahmini}")

print("-" * 30)

print("\n--- Belirli İntegral Hesabı 2 ---")

print(">>> Sembolik Çözüm (SymPy):")

f_integral_2_sym = 4*x_sym**3 - 3*x_sym**2 + 2
# 4 * x^3 - 3 * x^2 + 2

integral_sonucu_2_sym = sp.integrate(f_integral_2_sym, (x_sym, -1, 2))

print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_2_sym}")
print(f"İntegral sınırlar: x = -1'den x = 2'ye")
print(f"Belirli integralin sonucu (SymPy): {integral_sonucu_2_sym}")
print("-" * 15)

print(">>> Sayısal Çözüm (SciPy Quad):")

def f_integral_2_num(x):
    return 4*x**3 - 3*x**2 + 2
    # 4 * x^3 - 3 * x^2 + 2

integral_sonucu_2_num, hata_tahmini_2 = integrate.quad(f_integral_2_num, -1, 2)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: 4*x**3 - 3*x**2 + 2")
print(f"İntegral sınırlar: x = -1'den x = 2'ye")
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_2_num}")
print(f"Tahmini sayısal hata: {hata_tahmini_2}")

print("-" * 30)

print("\n--- Belirli İntegral Hesabı 3 ---")

print(">>> Sembolik Çözüm (SymPy):")

f_integral_3_sym = x_sym**4 * sp.exp(-x_sym)
# x^4 * e^(-x)

integral_sonucu_3_sym = sp.integrate(f_integral_3_sym, (x_sym, 0, 1))

print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_3_sym}")
print(f"İntegral sınırlar: x = 0'dan x = 1'e")
print(f"Belirli integralin sembolik sonucu: {integral_sonucu_3_sym}")
print(f"Belirli integralin sembolik sonucunun sayısal değeri: {integral_sonucu_3_sym.evalf()}")
print("-" * 15)

print(">>> Sayısal Çözüm (SciPy Quad):")

def f_integral_3_num(x):
    return x**4 * np.exp(-x)
    # x^4 * e^(-x)

integral_sonucu_3_num, hata_tahmini_3 = integrate.quad(f_integral_3_num, 0, 1)

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: x**4 * np.exp(-x)")
print(f"İntegral sınırlar: x = 0'dan x = 1'e")
print(f"Belirli integralin sayısal sonucu (quad): {integral_sonucu_3_num}")
print(f"Tahmini sayısal hata: {hata_tahmini_3}")

print("-" * 30)

print("\n--- Belirli İntegral Hesabı 4 ---")

print(">>> Sembolik Çözüm (SymPy):")

f_integral_4_sym = 1 / (x_sym**2 - 6*x_sym + 5)
# 1 / (x^2 - 6 * x + 5)

integral_sonucu_4_sym = sp.integrate(f_integral_4_sym, (x_sym, 0, 3))

print(f"İntegrali alınacak fonksiyon (sembolik): {f_integral_4_sym}")
print(f"İntegral sınırlar: x = 0'dan x = 3'e")
print(f"Belirli integralin sembolik sonucu: {integral_sonucu_4_sym}")

try:
    numerical_result = integral_sonucu_4_sym.evalf()
    print(f"Sembolik integralin sayısal yaklaşık sonucu: {numerical_result}")
except Exception as e:
    print(f"Sayısal hesaplama başarısız (tekillik nedeniyle?): {e}")

integral_part1 = sp.integrate(f_integral_4_sym, (x_sym, 0, 1 - sp.Rational(1, 100)))
integral_part2 = sp.integrate(f_integral_4_sym, (x_sym, 1 + sp.Rational(1, 100), 3))
total_manual = integral_part1 + integral_part2
print(f"Manuel bölünmüş integralin yaklaşık sembolik sonucu: {total_manual}") # Elle 4'e bölünmesi gerekiyor
print(f"Manuel bölünmüş integralin sayısal yaklaşık sonucu: {total_manual.evalf()}")

print("-" * 15)

print(">>> Sayısal Çözüm (SciPy Quad):")

def f_integral_4_num(x):
    return 1 / (x**2 - 6*x + 5)
    # 1 / (x^2 - 6 * x + 5)

print("Not: İntegrasyon aralığında (x=1) tekillik olduğundan SciPy uyarı verebilir.")

# Uyarıyı gizlemek için warnings modülünü kullandum
warnings.filterwarnings("ignore", category=integrate.IntegrationWarning)

# Artık uyarı göstermeyecek
integral_sonucu_4_num, hata_tahmini_4 = integrate.quad(f_integral_4_num, 0, 3, points=[1])

print(f"İntegrali alınacak fonksiyon (sayısal): lambda x: 1 / (x**2 - 6*x + 5)")
print(f"Tahmini sayısal hata: {hata_tahmini_4}")
print(f"İntegral sınırlar: x = 0'dan x = 3'e")
print(f"Belirli integralin sayısal sonucu (quad, points=[1] ile): {integral_sonucu_4_num}")

print("-" * 30)






