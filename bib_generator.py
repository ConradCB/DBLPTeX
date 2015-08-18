import urllib.request
from html.parser import HTMLParser

def get_refs_list(filename):
	refs_source_file = open(filename, 'r')
	refs_source_list = []

	line_index = 0
	
	recording = False
	current_entry = ""
	
	for line in refs_source_file:
		line_index += 1
		l = line.strip()
		
		if l == "" or l[0] == "#":
			# Skip empty lines, or those beginning with #
			pass
			
		elif l[0] == "%":
			# Toggle whether it's taking a verbatim entry, and ignore the rest of the line
			if recording:
				refs_source_list.append([current_entry])
				recording = False
			elif not recording:
				current_entry = ""
				recording = True
				
		elif recording:
			current_entry += line
			
		else:
			# Check the line has the correct structure, of two comma-separated sections
			if len(l.split(",")) == 2:
				refs_source_list.append(l.split(","))
			else:
				print("ALERT: Incorrectly formatted line!")
				print("Line number " + str(line_index) + " has " + str(len(l.split(","))) + " sections!")
				print("This line has been ignored.\n")
				
	refs_source_file.close()
			
	return refs_source_list

# This relies on the fact that dblp presents the references as .bib files, at an address highly related to the address provided in the source file.
# (And avoids having to do genuine HTML parsing to get the information we want)
# The url will either have /bibtex/ or /bibtex1/ in, to be replaced with simply /bib1/
def retrieve_bibtex_url(dblp_url):
	url = dblp_url.replace("/bibtex1/","/bib1/")
	url = url.replace("/bibtex/","/bib1/")
	return url + ".bib"
	
def retrieve_bibtex(dblp_url):
	return urllib.request.urlopen(retrieve_bibtex_url(dblp_url)).read().decode('utf-8')
	
def get_bibtex(ref_key,dblp_url):
	raw_bibtex = retrieve_bibtex(dblp_url).strip()
	# We rely on the citation key being between the first '{' and ',' in the bibtex file
	key_pos = raw_bibtex.find("{") +1
	comma_pos = raw_bibtex.find(",")
	mangled_bibtex = raw_bibtex[:key_pos] + ref_key + raw_bibtex[comma_pos:]
	return mangled_bibtex
	
	
refs_source_list = get_refs_list("example.txt")
bib_file = open("refs.bib","w")
for source in refs_source_list:
	if len(source) == 2:
		bib_file.write(get_bibtex(source[0],source[1]))
	elif len(source) == 1:
		# It was a verbatim entry
		bib_file.write(source[0])
		
	bib_file.write("\n\n")
	
bib_file.close()
	

