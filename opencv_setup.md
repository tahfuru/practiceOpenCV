# OpenCV使ってみた 〜環境構築からテストするまで〜

## 開発環境
- macOS catalina 10.15.4
- python3
- OpenCV 3.4.10

## 環境構築
1. 前提\
  homebrewをインストール済み(インストールしていない方はこちらを参考にすると良いでしょう https://qiita.com/zaburo/items/29fe23c1ceb6056109fd)\
  python3をインストール済み(インストールしていない方はこちらを参考にすると良いでしょう https://qiita.com/7110/items/1aa5968022373e99ae28)

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

作業用フォルダが以下のようなディレクトリ（フォルダ）構造を持つように必要なディレクトリを作成\
opencv_createsamplesとopencv_traincascadeはダウンロードしたフォルダのbinの中にある実行ファイルなのでコピーしてこのフォルダにペースト。\
私の環境では`/usr/local/Cellar/opencv@3/3.4.10_2/bin`にあった
```
practicePython
[DIR]  - cascade
[DIR]  - negativeImg
[DIR]  - positiveImg
[DIR]  - src
[DIR]  - vec
       - opencv_createsamples
       - opencv_traincascade
```

## 画像の準備
識別させたいものの正例画像と負例画像を用意する。\
正例画像は認識させたいものの画像、負例画像は正しくないものの画像である。

1. 正例画像の準備\
正例画像は先ほど作成した`positiveImg`に保存する。\
保存した画像のどこに認識させたいものがあるのかを指示する`poslist.txt`を`practicePython/src`に作成する。

書き方は
```
{ファイルのパス} {認識するもののの個数} x1 y1 w1 h1 x2 y2 w2 h2 ...
```
xi, yi, wi, hi...はi番目の対象オブジェクトの矩形表現である。(xi, yi)が矩形の左上の点を指定し、(wi, hi)でその矩形の幅と高さを指定\
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
負例画像は先ほど作成した`negativeImg`に保存する\
一緒に負例画像の一覧ファイルを作成\
一覧ファイルには負例画像の絶対パスを記述するだけ\

## 正例のベクトルファイルの生成
`opencv_createsamples`を使う\
最初に作成した作業ディレクトリ`practicePython`に移動して以下のコマンドを実行\
```./opencv_createsamples -info src/poslist.txt -vec vec/positive.vec -num 30```

オプションを下に示す
| オプション | 説明 |
| ---- | ---- |
| -info collection_file_name | 正例のデータベース |
| -vec vec_file_name | 学習のために使用する正例のベクトルファイル |
| -num number_of_samples | 学習する正例の数。デフォルトは1000 |
| -h sample_height | 精霊を学習する際に指定した高さに画像を正規化する。デフォルトは24 |
| -w sample_width | 精霊を学習する際に指定した幅に画像を正規化する。デフォルトは24 |

## 識別器の生成
`opencv_traincascade`を使う\
最初に作成した作業ディレクトリ`practicePython`に移動して以下のコマンドを実行\
```./opencv_traincascade -data cascade -vec vec/positive.vec -bg negativeImg/neglist.txt -numPos 30 -numNeg 30```

必須パラメータを以下に示す
| 必須パラメータ | 説明 |
| ---- | ---- |
| -data cascade_dir_name | 学習された識別器を出力するディレクトリ名 |
| -vec vec_file_name | 先ほどの処理で生成したベクトルファイル |
| -bg background_file_name | 負例画像一覧表ファイル |

オプションを以下に示す
| オプション | 説明 |
| ---- | ---- |
| -numPos number_of_positive_samples | 作成した正例の数。デフォルトは2000 |
| -numNeg number_of_negative_samples | 作成した負例の数。デフォルトは1000 |
| -precalcValBufSize precalculated_vals_buffer_size_in_Mb | 特徴量のメモリサイズ。単位はMB。デフォルトは256 |
| -precalcIdxBufSize precalculatec_idxs_buffer_size_in_Mb | 特徴量のメモリサイズ。単位はMB。デフォルトは256 |
| -featureType <{HAAR, LBP, HOG}> | 使用する特徴量を指定。デフォルトは'HAAR' |
| -w sampleWidth | 正例を作成したときと同じものを指定 |
| -h sampleHeight | 正例を作成したときと同じものを指定 |

## 識別器を利用するプログラムの作成
識別器を利用するためのプログラムを作成。\
`practicePython/src`に移動して以下のプログラム`dogDetector.py`を作成\
{rootDirectory}は自分の環境のディレクトリに変更した上で利用
```python
import cv2

print('読み込む画像のパス（相対or絶対）')

inputImg = input('>> ')

print('生成後画像の名前（拡張子なし）')

outputImg = input('>> ')

# 入力画像の読み込み（テスト用画像ファイル）
img = cv2.imread(inputImg)

# カスケード型識別器（自作した分類器）
cascade = cv2.CascadeClassifier('{rootDirectory}/practiceOpenCV/cascade/cascade.xml')

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
```

## 実験
`practicePython/src`に移動して先ほど作成したプログラム`dogDetector.py`を実行
```
ζ python3 dogDetector.python3                    // この行を実行
読み込む画像のパス（相対or絶対）
>> ./dog_test.jpg                                // 実験してみたい画像のパス
生成後画像の名前（拡張子なし）
>> dog_test_result                               // 同じフォルダ内にdog_test_result.jpgとして結果を出力
```

これで完成！


