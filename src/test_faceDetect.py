import cv2

# 入力画像の読み込み
img = cv2.imread("../img/IMG_0846.JPG")

# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier("/usr/local/Cellar/opencv/4.3.0/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# グレースケール変換(グレースケールを使用すると、高速に顔検出できるらしい)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 顔領域の探索
face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

# 顔領域を赤色の矩形で囲む
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y+h), (0,0,200), 3)

# 結果画像を保存
cv2.imwrite("result.jpg",img)

#結果画像を表示
cv2.imshow('image', img)
cv2.waitKey(0)
