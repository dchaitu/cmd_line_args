import json
import sys


class FileStorageImplementation:
	def __init__(self, json_file='./updated_quotes.json'):
		with open(json_file, 'r') as f:
			json_data = json.load(f)

		self.json_data = json_data


	def update_with_index(self):

		for num, quote in enumerate(self.json_data["quotes"],1):
			quote['id'] = num

		with open('./updated_quotes.json','w') as f1:
			json.dump(self.json_data,f1,indent=2)


	def get_quote(self, quote_id):
		for quote in self.json_data["quotes"]:
			if quote['id'] == quote_id:
				return quote["quote"]


	def get_quotes_by_author(self, author_name):
		author_quotes = []
		for quote in self.json_data["quotes"]:
			if quote["author"].lower() == author_name.lower():
				author_quotes.append(quote["quote"])

		return author_quotes

	def get_quotes_by_tag(self, tag):
		author_quotes = []
		for quote in self.json_data["quotes"]:
			if tag.lower() in quote["tags"].lower():
				author_quotes.append(quote["quote"])

		return author_quotes

	def get_quotes_by_search_text(self, search_text):
		author_quotes = []
		for quote in self.json_data["quotes"]:
			if search_text.lower() in quote["quote"].lower():
				author_quotes.append(quote["quote"])

		return author_quotes



if __name__ == '__main__':
	storage = FileStorageImplementation()
	if sys.argv[1]=="--quote" or sys.argv[1]=='-q':
		quote_id = int(sys.argv[2])
		quote = storage.get_quote(quote_id)
		print(quote)
	elif sys.argv[1]=="--author" or sys.argv[1]=='-a':
		author_name = sys.argv[2]
		author_quotes = storage.get_quotes_by_author(author_name)
		print(author_quotes)

	elif sys.argv[1]=="--tag" or sys.argv[1]=='-t':
		tag = sys.argv[2]
		author_quotes = storage.get_quotes_by_tag(tag)
		print(author_quotes)


	elif sys.argv[1]=="--search" or sys.argv[1]=='-s':
		search_text = sys.argv[2]
		author_quotes = storage.get_quotes_by_search_text(search_text)
		print(author_quotes)

	else:
		print(f"Error {sys.argv[1]} argument is not available")
		print('''Available are \n --search or -s for		 search text as argument and prints all quotes containing the given search text 
			\n --tag or -t for 		tag as an argument and prints all quotes with given tag
			\n --quote or -q for 		quote id as argument and prints the corresponding quote as output
			\n --author or -a for		 author name as argument and prints all quotes written by that author''')
