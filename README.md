Name
====
Automation for "Omiai"

Overview
This python script operates chrome with chromedriver via selenium library, and will find girls you like in "Omiai (Japanese dating apps)".

## Verification environment & Requirement
| Title | Version |
|:-----------|:------------|
| MacOS | 10.15.1 |
| python | 3.7.0 |
| Google Chrome | 78.0.3904.97 |
| ChromeDriver | 78.0.3904.70 |
| Selenium | 3.141.0 |
| Omiai | - |

## Install
* Google Chrome
  	<https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=ja>
* ChromeDriver
	`pip install chromedriver-binary==78.0.3904.70`
* Selenium
	`pip install selenium`
* Registration for "Omiai"
  	<https://fb.omiai-jp.com>

## Usage
1. Rename `secrets_dummy.py` to `secrets.py`
2. Edit `secrets.py` and input your facebook account and password into variables `facebook_account` and `facebook_pass` respectively.
3. `python main.py`

## Author
[TomooMari](https://github.com/TomooMari)
