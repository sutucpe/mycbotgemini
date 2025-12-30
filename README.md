💊 Accutane AI Asistanı
Hibrit Mimariye Sahip Akıllı Sağlık Chatbotu
🧠 Proje Hakkında

Accutane AI Asistanı, Accutane (Roaccutane / Isotretinoin) tedavisi hakkında sık sorulan sorulara doğru, hızlı ve kaynaklı cevaplar vermek üzere tasarlanmış hibrit mimarili bir sohbet botudur.

Bu projede:

🧭 Intent Classification ile kullanıcının niyeti anlaşılır

📚 RAG (Retrieval-Augmented Generation) ile tıbbi doğruluk sağlanır

⚡ Gereksiz LLM çağrıları engellenir, maliyet ve gecikme azaltılır

Amaç: “Her soruyu LLM’e atmak yerine, akıllıca yönlendirmek.”

💬 Chatbot Örnekleri
<p align="center"> <img src="https://github.com/user-attachments/assets/15d8c7a2-85db-45e1-be6c-74a7907ece9a" width="22%" /> <img src="https://github.com/user-attachments/assets/655c2f09-5c89-4ce7-aa0f-b66ee5047606" width="22%" /> <img src="https://github.com/user-attachments/assets/3d7bbfd0-4905-4c67-9d52-9220537db81b" width="22%" /> <img src="https://github.com/user-attachments/assets/0d7565f2-2a61-4108-992f-81ea5be490a7" width="22%" /> </p>

| Model / Araç           | Görevi              | Neden Seçildi                                                                        |
| ---------------------- | ------------------- | ------------------------------------------------------------------------------------ |
| **Gemini 2.5 Flash**   | LLM (Cevap Üretimi) | ⚡ Düşük gecikme süresi, uzun bağlamı maliyet-etkin yönetmesi ve RAG için ideal denge |
| **text-embedding-004** | Embedding           | 🎯 Tıbbi terimlerde yüksek semantik hassasiyet, güçlü retrieval başarımı             |
| **Scikit-Learn SVC**   | Intent Classifier   | 🛡️ Hafif, kararlı ve LLM’e kıyasla çok daha düşük maliyetli                         |

🚦 Akıllı Yönlendirme (Routing) Mantığı

Bu sistemin en kritik farkı:
❌ Her soruyu doğrudan LLM’e göndermemesi

Bunun yerine:

Kullanıcı sorusu Intent Classifier’dan geçer

Çıkan niyete göre en uygun yol seçilir

🛤️ Karar Mekanizması Nasıl Çalışır?
1️⃣ Deterministik Yol — Hızlı Yanıt ⚡

Eğer intent aşağıdakilerden biriyse:

greeting → Selamlaşma

goodbye → Vedalaşma

unrelated → Konu dışı

bot_identity_and_disclaimer → Bot kimliği / yasal uyarı

📌 Ne olur?

RAG devreye girmez

LLM çağrısı yapılmaz

Önceden tanımlı sabit cevap döner

🧠 Neden?
Bu soruların cevabı nettir.
40 sayfalık PDF taramak gereksizdir.

2️⃣ RAG Yolu — Belge Tabanlı Yanıt 📚

Eğer:

Soru tıbbi bilgi içeriyorsa (doz, yan etki, hamilelik vb.)

Confidence < %70 ise

📌 Ne olur?

accutane.pdf taranır

En alakalı metin parçaları seçilir

LLM’e şu kural verilir:

“Sadece bu dokümandaki bilgilere dayanarak cevap ver.”

🛡️ Neden?
Tıbbi alanda halüsinasyon kabul edilemez.
Bu yaklaşım kaynaklı ve güvenli cevap üretir.

📊 Performans Metrikleri
🎯 1. Intent Classification Başarımı

Genel Accuracy: %78

Sosyal niyetlerde başarı: ≈ %100
| Intent                 | Precision | Recall | F1    |
| ---------------------- | --------- | ------ | ----- |
| greeting               | 1.00      | 0.95   | 0.97  |
| goodbye                | 1.00      | 0.80   | 0.89  |
| unrelated              | 0.89      | 0.93   | 0.91  |
| bot_identity           | 0.86      | 0.95   | 0.90  |
| Tıbbi Intentler (Ort.) | ~0.70     | ~0.70  | ~0.70 |

img src="https://github.com/user-attachments/assets/0b2bfe1b-b23b-4ba3-9362-b46b359227f0" width="25%" />

📌 Not:
Tıbbi intentlerin birbirine karışması doğaldır.
Bu durumda sistem her zaman RAG’a yönlendiği için kullanıcı doğru cevabı alır.

🌟 2. RAG Başarımı (RAGAS)

RAG hattı RAGAS Framework ile değerlendirildi:

🏆 Faithfulness: 1.00 / 1.00

Model asla doküman dışına çıkmıyor.

🧠 Context Recall: 0.975 / 1.00

Gerekli bilginin %97.5’i doğru şekilde getiriliyor.

🎯 Answer Relevancy: ~0.87

Cevaplar soruyla yüksek oranda alakalı.

🍳 Veri Seti Hazırlama Süreci

Bu başarının arkasında sistematik bir veri üretimi vardır:

Kategorizasyon

Toplam 11 intent sınıfı belirlendi

Yapay Zeka Destekli Üretim

Gemini 3 Pro kullanılarak

1200 etiketli cümle oluşturuldu

Eğitim

%80 Eğitim / %20 Test

SVC (Support Vector Classifier) ile model eğitildi






