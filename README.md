PromoHack
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
## Installation
- Download the installer from the "dist" folder of the project
- Launch the installer and that's it!

## How to build
### Requirements
- Python 3.3
- Pyside 1.2.1 or newer
- Cx_freeze

### Step-by-step instructions
