from urllib import request
from urllib.parse import urlencode
import json


class iPaymu:
	base_api_ipaymu = "https://my.ipaymu.com/api/"
	url_ceksaldo = "https://my.ipaymu.com/api/CekSaldo.php"
	url_cektransaksi = "https://my.ipaymu.com/api/CekTransaksi.php"
	url_pembayaran = "https://my.ipaymu.com/payment.htm"

	# api key 
	api_key = ""

	# return format
	return_format = 'json'

	# ACTION : harus dibuat konstant biar tidak ada typo
	PAYMENT = 'payment'

	def __init__(self,api_key):
		self.api_key = api_key



	# check koneksi
	def cek_koneksi(self):
		try:
			req = request.urlopen(self.base_api_ipaymu)
		except request.HTTPError as e:
			raise Exception("{}".format(str(e)))
		except Exception as e:
			raise Exception("{}".format(str(e)))
		else:
			return req

	# membuat request pembayaran baru
	def pembayaran(self,data):
		obj = {
			"key":self.api_key,
			"action":self.PAYMENT,
			"format":self.return_format
		}
		new_obj = obj.update(data)

		try:
			obj_parse = urlencode(new_obj)
			req = request.urlopen(self.url_pembayaran,data=bytes(obj_parse,encoding='utf8'))
		except request.HTTPError as e:
			raise Exception("{}".format(str(e)))
		except Exception as e:
			raise Exception("{}".format(str(e)))
		else:
			return req
	# check saldo 
	def cek_saldo(self):
		try:
			req = request.urlopen(self.url_ceksaldo+"?key={}&format={}".format(self.api_key,self.return_format))
		except request.HTTPError as e:
			raise Exception("{}".format(str(e)))
		except Exception as e:
			raise Exception("{}".format(str(e)))
		else:
			return req
	# chek transaksi berdasarkan nomor invoice

	def cek_transaksi(self,id_transaksi):
		try:
			req = request.urlopen(self.url_cektransaksi+"?key={}&id={}&format={}".format(self.api_key,id_transaksi,self.return_format))
		except request.HTTPError as e:
			raise Exception("{}".format(str(e)))
		except Exception as e:
			raise Exception("{}".format(str(e)))
		else:
			return req