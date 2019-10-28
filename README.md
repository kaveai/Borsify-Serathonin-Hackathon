## Borsify - Kullanımı Kolay & Kişiselleştirilmiş Yatırım Asistanı

Borsify, Sermaye piyasalarına girmemiş, aynı zamanda borsadaki karışık arayüzlerden korkan, çekinen, Eğer hisse alırsa o hisseye dair bilgi akışına hakimiyet sağlayamayacağını düşünen kişiler için, kişiselleştirilmiş asistanı, sade arayüzü ile çözümler sunar. Aynı zamanda Twitter, KAP, Bloomberg gibi haber kaynaklarından topladığı verileri anlamlandırır, işler ve kullanıcıya servis eder.  

## Altyapı
- Borsify içerisinde, LightGBM ile kurulmuş, 8 yıllık borsa verilerini 7 günlük window_size'ler ile öğrenen bir makine öğrenmesi algoritmasına sahiptir. Bu algoritma ile belirlenen hissenin önümüzdeki 7 günlük tahminini gerçekleştirir. 
- Twitter, KAP ve Bloomberg için API üzerinden veriyi indirerek, daha önce 17.000 Tweet  ile kurulmuş Makine öğrenmesi bazlı duygu modellemesi ile veriler üzerinde tahminlemeler yapar. 
- Aynı zamanda, ChatterBot adlı kütüphane ile belli konu başlıkları için eğitilen Sohbetbotu üzerinden kullanıcılara "Hangi Hisseyi almalıyım?", "KCHOL'un durumu nedir?", "Ford'un Kap durumu nedir?", "Ford Alsaydım ne olurdu?" gibi sorularına dinamik olarak hesaplamalar yaparak cevap verir. 

## Gerekli Kütüphaneler
``` python
ChatterBot==1.0.5
chatterbot-corpus==1.2.0
Flask==1.1.1
networkx==2.3
PyYAML==5.1.1
scikit-image==0.15.0
scikit-learn==0.21.2
scipy==1.3.0
lightgbm==2.3.0
lxml==4.3.4
xlrd==1.2.0
```

## Ekran Görüntüleri

- **FROTO Hissesi Ana Sayfa Görseli**
![Froto Ana Sayfa Görsel](froto_gorsel.png)

- **BIST100 Endeksi Ana Sayfası**
![Froto Ana Sayfa Görsel](bist_gorsel.png)

- **Hisse Takip, Bildirim Sayfası Görseli**
![Froto Ana Sayfa Görsel](listeler_gorsel.png)


**Ekim 2019 / [Serathon-in Hackathon](http://serathonin.org.tr/default.aspx)**

**Ka|Ve / Yunus Emre Gündoğmuş, Mert Nuhuz, Kadircan Özdemir**
