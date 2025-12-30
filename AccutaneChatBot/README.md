Bu proje, Accutane (Roaccutane) tedavisi hakkında merak edilenleri yanıtlamak üzere tasarlanmış, Hibrit Mimariye sahip akıllı bir sohbet botudur.

Uygulama, kullanıcı niyetini anlamak için Scikit-Learn (SVM), tıbbi sorulara kesin ve doğru cevaplar vermek için ise RAG (Retrieval-Augmented Generation) & Gemini teknolojilerini birleştirir.

Ornek Gorseller
![alt text](1_page-0001.jpg) ![alt text](3_page-0001.jpg) ![alt text](<Accutane AI Assistant_page-0001.jpg>) ![alt text](extra_page-0001.jpg)
🧠 Mimari ve Routing Mantığı (Kritik Bölüm) 🚦

Model,Görevi,Neden Seçildi?
Gemini 2.5 Flash,LLM (Cevap Üretici),"⚡ Hız ve Verimlilik: ""Flash"" serisi, düşük gecikme süresi (low latency) ile bilinir. Sohbet botlarında kullanıcının saniyelerce beklememesi kritiktir. Ayrıca uzun bağlam pencerelerini (context window) çok daha maliyet etkin yöneterek RAG süreçleri için ideal bir denge sunar."

text-embedding-004,Embedding (Vektörleştirme),🎯 Semantik Hassasiyet: Google'ın en yeni embedding modelidir. Eski versiyonlara (001) kıyasla metinlerin anlamsal ilişkilerini çok daha iyi kavrar. Tıbbi terimlerin ve kullanıcı sorularının eşleştirilmesinde (Retrieval) yüksek doğruluk sağlar.

Scikit-Learn SVC,Intent Classifier,"🛡️ Hafif ve Kararlı: Her soru için LLM çağırmak maliyetlidir. Basit metin sınıflandırma işlerinde klasik ML (SVM), derin öğrenmeye göre çok daha hızlı ve kaynak dostudur."
Bu asistanın en önemli özelliği, her soruyu doğrudan LLM'e (Büyük Dil Modeli) göndermemesidir. Akıllı bir Yönlendirme (Routing) mekanizması kullanır. Bu sayede hem maliyet düşer hem de yanıt hızı artar.

Karar Mekanizması Nasıl Çalışır?
Sistem, kullanıcının sorusunu önce Niyet Sınıflandırıcıya (Intent Classifier) sokar ve çıkan sonuca göre iki yoldan birini seçer:

1. Deterministik Yol (Hızlı Yanıt) ⚡
Eğer tahmin edilen niyet (intent) aşağıdakilerden biriyse, RAG (Belge Tarama) devre dışı bırakılır ve önceden tanımlı sabit yanıtlar döner:

greeting (Selamlaşma)

goodbye (Vedalaşma)

unrelated (Konu dışı / Alakasız sorular)

bot_identity_and_disclaimer (Bot kimliği ve yasal uyarı)

Neden? Bu sorular sosyal veya kapsam dışıdır. Modelin 40 sayfalık bir PDF'i taramasına gerek yoktur. Cevap kesindir.

2. RAG Yolu (Belge Tabanlı Yanıt) 📚
Eğer niyet tıbbi bir bilgi gerektiriyorsa (örn: dozaj, yan etkiler, hamilelik riskleri) veya model niyetten emin değilse (Confidence < %70):

Sistem accutane.pdf dosyasını tarar.

En alakalı parçaları bulur.

LLM'e (Gemini) şu talimatı verir: "Sadece bu metindeki bilgileri kullanarak cevap ver."

Neden? İlaç kullanımı ciddi bir konudur. Bu yöntem halüsinasyon (uydurma) riskini minimize eder ve cevabın kaynağa dayalı olmasını sağlar.


📊 Performans Metrikleri
Modelin başarısı hem sınıflandırma hem de cevap oluşturma kalitesi açısından test edilmiştir. İşte sonuçlar:

1. Niyet Sınıflandırma Başarısı (Intent Classifier) 🎯
Sınıflandırıcı, %78 genel doğruluk (accuracy) ile çalışmaktadır. Özellikle sosyal niyetlerde (selamlaşma vb.) başarı %100'e yakındır.

Sınıflandırma Raporu Özeti:

Intent (Niyet)	Precision	Recall	F1-Score
greeting (Selamlaşma)	1.00	0.95	0.97
goodbye (Vedalaşma)	1.00	0.80	0.89
unrelated (Alakasız)	0.89	0.93	0.91
bot_identity	0.86	0.95	0.90
Tıbbi Niyetler (Ortalama)	~0.70	~0.70	~0.70

![alt text](Figure_1.png) Confusion Matrix


Not: Tıbbi niyetlerin birbirine karışması (örn: yan etkiler vs. uyarılar) doğaldır, ancak sistem bu durumlarda her halükarda RAG'a gittiği için kullanıcı doğru cevabı almaya devam eder.

2. RAG Başarısı (RAGAS Değerlendirmesi) 🌟
RAG (Retrieval-Augmented Generation) hattının kalitesi, RAGAS framework'ü kullanılarak test edilmiştir. Sonuçlar modelin güvenilirliğini kanıtlamaktadır:

Faithfulness (Sadakat): 1.00 / 1.00 🏆

Anlamı: Model, kendisine verilen doküman dışına asla çıkmıyor ve bilgi uydurmuyor. Verilen cevapların tamamı dokümandan türetilmiş.

Context Recall (Bağlam Hatırlama): 0.975 / 1.00 🧠

Anlamı: Sistem, sorulan soruya cevap vermek için gereken bilgiyi doküman içinden %97.5 oranında başarıyla bulup getiriyor.

Answer Relevancy:

Sorulan sorulara verilen cevapların alaka düzeyi ortalama 0.87 civarındadır.

🍳 Veri Seti Hazırlama Süreci
Bu başarının arkasında titiz bir veri hazırlama süreci yatmaktadır:

Kategorizasyon: Kullanıcı soruları 11 farklı sınıfa ayrıldı.

Yapay Zeka Destekli Veri Üretimi: Gemini 3 Pro kullanılarak, her kategori için varyasyonlu cümleler üretildi. Toplamda 1200 cümlelik bir veri seti oluşturuldu.

Eğitim: Veri seti %80 Eğitim - %20 Test olarak bölündü ve SVC (Support Vector Classifier) modeli eğitildi.

🛠️ Kurulum ve Çalıştırma
1. Gereksinimleri Yükle
Bash

pip install streamlit pandas scikit-learn langchain langchain-community langchain-google-genai langchain-chroma pypdf ragas
pip isntall -r requirements.txt
2. Dosyaları Kontrol Et
training.csv: Eğitim verisi.

accutane.pdf: Bilgi kaynağı (Prospektüs).

3. Çalıştır

streamlit run app.py
⚠️ Yasal Uyarı
Bu asistan eğitim amaçlıdır ve tıbbi tavsiye yerine geçmez. Sağlık sorunlarınızda mutlaka doktorunuza danışın.