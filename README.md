PromoConnect
=========

This script aims to automatically connect the network with a fancy gui.
You can also use the following command associated with a cron job:

```bash
curl -k -X POST -m 5 -d accept='Connexion'\
                     -d auth_user='username'\
                     -d auth_pass='password'\
                     -d redirurl='https://www.kernel.org'\
                     -d checkbox_charte='on'\
                     'https://portail-promologis-lan.insa-toulouse.fr:8001'
```
## Requirements
- Python 3.3
- Pyside 1.2.1
- Cx_freeze for python3

## How to build
- Generate the qrc_images.py file with the following command : 

```bash
pyside-rcc -py3 images.qrc -o qrc_images.py
```
- Launch the build command depending on your os:

```bash
python3.3 build_script.py build
python3.3 build_script.py bdist_msi
```
