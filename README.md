# renamer
## how to use
```
pip install -r requirements.txt
python3 jpgRenamer.py [some arguments]
```

```
usage: jpgRenamer.py [-h] [--files [FILES ...]] [--dir DIR] [--format FORMAT] [--ext EXT]

options:
  -h, --help            show this help message and exit
  --files [FILES ...], -f [FILES ...]
                        リネーム対象のファイルを指定します
  --dir DIR, -d DIR     リネーム対象のファイルが存在するディレクトリを指定します
  --format FORMAT, -fmt FORMAT
                        リネームのフォーマットを指定します
  --ext EXT             リネーム後の拡張子を指定します
```

## jpgRenamer.py
画像ファイルのexif情報を利用して、撮影日時を元にリネームを行います
