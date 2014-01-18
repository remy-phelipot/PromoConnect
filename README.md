PromoHack
=========

This script aims to automatically connect the promo network with a fancy gui.
You can also use the following command associated with a cron job:

```bash
curl -k -X POST -m 5 -d accept='Connexion'\
                     -d auth_user='username'\
                     -d auth_pass='password'\
                     -d redirurl='https://www.kernel.org'\
                     -d checkbox_charte='on'\
                     'https://portail-promologis-lan.insa-toulouse.fr:8001'
```
