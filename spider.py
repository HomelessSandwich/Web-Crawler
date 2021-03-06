from urllib.request import urlopen
from linkFinder import LinkFinder
from domain import *
from general import *

class Spider:

	# Class variables (shared amond all instances)
	projectName = ''
	baseURL = ''
	domainName = ''
	queueFile = ''
	crawledFile = ''
	queueSet = set()
	crawledSet = set()
	errorNumber = 0

	def __init__(self, projectName, baseURL, domainName):
		Spider.projectName = projectName
		Spider.baseURL = baseURL
		Spider.domainName = domainName
		Spider.queueFile = 'projects/' + Spider.projectName + '/queue.txt'
		Spider.crawledFile = 'projects/' + Spider.projectName + '/crawled.txt'
		self.boot()
		self.crawlPage('First Spider', Spider.baseURL)

	@staticmethod 
	def boot():
		createProjectDir(Spider.projectName)
		createDataFiles(Spider.projectName, Spider.baseURL)
		Spider.queueSet = fileToSet(Spider.queueFile)
		Spider.crawledSet = fileToSet(Spider.crawledFile)

	@staticmethod
	def crawlPage(theadName, pageURL):
		if pageURL not in Spider.crawledSet:
			print(theadName + ' is now crawling: ' + pageURL)
			print('Queue length: ' + str(len(Spider.queueSet)) + ' | Crawled: ' + str(len(Spider.crawledSet)) + ' | URL Decode Errors: ' + str(Spider.errorNumber))
			Spider.addLinksToQueue(Spider.gatherLinks(pageURL))
			Spider.queueSet.remove(pageURL)
			Spider.crawledSet.add(pageURL)
			Spider.updateFiles()

	@staticmethod
	def gatherLinks(pageURL):
		htmlString = ''
		try:
			response = urlopen(pageURL)
			if 'text/html' in response.getheader('Content-Type'):
				htmlBytes = response.read()
				htmlString = htmlBytes.decode('utf-8')
			finder = LinkFinder(Spider.baseURL, pageURL)
			finder.feed(htmlString)
		except:
			print('Error: Can not crawl page!')
			Spider.errorNumber += 1
			return set()
		return finder.pageLinks()

	@staticmethod
	def addLinksToQueue(links):
		for url in links:
			if (url in Spider.queueSet) or (url in Spider.crawledSet):
				continue
			if Spider.domainName != getDomainName(url):
				continue
			Spider.queueSet.add(url)

	@staticmethod
	def updateFiles():
		setToFile(Spider.queueSet, Spider.queueFile)
		setToFile(Spider.crawledSet, Spider.crawledFile)