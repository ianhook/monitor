import json, urllib2, time

class market(object):
	def __init__(self):
		self.transaction_fee = 0
		self.deposit_fee = 0
		self.withrawal_fee = 0
		self.name = 'fake'
		self.orderBookURL = 'none'

	def getOrderBook(self):
		self.orderBook = json.loads(urllib2.urlopen(self.orderBookURL).read())

	def printOrderBook(self):
		print 'ask: {0}, bid: {1}'.format(self.orderBook['asks'][0], self.orderBook['bids'][0])

	def getAsk(self):
		return float(self.orderBook['asks'][0][0])

	def getBid(self):
		return float(self.orderBook['bids'][0][0])

class bitstamp(market):
	def __init__(self):
		super(bitstamp, self).__init__()
		self.name = 'bitstamp'
		self.transaction_fee = .0048
		self.orderBookURL = 'https://www.bitstamp.net/api/order_book/'

class btce(market):
	def __init__(self):
		self.name = 'btce'
		self.orderBookURL = 'https://btc-e.com/api/2/btc_usd/depth'

class arbitor():
	def __init__(self):
		self.markets = [bitstamp(), btce()]

	def printBooks(self):
		for market in self.markets:
			market.printOrderBook()

	def updateBooks(self):
		for market in self.markets:
			market.getOrderBook()

	def lookForOpp(self):
		self.updateBooks()

		for first in range(len(self.markets)):
			for second in range(first + 1, len(self.markets)):
				if self.markets[first].getBid() > self.markets[second].getAsk():
					self.printOpp(self.markets[first], self.markets[second])
				elif self.markets[second].getBid() > self.markets[first].getAsk():
					self.printOpp(self.markets[second], self.markets[first])
				else:
					print 'nothing'

	def printOpp(self, sell_market, buy_market):
		print ' {0} -> {1} || ${2} - ${3} = ${4} :: {5}%'.format( 
					buy_market.name,
					sell_market.name, 
					sell_market.getBid(),
					buy_market.getAsk(), 
					(sell_market.getBid() - buy_market.getAsk()),
					((sell_market.getBid() - buy_market.getAsk()) / buy_market.getAsk() * 100.0))


	def monitor(self):
		sleep = 10
		count = 100
		while True:
			self.lookForOpp()
			#a.printBooks()
			if sleep * count > 60:
				print time.strftime("%a, %d %b %Y %H:%M:%S -0800")
				count = 0
			time.sleep(sleep)
			count += 1

a = arbitor()
a.monitor()


