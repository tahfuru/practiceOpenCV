# OpenCV使ってみた ~環境構築からテストするまで~

## 開発環境
- macOS catalina 10.15.4
- python3
- OpenCV 3.4.10

## 環境構築
1. 前提\
  homebrewをインストール済み
  python3をインストール済み

2. 準備\
OpenCVはver.3を利用する。\
（ver.4以降にはopencv_createsamplesとopencv_traincascadeが含まれないためオリジナルの識別器を生成できない）
```
brew install opencv@3
```
インストール後、どこにダウンロードされたかのパスがコンソールに表示されるので控えておく。\
私の環境では`/usr/local/Cellar/opencv@3`

インストールできたかどうかの確認は、`import cv2`を以下のように実行してエラーなど何も表示されないことで確認できる
```
$ python3
>>> import cv2
>>>
```

3. 開発を行うディレクトリの用意\
適当な場所に作業用フォルダ（ここでは`practicePython`）を作成
```
mkdir practicePython
```

ディレクトリ（フォルダ）構造
```
practicePython
  - cascade
  - negativeImg
  - positiveImg
  - src
  - vec
  - opencv_createsamples
  - opencv_traincascade
```
opencv_createsamplesとopencv_traincascadeはダウンロードしたフォルダのbinの中にある実行ファイルなのでコピーしてこのフォルダにペースト。\
私の環境では`/usr/local/Cellar/opencv@3/3.4.10_2/bin`にあった

## 画像の準備
識別させたいものの正例画像と負例画像を用意する。\
正例画像は認識させたいものの画像、負例画像は正しくないものの画像である。

1. 正例画像の準備\
正例画像は先ほど作成した`positiveImg`に保存する。\
保存した画像のどこに認識させたいものがあるのかを指示する`poslist.txt`を`practicePython/src`に作成する。\

書き方は
```
{ファイルのパス} {認識するもののの個数} {}
```
ここではこのように相対パスを利用して記述。\
認識するものの場所をいちいち指示するのは大変なので、あらかじめ300×300くらいの大きさに拡大・トリミングした画像を利用する。
```
../positiveImg/0001.jpg 1 0 0 297 297
../positiveImg/0002.jpg 1 0 0 297 297
../positiveImg/0003.jpg 1 0 0 297 297
.
.
.
../positiveImg/0030.jpg 1 0 0 297 297
```

2. 負例画像の準備\
負例画像は先ほど作成した`negativeImg`に保存する。




