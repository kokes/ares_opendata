from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import re
from urllib.parse import unquote

class aresHandler(BaseHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		self.db = sqlite3.connect('../vystupy/data.db')
		self.re = {
			'firmy': re.compile(r'/api/firma/(?P<ico>[0-9]+)$'),
			'fosoby': re.compile(r'/api/fosoby/(?P<ico>[0-9]+)$'),
			'posoby': re.compile(r'/api/posoby/(?P<ico>[0-9]+)$'),
			'hledej': re.compile(r'/api/hledej/(?P<q>.+)$'),
		}
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)

	def html(self, data):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(data)

	def json(self, obj):
		resj = json.dumps(obj, indent=2).encode()
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		self.wfile.write(resj)

	def firma(self):
		m = self.re['firmy'].match(self.path)
		if m is None:
			self.send_response(400)
			return

		ico = int(m.groupdict()['ico'])

		slp = 'rejstrik, ico, obchodni_firma, datum_zapisu, datum_vymazu, sidlo'.split(', ')
		ex = self.db.execute('select %s from firmy where ico = %d' % (', '.join(slp), ico))

		rdt = ex.fetchall()
		res = []
		for el in rdt:
			dt = dict(zip(slp, el))
			dt['sidlo'] = json.loads(dt['sidlo'])
			res.append(dt)


		self.json(res)

	def fosoby(self):
		m = self.re['fosoby'].match(self.path)
		if m is None:
			self.send_response(400)
			return

		ico = int(m.groupdict()['ico'])

		slp = 'ico, nazev_organu, datum_zapisu, datum_vymazu, nazev_funkce, jmeno, prijmeni, titul_pred, titul_za'.split(', ')
		ex = self.db.execute('select %s from fosoby where ico = %d order by datum_vymazu <> \'\', datum_vymazu desc' % (', '.join(slp), ico))

		res = [dict(zip([j[0] for j in ex.description], el)) for el in ex.fetchall()]

		self.json(res)

	def posoby(self):
		m = self.re['posoby'].match(self.path)
		if m is None:
			self.send_response(400)
			return

		ico = int(m.groupdict()['ico'])

		slp = 'ico_organu as ico, nazev_organu, datum_zapisu, datum_vymazu, nazev_funkce, obchodni_firma'.split(', ')
		jev = self.db.execute('select %s from posoby where ico = %d' % (', '.join(slp), ico))

		# dohledej info o firme, kterou vlastnim
		vl = self.db.execute("""select
			p.ico, p.nazev_organu, p.datum_zapisu, p.datum_vymazu, p.nazev_funkce, f.obchodni_firma
			from posoby p
			left join firmy f on f.ico = p.ico

			where ico_organu = %d
			order by p.datum_vymazu <> '', p.datum_vymazu desc
			""" % ico)

		res = {
			'je_vlastnen': [dict(zip([j[0] for j in jev.description], el)) for el in jev.fetchall()],
			'vlastni': [dict(zip([j[0] for j in vl.description], el)) for el in vl.fetchall()],
		}

		self.json(res)

	def hledej(self):
		m = self.re['hledej'].match(self.path)
		if m is None:
			self.send_response(400)
			return

		q = unquote(m.groupdict()['q'])

		slp = 'rejstrik, ico, obchodni_firma, datum_zapisu, datum_vymazu'.split(', ')
		if q.isdigit():
			ex = self.db.execute("select %s from firmy where ico = %d \
			order by datum_vymazu <> \'\', datum_vymazu desc limit 50" % (', '.join(slp), int(q)))
		else:
			ex = self.db.execute("select %s from firmy where obchodni_firma like '%s%%' \
			order by datum_vymazu <> \'\', datum_vymazu desc limit 50" % (', '.join(slp), q))

		res = [dict(zip([j[0] for j in ex.description], el)) for el in ex.fetchall()]

		self.json({
			'q': q,
			'data': res,
			})

	def do_GET(self):
		if self.path == '/':
			with open('index.html', 'rb') as f:
				dt = f.read()

			return self.html(dt)

		if self.path.startswith('/api/firma/'):
			return self.firma()

		if self.path.startswith('/api/fosoby/'):
			return self.fosoby()

		if self.path.startswith('/api/posoby/'):
			return self.posoby()

		if self.path.startswith('/api/hledej/'):
			return self.hledej()

		self.send_response(400) # fallback

if __name__ == '__main__':
	print('prohlizec na http://localhost:8089')
	server = HTTPServer(('', 8089), aresHandler)
	server.serve_forever()