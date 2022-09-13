# sauna-crawler

## Install

```bash
poetry install
```

## Howl to Run 

```bash
poetry run python sauna_crawler/main.py
```

## Raspberry piで動かす場合

Raspberry piの場合、driverのインストールで意図しないものが入るのと独自のdriverを使わないといけないので
`chromium-chromedriver`をインストールしておく。

```bash
sudo apt install chromium-chromedriver
```

## ログファイル

```
$HOME//log/sauna-crawler/application.log
```

## 利用API
### 緯度経度取得API

https://www.geocoding.jp/api/