import sys
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup


def main():
	infile = open('seed.txt', 'r')
	for line in infile:
		try:
			line = line.replace('\n','')
			line = urllib.parse.quote(fetch_redirect('http://dbpedia.org/resource/'+line))
			soup = BeautifulSoup(fetch_url('https://es.wikipedia.org/wiki/'+line),'lxml')
			paragraphs = soup.find(id="mw-content-text").find_all("p")
			for paragraph in paragraphs:
				links = paragraph.find_all("a")
				for link in links:
					href = link['href'] 
					if '/wiki/' in href and not href.startswith('Wikipedia:'):
						try:
							if '#' in href: href = href.split('#')[0]
							print (urllib.parse.unquote('"'+line + '"\t"' +href.replace('/wiki/','')+'"').replace('_',' '))
						except:
							pass
		except:
			pass

	infile.close()


def fetch_redirect(query):
	try:
		response = urlopen(query)
		soup = BeautifulSoup(response.read(),'lxml')
		return soup.find(id="title").find('a').getText()
	except:
		return str(e)


def fetch_url(query):
	try:
		response = urlopen(query)
		return response.read()
	except:
		return str(e)
	

if __name__ == '__main__':
	main()

