from bs4 import BeautifulSoup
import requests
import sys
import re
import bs4
from inspect import currentframe, getframeinfo
import json
import csv
from optparse import OptionParser

class WebScrapper:
	def __init__(self,response,config):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
		self.parsed = BeautifulSoup(response,'html.parser')
		self.child = self.parsed.findChild()
		self.path = []
		self.backtracking = 0
		self.locs = []
		self.found = 0
		self.strin = ''
		self.more = 0
		self.first = 1
		self.dynamic_path = []
		self.type = ''
		self.identifier = ''
		self.locator = ''
		self.sequence = 0
		self.setflags(config)
	def setflags(self,config):
		self.type = "dynamic"
		if "sequence" in config.keys():
			self.sequence = 1
		if self.type == "dynamic":
			if "identifier" in config.keys():
				self.identifier = config['identifier']
			if "locator" in config.keys():
				self.locator = config['locator']
#		print("Type:",self.type)
#		print("String:",self.strin)
	def get_link(self,root):
		backtracking = 0
		while True:
			if root.name == "a":
				return root.attrs['href']
			if backtracking == 1:
				if root.find_next_sibling() == None:
					root = root.findParent()
				else:
					root = root.find_next_sibling()
					backtracking = 0
			elif root.findChild() == None:
				if root.find_next_sibling() == None:
					root = root.findParent()
					backtracking = 1
				elif root.find_next_sibling() != None:
					root = root.find_next_sibling()
			else:
				root = root.findChild()
#print("Unable to locate link");
		return None
				
				
	def get_data(self):
		t = ''
		for i in self.path:
			t += i[0] + '%s' % str(i[1])
		back = 1
		temp = self.chil
		while temp.findParent() != None:
			if temp.attrs != None:
				attributes = self.child.attrs
				for i in attributes.keys():
					if isinstance(attributes[i],list):
						t = ' '.join(attributes[i])
						attributes[i] = t
						self.dynamic_path.insert(0,[temp.name,attributes])
				self.dynamic_path.insert(0,[temp.name,attributes])
				break
			self.dynamic_path.insert(0,temp.name,temp.attrs)
			temp = temp.findParent()
		self.path = self.dynamic_path
#		print("Line:",getframeinfo(currentframe()).lineno,t)
	def locate_table_body(self,table):
		temp = table
		backtracking = 0
		while True:
			if temp.name == "thead":
				return temp
			if temp.name == "tbody":
				return temp
			if temp.name == "tr":
				return temp
			if backtracking == 1:
				if temp.find_next_sibling() == None:
					temp = temp.findParent()
				else:
					temp = temp.find_next_sibling()
					backtracking = 0
			elif temp.findChild() == None:
				if temp.find_next_sibling() == None:
					temp = temp.findParent()
					backtracking = 1
				elif temp.find_next_sibling() != None:
					temp = temp.find_next_sibling()
			else:
				temp = temp.findChild()			
		print("Unable to locate table")
		return None
	def get_sequence_data(self):
		temp = self.child
		backtracking = 0
		dat = []
		while True:
			if temp == None:
				break
			if isinstance(self.locator,str):
				if temp.text.replace("\n",'').strip() == self.locator:
					dat.append(self.get_dynamic_data(temp))
			elif isinstance(self.locator,dict):
				ret = self.check_condition(temp)
				if ret == 1:
					dat.append(self.get_dynamic_data(temp))
			if backtracking == 1:
				if temp.find_next_sibling() == None:
					temp = temp.findParent()
				else:
					temp = temp.find_next_sibling()
					backtracking = 0
			elif temp.findChild() == None:
				if temp.find_next_sibling() == None:
					temp = temp.findParent()
					backtracking = 1
				elif temp.find_next_sibling() != None:
					temp = temp.find_next_sibling()
			else:
				temp = temp.findChild()
			if temp == None:
				break
		for i in dat:
			print(i)
		return [dat]
	def grabber(self,temp):
		res = ''
		if self.identifier['datatype'] == "string":
			res += temp.text.replace("\n",'').replace("\t"," ").replace("  ",'').strip()
#			print(temp.text.replace("\n",'').replace("\t",' ').replace("  ",'').strip())
		elif self.identifier['datatype'] == "link":
			res += temp.attrs['href']
#			print(temp.attrs['href'])
		elif self.identifier['datatype'] == "value":
			res += temp.attrs[self.identifier['datatype']]
#			print(temp.attrs[self.identifier['datatype']])
		return res
	def get_dynamic_data(self,curr=None):
		if curr != None:
			temp = curr
		else:
			temp = self.child
		res = ''
		while True:
			if self.identifier['data'] == "unique":
				if self.identifier['level'] == 'same':
#					print(repr(temp.name))
#					print(repr(temp.attrs))
					if temp.name == self.identifier['tag']:
						res += self.grabber(temp)
						break
					if temp.find_next_sibling() != None:
						temp = temp.find_next_sibling()
					else:
						break
							
				elif self.identifier['level'] == 'low':
#					print(repr(temp.name))
#					print(repr(temp.attrs))
					if temp.name == self.identifier['tag']:
						res += self.grabber(temp)
						break
					if temp.findChild() != None:
						temp = temp.findChild()
					else:
						break
			elif self.identifier['data'] == "multiple":
				if self.identifier['level'] == 'same':
					if temp.name == self.identifier['tag']:
						while temp.name == self.identifier['tag']:
							res += self.grabber(temp)
							if temp.find_next_sibling() == None:
									break
							temp = temp.find_next_sibling()
					if temp.find_next_sibling() != None:
						temp = temp.find_next_sibling()
					else:
						break
				elif self.identifier['level'] == "low":
					if temp.name == self.identifier['tag']:
						while temp.name == self.identifier['tag']:
							res += self.grabber(temp)	
							try:
								if temp == None or temp.find_next_sibing() == None:
									break
								temp = temp.find_next_sibling()
							except:
								print(type(temp))
								break
					if temp.findChild() != None:
						temp = temp.findChild()
					else:
						break
			elif self.identifier['data'] == "table":
				contents = []
				if self.identifier['level'] == 'low':
					temp = self.locate_table_body(temp)
#					print("tag:",temp.name)
					if temp.name == "thead":
						temp = temp.find_next_sibling()
#					print("tag",temp.name)
#					assert temp.name == "tbody", "Not body"
					if temp.name != "tr":
						temp = temp.findChild()
					while temp != None:
						td = []
						dat = temp.findChild()
#						print(dat.name)
						while dat != None and dat.name == self.identifier['child']:
							if self.identifier['datatype'] == "string":
								td.append(dat.text.replace("\n",'').replace("  ",'').strip())
							elif self.identifier['datatype'] == "link":
								a = temp
								link = self.get_link(a)
								td.append(link)
							dat = dat.find_next_sibling()
						temp = temp.find_next_sibling()
						contents.append(td)
#					for i in contents:
#						print(i)
					return contents
				elif self.identifier['level'] == 'same':
					while temp.name != 'tr' or tmep.name != 'thead' or temp.name != 'tbody':
						if temp == None:
							return None
						if temp.name == "tr":
							break
						if temp.name == "thead":
							break
						if temp.name == "tbody":
							break
#						print("Searching for head:%s" % temp.name)
						temp = temp.find_next_sibling()
						if temp == None:
							return None
#					print("tag:",temp.name)
					if temp.name == "thead":
						temp = temp.find_next_sibling()
					if temp.name != "tr":
						temp = temp.findChild()
					contents = self.get_table_contents(temp)
					return contents
#		print(repr("Data:"+res))
		return res
	def get_table_contents(self,temp):
		contents = []
		while temp != None:
			td = []
			dat = temp.findChild()
#			print(dat.name)
			while dat != None and dat.name == self.identifier['child'] or dat.name == "th":
				if self.identifier['datatype'] == 'string':
					td.append(dat.text.replace("\n",'').replace("  ",'').strip())
				elif self.identifier['datatype'] == 'link':
					a = temp
					link = self.get_link(a)
					td.append(link)
				dat = dat.find_next_sibling()
				if dat == None:
					break
			temp = temp.find_next_sibling()
			contents.append(td)
#		for i in contents:
#			print(i)
		return contents
	def check_condition(self,child=None):
		if child == None:
			attributes = sorted(dict(self.child.attrs).keys())
			node = self.child
		else:
			attributes = sorted(dict(child.attrs).keys())
			node = child
		for i in dict(node.attrs).keys():
			if isinstance(node.attrs[i],list):
				node.attrs[i] = ' '.join(node.attrs[i])
		target_attrs = sorted(self.locator.keys())
		nullfound = 0
		count = 0
		for i in target_attrs:
			if self.locator[i] == None:
				 nullfound = 1;count += 1
		found = 0
		if len(target_attrs) == len(attributes):
#			print(self.child.attrs)
#			print(self.locator)
			u =1
			result = []
			for i,j in zip(target_attrs,attributes):
#				print("Loop ran:",u)
				if i == j:
					if self.locator[i] == None or node.attrs[j] == None:
						result.append(0)
						continue
					if self.locator[i] == node.attrs[j] or node.attrs[j].find(self.locator[i]) != -1:
						print(self.locator[i],node.attrs[j])	
#						print("After If condition is true for  %s and %s" %(i,j))
#						assert i == j, "These %s and %s are not equal" % (i,j)
						if nullfound == 1:
							result.append(1)
						else:
							found = 1
					else:
						if nullfound == 1:
							result.append(0)
						else:
							return 0
				else:
#					print("Target:",self.locator[i])
#					print("Found:",self.child.attrs[j])
					return found
				u += 1
			if nullfound == 1:
				if result.count(0) == count:
					return 1
				else:
					return 0
			else:
				return found
		return found
	def locatepath(self):
		while True:
			if self.child == None:
				break
			h = '/'
			for i in self.path:
				h += i[0] + '/'
			if self.child.text != None:	
				if self.type == "dynamic":
					if isinstance(self.locator,str):
						if self.child.text.replace("\n",'').strip() == self.locator:
							if self.sequence == 1:
								return self.get_sequence_data()
							else:
								return self.get_dynamic_data()
							break
					elif isinstance(self.locator,dict):
						ret = self.check_condition()
						if ret == 1:
							if self.sequence == 1:
								return self.get_sequence_data()
							else:
								return self.get_dynamic_data()
							break
							
			if self.backtracking == 1:
				if self.child.find_next_sibling() == None:
					self.child = self.child.findParent()
					try:
						self.path.pop()
					except:
						print("Error while popping")
						return
				else:
					self.child = self.child.find_next_sibling()
					try:
						self.path.pop()
					except:
						print("Error while popping")
						return
					attributes = self.child.attrs
					for i in attributes.keys():
						if isinstance(attributes[i],list):
							temp = ' '.join(attributes[i])
							attributes[i] = temp
					self.path.append([self.child.name,attributes])
					self.backtracking = 0
			elif self.child.findChild() == None:
				if self.child.find_next_sibling() == None:
					self.child = self.child.findParent()
					self.backtracking = 1
					try:
						self.path.pop()
					except:
						print("Error while popping")
						return
				elif self.child.find_next_sibling() != None:
					self.child = self.child.find_next_sibling()
					try:
						self.path.pop()
					except:
						print("Error while popping")
						return

					attributes = self.child.attrs
					for i in attributes.keys():
						if isinstance(attributes[i],list):
							temp = ' '.join(attributes[i])
							attributes[i] = temp
					self.path.append([self.child.name,attributes])
			else:
				if self.first == 1:
					self.path.append([self.child.name,self.child.get('class')])
					self.first = 0
				self.child = self.child.findChild()
				attributes = self.child.attrs
				for i in attributes.keys():
#					print(type(attributes[i]))
					if isinstance(attributes[i],list):
						temp = ' '.join(attributes[i])
						attributes[i] = temp
				self.path.append([self.child.name,attributes])	
def start_extraction(scrap_object):
	if scrap_object.type == "static":
		scrap_object.locatepath()
		extract_data("https://snyk.io/test/npm/css-loader/0.28.7",scrap_object)
	elif scrap_object.type == "dynamic":
		data = scrap_object.locatepath()
		if data != None and len(data) >= 1 and isinstance(data[0],list):
			return data
		else:
			return data
def formatter(data):
	temp = []
	multiple_row = 0
	for i in data:
		if isinstance(i,list):
			curr = temp
			temp = []
			if multiple_row == 0:
				for j in i:
					temp.append(curr+j)
				multiple_row = 1
			else:
				t = curr
				curr = []
				for j,k in zip(t,i):
					curr.append(j+k)
				temp = curr
		elif isinstance(i,str):
			if multiple_row == 1:
				for j in temp:
					j.append(i)
			else:
				temp.append(i)
	if len(temp) >= 1 and isinstance(temp[0],list):
		return temp
	else:
		return [temp]
def start_scraping(csv_writer,config,urllist):
	row = []
	scrap_objects = []
	for i in config:
		if i['identifier']['data'] == "table":
			config.remove(i)
			config.append(i)
	for url in urllist:
		final = []
		print("URL:",url)
		if url == '':
			csv_writer.writerow([])
			continue
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
		response = requests.get(url,headers=headers)
		for conf in config:
			obj = WebScrapper(response.text,conf)
			scrap_objects.append(obj)
		data = []
		for i in scrap_objects:
			ret = start_extraction(i)
			data.append(ret)
		scrap_objects = []
		final = formatter(data)
		for i in final:
			csv_writer.writerow(i)
def start_scraping_from_text(config,text):
	row = []
	scrap_objects = []
	for i in config:
		if i['identifier']['data'] == 'table':
			config.remove(i)
			config.append(i)
	final = []	
	for conf in config:
		obj = WebScrapper(text,conf)
		scrap_objects.append(obj)
	data = []
	for i in scrap_objects:
		ret = start_extraction(i)
		data.append(ret)
	scrap_objects = []
	final = formatter(data)
	return final
def start_scraping_from_url(config,url):
	print("URL:",url)
	if url == '':
		return "Not a valid url"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
	response = requests.get(url,headers=headers)
	data = start_scraping_from_text(config,response.text)
	return data

def check_options(options,parser):
	opt = "config_file url outfile".split(" ")
	for i in opt:
		if options.__dict__[i] is None:
			print("Error: %s parameter is required" % i)
			parser.print_help()
			sys.exit(-1)
if __name__ == "__main__":
	parser = OptionParser(usage="Usage: %prog -c <config_file> -u <urllist_file> -o <output_filename>")
	parser.add_option("-c","--config",dest="config_file",help="Specify the path to the config file")
	parser.add_option("-u","--url-list",dest="url",help="Specify the path to the url list text file")
	parser.add_option("-o","--outfile",dest="outfile",help="Specify the output file name")
	(options,args) = parser.parse_args()
	check_options(options,parser)
	url = options.url
	config_file = options.config_file
	outfile = options.outfile
	lis = open(config_file).read()
	config = json.loads(lis)
	headers = []
	strings = []
	for i in config:
		headers.append(i['title'])
	writer = open(outfile,'w')
	csv_writer = csv.writer(writer)
	csv_writer.writerow(headers)
	urllist = open(url,"r")
	urls = []
	for i in urllist:
		urls.append(i.strip())
	start_scraping(csv_writer,config,urls)	
