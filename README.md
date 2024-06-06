## 概要
Google Chromeを自動操作して、マッチングアプリ「omiai」でマッチングするまでの過程を自動化する。

## 動作環境
|  | version |
|:-----------|:------------|
| MacOS | 10.15.1 |
| python | 3.7.0 |
| Google Chrome | 78.0.3904.97 |
| ChromeDriver | 78.0.3904.70 |
| Selenium | 3.141.0 |
| Omiai | - |

## 導入
* Google Chrome
  * <https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=ja>
* ChromeDriver
  * `pip install chromedriver-binary==78.0.3904.70`
* Selenium
  * `pip install selenium`
* omiai
  * <https://fb.omiai-jp.com>

## 使い方
1. `secrets.py` に自分の Facebook アカウントとパスワードを書き込む。
2. `python main.py`
