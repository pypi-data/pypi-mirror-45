# Python iPaymu
[![PyPI version](https://img.shields.io/pypi/v/python-ipaymu.svg)](https://pypi.org/project/python-ipaymu/)
[![PyPI version](https://img.shields.io/pypi/dm/python-ipaymu.svg)](https://pypi.org/project/python-ipaymu/)
[![PyPI version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/python-ipaymu/)

Koneksi api iPaymu dengan python

Installing python-ipaymu
-------------------------
Install `python-ipaymu` dengan pip: `pip install python-ipaymu`

Cek Saldo
-------------------------
```
from ipaymupython.ipaymu import iPaymu

ipaymu = iPaymu(api_key)

resp = ipaymu.cek_saldo()

result = resp.read()

print (result)
```

Cek Transaksi
-------------------------
```
from ipaymupython.ipaymu import iPaymu

ipaymu = iPaymu(api_key)

resp = ipaymu.cek_transaksi(id_transaksi)

result = resp.status

print (result)
```

Pembayaran
-------------------------

```
from ipaymupython.ipaymu import iPaymu

ipaymu = iPaymu(api_key)

data = { 
    'product'  : 'Nama Produk', 
    'price'    : '5000', 
    'quantity' : 1, 
    'comments' : 'Keterangan Produk', 
    'ureturn'  : 'http://websiteanda.com/return?q=return', 
    'unotify'  : 'http://websiteanda.com/notify', 
    'ucancel'  : 'http://websiteanda.com/cancel', 
}

resp = ipaymu.pembayaran(data)

result = resp.read()

print (result)
```

Semua hasil return secara default menggunakan format '''json'''

