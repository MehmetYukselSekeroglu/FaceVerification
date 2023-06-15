#!/usr/bin/env python3
import tkinter as tk
import face_recognition
from tkinter import ttk
from tkinter.font import Font
from tkinter import filedialog
from PIL import Image , ImageTk
from pathlib import Path
import os 
import cv2 
import subprocess
import random

"""
-------------------- PRIME SECURITY --------------------

Developed By https://github.com/TheKoba-dev


Tavsiye edilen & Test edilmiş python sürümü     :: python3.11
Test Edilen sistemler                           :: Kali linux 2023.1 
Desteklenene sistemler                          :: Linux && Windows 
Versiyon numarası                               :: v0.0.8 stable
Son düzenlenme Tarihi                           :: 26.05.2023 12:00
Yazılım lisans                                  :: Gnu Gpl v2
İletişim                                        :: https://t.me/BayTapsan
Kütüphane klasörü                               :: $PWD/lib
Tmp klasörü                                     :: $PWD/temp

>> Doğruluk oranı hakkında:

Hafiflik için python'daki openCV be face_recognition kullanılmaktadır bu nedenle 
benzerlik oranı hesaplanırken önceden eğitilmiş modeller kullanılmaktadır.
Bunların eğitim kalitesine bağlı olarak doğruluk oranı değişmektedir.



"""

# SELECT YOUR USER LANG BRO
USER_LANG = "TR"

# KUTUPHANE VE TEMP DIZINLERI BELIRLENDI 
CORP_NAME = "PRIME"
TEMP_PATH = "temp"+str(os.sep)
LIB_PATH = "lib"+str(os.sep)
FULL_PATH_OF_TEMP = str(os.getcwd())+str(os.sep)+TEMP_PATH



langPack_tr = {
    "init_info":">> Karşılaştırılacak yüzleri seçiniz.",
    "select_img" : "Resim seç",
    "compre_faces": "Karşılaştır",
    "external_info":"""-- Kullanım için notlar --
Bu yazılım python face_recognition & openCV kütüphanesine dayanmaktadır.
Yüz benzerliklerini hesaplamada bu kütüphane kullanılır %50+ benzerlik oranı yüksek ihtimalle aynı kişi demektir.
""",
    "msg_noface_found":"Yüz bulunamadı.",
    "null_image_select":"Resim alanlarından birisi boş bırakıldı.",
    "similarity_level":">>> Eşleştirme Oranı: ",
    "err_msg2":">> Hata: "
    }


langPack_en = {
    "init_info":">> Select the faces to compare.",
    "select_img":"Choose image",
    "compre_faces":"Compare",
    "external_info":"""-- Notes for usage --
This software is based on python face_recognition & openCV library.
This library is used to calculate facial similarities. The 50%+ similarity rate means the same person with a high probability.
""",
    "msg_noface_found":"No faces found.",
    "null_image_select":"One or two of the image fields is left blank.",
    "similarity_level":">>> Match Rate: ",
    "err_msg2":">> Error: ",
    }



if USER_LANG.upper() == "TR":
    lang = langPack_tr
    APP_NAME = "Yüz doğrulama"

elif USER_LANG.upper() == "EN":
    lang = langPack_en
    APP_NAME = "Face verification"

else:
    lang = langPack_en
    APP_NAME = "Face verification"


# Baslangıcta düzenli olarak temp dizini kontrol ediliyor 
if not os.path.exists(FULL_PATH_OF_TEMP):
    os.mkdir(FULL_PATH_OF_TEMP)

# Hata ayıklama vs durumları için konsol log fonksiyonu 
def ConsoleLog(log_msg:str):
    print(f"[LOG]: {str(log_msg)}")

# Ana sınıfın belirlenmesi 
class FaceVerifyKift(tk.Tk):
    def __init__(self, AppName):
        # tk.Tk nın miras alınması 
        super().__init__()

        # Program kapatma protokolünün set edilmesi 
        self.protocol("WM_DELETE_WINDOW", self.ShutDownProtocol)

        # Programın iconunun ve aynı zamanda ön tanımlı resim konumunun set edilmesi
        self.deffaults_img_path = LIB_PATH+"faceicon.png"


        #self.window_icon_path = "windowicon.png"
        
        # Set edilen ön tanımlı resmin tk için uyumku gake getirilmesi 
        self.def_img1 = ImageTk.PhotoImage(self.ResizeImg(self.deffaults_img_path))
        self.def_img2 = ImageTk.PhotoImage(self.ResizeImg(self.deffaults_img_path))
        
        # ilk açılışta resimlerin seçilmesine kadar ekranda görünecek resimler 
        self.Face_1 = self.deffaults_img_path
        self.Face_2 = self.deffaults_img_path
        
        #self.DarkThemaColor = "#2F2F2F"
        #self.DarkButtonColor = "#655C5C"

        # Butonların daha yumuşak görünebilmesi için temanın ayarlanması
        self.WindowStye = ttk.Style()
        self.WindowStye.theme_use("clam")


        #self.config(background=self.DarkThemaColor)
        #self.resizable(False, False)
        
        # Pencere ikonunun set edilmesi 
        self.iconphoto(False, tk.PhotoImage(file=self.deffaults_img_path))
        
        # Uygulama adı ve pencere yapıı tanımlandı 
        self.title(AppName)
        self.geometry("900x500+200+50")
        #self.protocol("WM_DELETE_WINDOW", self.AppShutdownProtocol)

        # Yazı fontları ve renkleri belirlendi 
        self.TitleFonts = Font(family="arial",size="16",)
        self.StandartFonts = Font(family="arial",  size="12",)   
        self.StandartColor = "#0a1e4a"

        # Bilgi verme kısmı tanımlandı 
        self.BilgiVerme = tk.Label(text=lang["init_info"], font=self.StandartFonts, 
                                   fg=self.StandartColor,)
        self.BilgiVerme.place(relx=0.01, rely=0.01)

        # 1.Resmin seçilmesi için gereken buton tenılandı 
        Open_yüz_1 = ttk.Button(text=lang["select_img"], command=self.GüzelResimSecici__1)
        Open_yüz_1.place(relx=0.22, rely=0.1)

        # 1.Resim için ekranda gösterme alanı tanımlandı 
        self.Show_img1 = tk.Label(width=150, height=150,  image=self.def_img1)
        self.Show_img1.place(relx=0.2, rely=0.2)


        # 2.Resim için gereken buton tanımlandı
        Open_yüz_2 = ttk.Button(text=lang["select_img"] ,command=self.GüzelResimSecici__2)
        Open_yüz_2.place(relx=0.62, rely=0.1)

        # 2.resmi ekrana eklemek için olan alan
        self.Show_img2 = tk.Label(width=150 , height=150, image=self.def_img2 )
        self.Show_img2.place(relx=0.6, rely=0.2)


        # Yüzleri karşılaştırma butonu için olan alan
        self.GetQueryFaces = ttk.Button(text=lang["compre_faces"], command=self.AnalayzTheFace)
        self.GetQueryFaces.place(relx=0.01, rely=0.5)

        self.EkBilgiler_data = lang["external_info"]

        self.AltBilgiPaneli = tk.Label(text=f"""Powered by {AppName}.\n\n{self.EkBilgiler_data} """, fg=self.StandartColor, justify="left")
        self.AltBilgiPaneli.place(relx=0.01, rely=0.6)




    # Resimleri ekrana sığdırmak için 
    def ResizeImg(self,PathToImg):
        TargetImg = Image.open(PathToImg)
        ResizedImg =TargetImg.resize((150, 150))
        return ResizedImg


    # linux ortamında Dosya seçimini daha güzel hale getirildi 
    # ama windows için hala standart Tkinter seçicisi kullanılmakta
    def GüzelResimSecici__1(self):
        if os.name == "posix":
            self.selected_file = subprocess.run(["zenity", "--file-selection", '--file-filter=Resim dosyaları (*.png, *.jpg, *.jpeg) | *.jpg *.png *.jpeg']
                                                ,capture_output=True, text=True)

            if self.selected_file.returncode == 0:
                self.Face_1 = self.selected_file.stdout.strip()
                self.Show_img1["image"] = self.def_img1 = ImageTk.PhotoImage(self.ResizeImg(self.Face_1)) 
            else:
                pass
        
        else:
            self.Select_img1()


    def GüzelResimSecici__2(self):
        if os.name == "posix":
            self.selected_file2 = subprocess.run(["zenity", "--file-selection", '--file-filter=Resim dosyaları (*.png, *.jpg, *.jpeg) | *.jpg *.png *.jpeg']
                                                ,capture_output=True, text=True)

            if self.selected_file2.returncode == 0:
                self.Face_2 = self.selected_file2.stdout.strip()
                self.Show_img2["image"] = self.def_img2 = ImageTk.PhotoImage(self.ResizeImg(self.Face_2)) 
            else:
                pass
        
        else:
            self.Select_img2()


	# Windows için standart Tkinter dosya seçicisi
    def Select_img1(self):
        FileTypes = (('image files', '*.png *.jpg *.jpeg'),)
        FileName = filedialog.askopenfile(filetypes=FileTypes,initialdir=Path.home())
        try:
            self.Show_img1["image"] = self.def_img1 = ImageTk.PhotoImage(self.ResizeImg(FileName.name)) 
            self.Face_1 = FileName.name
        except Exception:
            pass
            #self.Face_1 = self.deffaults_img_path
        
    def Select_img2(self):
        FileTypes = (('image files', '*.png *.jpg *.jpeg'),)
        FileName1 = filedialog.askopenfile(filetypes=FileTypes,initialdir=Path.home())
        try:
            self.Show_img2["image"] = self.def_img2 = ImageTk.PhotoImage(self.ResizeImg(FileName1.name)) 
            self.Face_2 = FileName1.name
        except Exception:
            pass
            #self.Face_2 = self.deffaults_img_path
        
    # Programın doğru kapanması için protokol 
    def ShutDownProtocol(self):
        temp_icerik = os.listdir(TEMP_PATH)
        for element in temp_icerik:
            os.remove(TEMP_PATH+str(element))
        
        self.destroy()
    
    
    
    
    # final olarak karşılaştırma kodları
	
    def AnalayzTheFace(self):
        try:
			
			# Resimleri vs değişkenlere atandı 
            final_status = {}
            
            target_img1 = cv2.imread(self.Face_1)
            target_img2 = cv2.imread(self.Face_2)
			
			# Eğer dosyalardan birisi boş bırakılırsa hata ile iptal tetikleme kısmı 
            if self.Face_1 == self.deffaults_img_path or self.Face_2 == self.deffaults_img_path:
                ger_ssa = "s"
                get_ims = 1
                sn = ger_ssa+get_ims

            
            # Doğru analiz için resimler gri olarak yeniden ayarlandı. 
            target_img1 = cv2.cvtColor(target_img1, cv2.COLOR_BGR2GRAY)
            target_img2 = cv2.cvtColor(target_img2, cv2.COLOR_BGR2GRAY)
            
			# face_ecognition un resimleri kullanabilmesi için temp altınsa kayıt isimleri
            rand_save_name1 = f"face_image_{str(random.randint(12,9999))}.jpg"
            rand_save_name2 = f"face_image_{str(random.randint(12,9999))}.jpg"

			# Dsoyalar kaydedildi
            cv2.imwrite(TEMP_PATH+rand_save_name1,target_img1)
            cv2.imwrite(TEMP_PATH+rand_save_name2, target_img2)
            

            # Tanıma kütüphanesi için dosydan okunuyor tekrardan

            kisi_1 = face_recognition.load_image_file(TEMP_PATH+rand_save_name1)
            kisi_2 = face_recognition.load_image_file(TEMP_PATH+rand_save_name2)

			# Resimler numpy array a çevriliyor 
            kisi_1_encoded = face_recognition.face_encodings(kisi_1, model="cnn", num_jitters=4)[0]
            kisi_2_encoded = face_recognition.face_encodings(kisi_2, model="cnn", num_jitters=4)[0]

            # saf benzerlik oranı hesaplaması 
            raw_benzerlik_oranı = face_recognition.face_distance([kisi_1_encoded], kisi_2_encoded)


            # benzerlik oranının okunaklı hale getirilmesi
            benzerlik_tam = 1 - raw_benzerlik_oranı[0]
            benzerlik_tam = benzerlik_tam * 100
            benzerlik_tam = int(benzerlik_tam)

			# Yüzler kare içersine alınıyor 
            raw_face_landmarks1 = face_recognition.face_locations(kisi_1)
            raw_face_landmarks2 = face_recognition.face_locations(kisi_2)

            for face_location in raw_face_landmarks1:
                top, right, bottom, left = face_location
                image_is1 = cv2.imread(self.Face_1)
                cv2.rectangle(image_is1, (left, top), (right, bottom), (0, 255, 0), 3)
                rand_landmark_name1 = f"landmarks_{str(random.randint(1,9999))}.jpg"
                
                cv2.imwrite(TEMP_PATH+rand_landmark_name1,image_is1)

            for face_location in raw_face_landmarks2:
                top, right, bottom, left = face_location
                image_is2 = cv2.imread(self.Face_2)
                cv2.rectangle(image_is2, (left, top), (right, bottom), (0, 255, 0), 3)
                rand_landmark_name2 = f"landmarks_{str(random.randint(1,9999))}.jpg"            

                cv2.imwrite(TEMP_PATH+rand_landmark_name2, image_is2)
            

            
            
            self.Show_img1["image"] = self.def_img1 = ImageTk.PhotoImage(self.ResizeImg(TEMP_PATH+rand_landmark_name1)) 
            self.Show_img2["image"] = self.def_img2 = ImageTk.PhotoImage(self.ResizeImg(TEMP_PATH+rand_landmark_name2))

            
            temp_icerik = os.listdir(TEMP_PATH)
            for element in temp_icerik:
                os.remove(TEMP_PATH+str(element))
            
            final_status = {"success":True, "oran1":str(benzerlik_tam)}


        except IndexError as msg:
            final_status = {"success":False, "messagess":lang["msg_noface_found"]}
        
        except TypeError:
            final_status = {"success":False, "messagess":lang["null_image_select"]}


        if final_status["success"] == True:
            benz = str(final_status["oran1"])
            self.BilgiVerme["text"] = lang["similarity_level"]+f"%{benz}"
            self.BilgiVerme["fg"] = "green"

        else:
            err_msg = final_status["messagess"]
            self.BilgiVerme["text"] = lang["err_msg2"]+f"{err_msg}"
            self.BilgiVerme["fg"] = "red"


if __name__ == "__main__":
    FaceVeriyApp = FaceVerifyKift(f"{APP_NAME} | {CORP_NAME}")
    FaceVeriyApp.mainloop()
