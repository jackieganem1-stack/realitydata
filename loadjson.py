import urllib.request, json 
counts = dict()
with urllib.request.urlopen("https://www.reddit.com/r/webscraping/comments/1c4jd72/where_to_begin_web_scraping/.json") as url:
    data = json.load(url)
print(type(data))
for datum in data:
	print(datum)
for line in datum:
	words = line.split()
print(words)
'''
for line in data:
	words = line.split()
	for word in words:
		counts[word] = counts.get(word, 0) + 1
bigcount = None
bigword = None
for word, count in list(counts.items()):
     if bigcount is None or count > bigcount:
          bigword = word
          bigcount = count
 
print(bigword, bigcount)
'''
