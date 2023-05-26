import cv2
import sys



target_img1 = cv2.imread(sys.argv[1])
target_img2 = cv2.imread(sys.argv[2])

target_img1 = cv2.resize(target_img1, (256,512))
target_img2 = cv2.resize(target_img2, (256,512))

hog_analayzer = cv2.HOGDescriptor()

hog_özellikleri_img_1 = hog_analayzer.compute(target_img1)
hog_özellikleri_img_2 = hog_analayzer.compute(target_img2)

benzerlik_oranaı = cv2.compareHist(hog_özellikleri_img_1, hog_özellikleri_img_2, cv2.HISTCMP_CORREL)
benzerlik_oranaı = benzerlik_oranaı * 100 
benzerlik_oranaı = str(int(benzerlik_oranaı))


print(f">> benzerlik oranları: %{str(benzerlik_oranaı)}")

