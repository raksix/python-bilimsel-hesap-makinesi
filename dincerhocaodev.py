import numpy  as np

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
kok_yaklasimi = newton_raphson(f, df, x_baslangic, max_iter=3)
