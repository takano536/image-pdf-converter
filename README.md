# image-pdf-converter
本ツールは、画像ファイルをPDFにまとめるツールです。  
[releasesページ](https://github.com/takano536/image-pdf-converter/releases)からダウンロードすることができます。

## 使い方
「ImagePdfConverter.exe」は、CLIソフトです。まとめたい画像ファイルをドラッグ・アンド・ドロップするか、コマンドプロンプトを立ち上げ、以下のようなコマンドを打ち込み、使用してください。
```
ImagePdfConverter.exe --help
```
以下のコマンドは、PDFを作成するコマンドの一例です。
```
ImagePdfConverter.exe C:\Users\user\Pictures\images --output_name img.pdf
```
以下は、実行結果例です。
```
C:\Users\user\Pictures\images
page 1 : img1.jpg
page 2 : img2.jpg
page 3 : img3.jpg
page 4 : img4.jpg
page 5 : img5.png
output folder -> C:\Users\user\Pictures\images
output name -> img.pdf

Proceed ([y]/n)? y
PDF has been created successfully

Press enter key to quit...
```
引数を何も指定せずに実行すると、利用可能なオプションが表示されます。
```
usage: main.py [-h] [-o OUTPUT_FILENAME] [--output_folder OUTPUT_FOLDER] [-e [EXCLUDE [EXCLUDE ...]]]
               [--sort {folder,file,date,ext,file-desc,folder-desc,date-desc,ext-desc}] [-r] [-q QUALITY]
               [input [input ...]]

positional arguments:
  input                 input file or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        output pdf filename
  --output_folder OUTPUT_FOLDER
                        save the output in a certain folder
  -e [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]
                        exclude file, directory or extension
                        selecting an extension, prefix it with dot at the beginning
  --sort {folder,file,date,ext,file-desc,folder-desc,date-desc,ext-desc}
                        how to sort files (default=folder)
  -r, --recursive       recursively get input files
  -q QUALITY, --quality QUALITY
                        quality when converting png format to jpg format (default=95)

error: the following arguments are required: input
```

## コマンドラインオプション
本ソフトでは、以下のオプションを指定できます。
#### 入力ファイル
```
<ファイルのパスやフォルダのパス>
必須の引数です。
ファイルのパスやフォルダのパスを複数指定することができます。
```
#### 出力ファイル名
```
-o <出力ファイル名>, --output_filename <出力ファイル名>
ファイル名を指定します。
指定がなかった場合、1ページ目に指定されたファイルと同様の名前になります。
```
#### 出力フォルダ
```
--outfolder <出力フォルダ先>
ファイルの出力先を指定します。
指定がなかった場合、1ページ目に指定されたファイルの親フォルダに出力されます。
```
#### 除外するファイル
```
-e <ファイルのパスやフォルダのパス>, --exclude <ファイルのパスやフォルダのパス>
ファイルのパスやフォルダのパス、拡張子を複数指定することができます。
拡張子を指定する場合は、先頭にドットを付けてください。
```
#### 画像の並び方
```
--sort <folder|file|date|ext|file-desc|folder-desc|date-desc|ext-desc'>
画像の並び方を指定します。
デフォルト値は「folder」です。
* folder      : フォルダ名で昇順に並び、同一フォルダ内に複数のファイルが有る場合、ファイル名で昇順に並びます。
* file        : ファイル名で昇順に並びます。
* date        : 作成日時で昇順に並びます。
* ext         : 拡張子で昇順に並び、同一拡張子ファイルが複数ある場合、ファイル名で昇順に並びます。
* folder-desc : フォルダ名で降順に並び、同一フォルダ内に複数のファイルが有る場合、ファイル名で降順に並びます。
* file-desc   : ファイル名で降順に並びます。
* date-desc   : 作成日時で降順に並びます。
* ext-desc    : 拡張子で降順に並び、同一拡張子ファイルが複数ある場合、ファイル名で降順に並びます。
```
#### 入力ファイルを再帰的に取得する
```
-r, --recursive
このオプションを指定すると、サブフォルダを含めた全てのファイルを取得します。
```
#### PNG形式のファイルをJPG形式のファイルに変換するときの品質
```
-q, --quality
PNG形式のファイルをJPG形式のファイルに変換するときの品質を指定します。
0から100の値を指定できます。デフォルト値は95です。
```

## 注意
`PNG`形式のファイルは、`JPG`形式のファイルとしてPDFファイルに保存されます。  
`WEBP`形式のファイルには対応していません。

## ライセンス
本ソフトは無保証です。詳しくは[LICENSE](LICENSE)をご覧ください。
