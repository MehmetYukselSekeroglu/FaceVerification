# Yüz Doğrulama
<p>OSINT işlemlerinde kişileri doğrulamak & tespit edebilmek için tasalarnan bir python projesidir. Yüzleri karşılaştırmak için önceden eğitilmiş modeller kullanan face_recognition kütüphanesi, daha doğru eşleşmeler için resimleri yenien boyutlandırmada openCV ve kullanıcı dostu bir arayüz için Tkinter kullanılmaktadır.</p>

<br>
<br>
<h3> <B>
UYARI: Yanlızca linux üzerinde test edilmiştir diğer sistemler içinde uyumludur ama 
ilgili python paketlerinin kurulumu vs uyumlu olmayabilir özellikle windows üzerinde dlib kurulumu.
</B></h3>
</br>


## Gereksinimler:

| Kütüphane | Genel pip paket ismi |
|-----------|----------------------|
| face_recognition | face_recognition |
| tkinter           | tkinter
| OpenCV            | cv2
| subprocess        | subprocess
| pathlib           | pathlib


</br>

### Gereksinimlerin kurulumu:

```bash
# Sistem çapında gerekli paketlerin kurulumu
sudo apt-get install zenity git python3 

# Python kütüpahanelerinin kurulması
python3 -m pip install face_recognition cv2 tkinter subprocess pathlib

# Reponun sisteme klonlanması
git clone https://github.com/TheKoba-dev/FaceVerification.git

# Kod klasörüne gidiş
cd FaceVerification

# Programın çalıştırılması
python3 main.py

```

# Kullanıcı arayüzü:


### <B>Giriş ekranı </B>
<img src="img/giris.png">

</br>

### Farklı yüzlerin karşılaştırma sonucu
<img src="img/farkli.png"> 

</br>

### Aynı yüzlerin karşılaştırma sonucu
<img src="img/ayni.png">

</br>

# Yenilikler hakkında:

<p>Tespit edilen yüzlerin kare içine alınması arayüz ve sistemde ufak değişiklikler ve geliştirmeler.</p>

<img src="img/update1.png">


</br>

# Geliştirme & Kişiselleştirme:

<p>Proje python3.11 yani yyınlandığı dönemdeki en son sürümle yazılmış olsada önceki sürümlerlede uyumludur 
bunun yanı sıra kodun özelleştirme gerektiren (Program adı, yapımcı bilgisi, bilgi paneli) gibi kısımların büyük çoğunluğu kodun başında belirlenmiştir kolayca özelleştirilebilir ve yeniden dağıtılabilir.</p>


```python
# KUTUPHANE VE TEMP DIZINLERI BELIRLENDI 
CORP_NAME = "PRIME"
APP_NAME = "Yüz doğrulama"
TEMP_PATH = "temp"+str(os.sep)
LIB_PATH = "lib"+str(os.sep)
FULL_PATH_OF_TEMP = str(os.getcwd())+str(os.sep)+TEMP_PATH
```

# İletişim:
<B><h3><a href="https://t.me/BayTapsan">Telegram Adresim.</a></h3></B>

<B><h3><a href="https://t.me/safaksiz_egitim">Telegram Eğitim kanalımız.</a></h3></B>









<!-- Prime osint project için yazılmıştır. [2020 - ~]. -->
<!-- Destek olan tüm hanedan üyelerine selam olsun -->