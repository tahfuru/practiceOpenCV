import cv2

print('読み込む画像のパス（相対or絶対）')

inputImg = input('>> ')

print('生成後画像の名前（拡張子なし）')

outputImg = input('>> ')

# 入力画像の読み込み（テスト用画像ファイル）
img = cv2.imread(inputImg)

# カスケード型識別器（自作した分類器）
cascade = cv2.CascadeClassifier('/Users/takayafuruta/Documents/practicePython/cascade/cascade.xml')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

dog = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3)

# 犬を赤色の矩形で囲む
for (x, y, w, h) in dog:
  cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 200), 3)

# 結果画像を保存
cv2.imwrite(outputImg + '.jpg', img)

# 結果画像を表示
cv2.imshow('image', img)
cv2.waitKey(0)