Elbette, Casio FX-99ICW benzeri bir bilimsel hesap makinesi uygulaması için adım adım bir Ürün Gereksinimleri Dokümanı (PRD) taslağı aşağıdadır:

**Ürün Gereksinimleri Dokümanı (PRD): Python Bilimsel Hesap Makinesi (Casio FX-99ICW Benzeri)**

**1. Giriş**

*   **Amaç:** Python'da `customtkinter` kütüphanesini kullanarak, Casio FX-99ICW bilimsel hesap makinesinin arayüzünü ve temel işlevselliğini taklit eden bir masaüstü bilimsel hesap makinesi uygulaması geliştirmek.
*   **Kapsam:** Uygulama, temel aritmetik işlemlerden trigonometrik, logaritmik, üstel fonksiyonlara, değişken depolamaya ve `sympy` ile `numpy` kullanarak daha gelişmiş matematiksel işlemlere (türev, integral, matris) kadar geniş bir yelpazede işlevsellik sunacaktır.

**2. Gereksinimler**

*   **2.1. Fonksiyonel Gereksinimler:**
    *   **2.1.1. Kullanıcı Arayüzü (GUI):**
        *   `customtkinter` kullanılarak modern ve Casio FX-99ICW düzenine benzer bir arayüz oluşturulacak.
        *   Çok satırlı, monokrom stilinde bir ekran alanı bulunacak.
        *   Ekranın üst kısmında mod göstergeleri (Spreadsheet, Table, XY=0 Equation, Inequality, Complex, Base-N) yer alacak (başlangıçta statik ikonlar veya metinler olabilir).
        *   Tüm Casio FX-99ICW tuşları (aşağıda listelenmiştir) arayüzde buton olarak yer alacak.
    *   **2.1.2. Tuş Takımı ve İşlevler:**
        *   **Rakamlar:** 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, . (ondalık nokta)
        *   **Temel Operatörler:** +, -, ×, ÷, =
        *   **Matematiksel Fonksiyonlar:** QR (Karekök), √ (Karekök), x² (Kare), log (10 tabanında logaritma), ln (Doğal logaritma), sin, cos, tan, Ans (Son cevap), (, ), x10^ (10 üzeri), π (Pi sabiti), e (Euler sabiti)
        *   **Mod ve Navigasyon:** on (Açma/Kapama - Uygulama başlatma/kapatma simülasyonu), HOME, SETTINGS (Ayarlar menüsü - başlangıçta derece/radyan geçişi), Yukarı/Aşağı/Sol/Sağ Ok Tuşları (Giriş/geçmişte gezinme), OK (Onay)
        *   **Fonksiyon Tuşları:** SHIFT (İkincil fonksiyonları etkinleştirme), VARIABLE (Değişken menüsü), FUNCTION (Fonksiyon menüsü), CATALOG (Fonksiyon kataloğu), TOOLS (Araçlar menüsü)
        *   **Değişken Tuşları:** A, B, C, D, E, F (Değer atama ve kullanma)
        *   **Özel Tuşlar:** FORMAT (Sayı formatı), EXE (Hesapla/Eşittir), = (Hesapla/Eşittir - EXE ile aynı işlev), INS (İnsert/Ekleme modu), AC (All Clear/Tümünü Temizle), (-) (Negatif işareti)
    *   **2.1.3. Hesaplama Motoru:**
        *   Standart matematiksel işlem önceliğini (PEMDAS/BODMAS) doğru bir şekilde uygulayacak.
        *   Girilen ifadeleri ayrıştırıp (parsing) değerlendirecek (evaluation).
        *   '=' veya 'EXE' tuşuna basıldığında hesaplama yapılacak.
        *   Trigonometrik fonksiyonlar için Derece ve Radyan modları arasında geçiş yapılabilecek ve hesaplamalar seçili moda göre yapılacak.
        *   Logaritmik (log, ln) ve üstel (x10^) fonksiyonları destekleyecek.
        *   `sympy` kütüphanesi kullanılarak sembolik türev ve integral hesaplamaları yapılacak (örneğin, `diff(x**2, x)`, `integrate(x, x)`).
        *   `sympy` kütüphanesi kullanılarak denklem çözme (`solve(x**2 - 4, x)`) yapılacak.
        *   `numpy` kütüphanesi kullanılarak temel matris işlemleri (toplama, çıkarma, çarpma - eğer matris modu eklenirse) yapılacak.
    *   **2.1.4. Değişken Yönetimi:**
        *   Kullanıcıların hesaplama sonuçlarını veya girdikleri değerleri A, B, C, D, E, F değişkenlerine atamasına izin verilecek.
        *   Ans değişkeni, son hesaplama sonucunu otomatik olarak saklayacak.
        *   Bu değişkenler sonraki hesaplamalarda kullanılabilecek.
    *   **2.1.5. Hata Yönetimi:**
        *   Geçersiz matematiksel ifadeler (örn: "2++3", "sin()"), sıfıra bölme gibi durumlar için anlaşılır hata mesajları gösterilecek.
        *   Giriş hataları (örn: tanımsız fonksiyon) kullanıcıya bildirilecek.
*   **2.2. Teknik Gereksinimler:**
    *   **Programlama Dili:** Python (önerilen sürüm 3.8+)
    *   **GUI Kütüphanesi:** `customtkinter`
    *   **Matematik Kütüphaneleri:** `math` (temel fonksiyonlar için), `sympy` (sembolik matematik için), `numpy` (matris işlemleri için)
    *   **Platform:** Çapraz platform (Windows, macOS, Linux üzerinde çalışabilmeli)
*   **2.3. Diğer Gereksinimler:**
    *   **Kod Yapısı:** Kod, okunabilirlik ve bakım kolaylığı için modüler olacak (örn: `gui.py`, `calculator.py`, `variables.py`). Her modül ve önemli fonksiyonlar için açıklayıcı yorumlar eklenecek.
    *   **Taklit:** Arayüz düzeni ve temel etkileşim akışı Casio FX-99ICW modelini olabildiğince yakından takip edecek.

**3. Uygulama Adımları (Yüksek Seviye)**

1.  **Proje Kurulumu:** Gerekli kütüphanelerin (`customtkinter`, `sympy`, `numpy`) kurulumu ve proje dosya yapısının oluşturulması.
2.  **GUI Tasarımı:** `customtkinter` kullanarak ana pencere, ekran alanı ve tüm tuşların (butonların) görsel olarak yerleştirilmesi. Casio FX-99ICW düzenine göre konumlandırma.
3.  **Ekran Uygulaması:** Çok satırlı girişi ve sonucu gösterecek metin alanı veya etiket widget'ının yapılandırılması. Mod ikonlarının eklenmesi.
4.  **Temel Tuş İşlevselliği:** Rakam, operatör, parantez, ondalık nokta tuşlarına basıldığında bunların ekrana yazdırılması.
5.  **Temizleme ve Silme:** AC (All Clear) ve DEL (Silme - ok tuşları ile birlikte) işlevlerinin eklenmesi.
6.  **Hesaplama Motoru (Temel):** '=' veya 'EXE' tuşuna basıldığında ekrandaki ifadenin alınması, `eval()` veya daha güvenli bir ayrıştırıcı/değerlendirici (örn: `sympy.sympify` ve `evalf`) kullanılarak sonucun hesaplanması ve ekranda gösterilmesi. İşlem önceliğinin sağlanması.
7.  **Gelişmiş Fonksiyonlar:** Karekök, kare, log, ln, sin, cos, tan, x10^, π, e gibi fonksiyonların tuşlara bağlanması ve hesaplama motoruna entegrasyonu.
8.  **Derece/Radyan Modu:** Ayarlar (SETTINGS) veya özel bir mod tuşu ile derece/radyan arasında geçiş yapma mekanizmasının eklenmesi ve trigonometrik hesaplamaların bu moda göre ayarlanması.
9.  **Değişken Yönetimi:** Ans değişkeninin otomatik güncellenmesi. A-F değişkenlerine değer atama (örn: SHIFT + STO + A) ve bu değişkenleri kullanma mekanizmasının uygulanması.
10. **SHIFT Tuşu İşlevselliği:** SHIFT tuşuna basıldığında butonların ikincil işlevlerinin (örn: sin -> asin) aktif hale gelmesi.
11. **SymPy Entegrasyonu:** Türev, integral, denklem çözme gibi fonksiyonlar için `sympy`'nin kullanılması. Girdinin `sympy` tarafından anlaşılabilecek formata dönüştürülmesi.
12. **NumPy Entegrasyonu (Opsiyonel/İleri Seviye):** Matris modu eklenirse, matris girişi ve temel `numpy` matris işlemleri için arayüz ve hesaplama mantığının eklenmesi.
13. **Hata Yönetimi:** Hesaplama ve giriş sırasında oluşabilecek hataların yakalanması (`try-except` blokları) ve kullanıcıya bilgi verilmesi.
14. **İyileştirmeler:** Ok tuşları ile giriş ifadesinde gezinme, INS (insert) modu gibi ek özelliklerin implementasyonu. Arayüzün Casio modeline daha çok benzetilmesi.
15. **Kod Yapılandırma ve Yorumlama:** Kodun modüllere ayrılması ve açıklayıcı yorumlar eklenmesi.
16. **Test:** Belirtilen test senaryoları ('2 + 3 × 4', 'sin(30)' derece modunda, 'solve(x**2 - 4, x)') ve ek kapsamlı testlerin yapılması.

**4. Test Senaryoları (Örnekler)**

*   **Temel Aritmetik:** `2 + 3 * 4` -> Beklenen Sonuç: `14`
*   **Parantez Kullanımı:** `(2 + 3) * 4` -> Beklenen Sonuç: `20`
*   **Trigonometri (Derece Modu):** `sin(30)` -> Beklenen Sonuç: `0.5`
*   **Trigonometri (Radyan Modu):** `cos(pi)` -> Beklenen Sonuç: `-1`
*   **Logaritma:** `log(100)` -> Beklenen Sonuç: `2`
*   **Doğal Logaritma:** `ln(e)` -> Beklenen Sonuç: `1`
*   **Karekök:** `sqrt(9)` veya `√(9)` -> Beklenen Sonuç: `3`
*   **Üs Alma:** `2^3` (veya `2 x^y 3`) -> Beklenen Sonuç: `8`
*   **Değişken Kullanımı:** `5 -> A`, `A + 10` -> Beklenen Sonuç: `15`, `Ans` -> Beklenen Sonuç: `15`
*   **Denklem Çözme:** `solve(x**2 - 4, x)` -> Beklenen Sonuç: `[-2, 2]` (veya benzeri format)
*   **Türev:** `diff(x**3, x)` -> Beklenen Sonuç: `3*x**2` (veya benzeri format)
*   **Hata Durumu:** `5 / 0` -> Beklenen: Hata Mesajı (örn: "Sıfıra Bölme Hatası")
*   **Hata Durumu:** `log(-1)` -> Beklenen: Hata Mesajı (örn: "Matematik Alan Hatası")

**5. Gelecek Geliştirmeleri (Opsiyonel)**

*   Tam fonksiyonel modlar (Spreadsheet, Table, Complex, Base-N vb.).
*   Grafik çizim yetenekleri (`matplotlib` entegrasyonu).
*   Ayarların kalıcı olarak saklanması.
*   Kullanıcı tanımlı fonksiyonlar.
*   Daha gelişmiş matris işlemleri ve vektörler.

Bu PRD, geliştirme sürecine rehberlik etmek için bir başlangıç noktasıdır. Geliştirme sırasında detaylar netleşebilir ve gereksinimler güncellenebilir.