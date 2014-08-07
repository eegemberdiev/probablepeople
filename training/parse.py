from lxml import etree
import ast
import re


# parse xml data in training format
def parseTrainingData(filepath):
	tree = etree.parse(filepath)
	root = tree.getroot()
	
	addr_list = []
	for element in root: #this ignores punctuation - need to figure out how to handle
		address = []
		for x in list(element):
			addr_list.append([x.text, x.tag])
			if x.tail.strip() :
				addr_list.append([x.tail.strip(), None])
	return addr_list


# parse osm xml data, return a list of dicts representing addresses
def xmlToAddrList(xml_file):
	tree = etree.parse(xml_file)
	root = tree.getroot()
	addr_list=[]
	for element in root:
		if element.tag == 'node' or element.tag =='way':
			address={}
			for x in element.iter('tag'):
				addr = ast.literal_eval(str(x.attrib))
				address[addr['k']]=addr['v']
			addr_list.append(address)
	return addr_list


# transform natural addresses (in addr:full) from osm xml data into training file
def osmNaturalToTraining(xml_file):
	address_list = xmlToAddrList(xml_file)
	train_addr_list = etree.Element('AddressCollection')
	trainFileName = '../training_data/'+re.sub(r'\W+', '_', xml_file)+'.xml'
	# only the osm tags below will end up in training data; others will be ignored
	osm_tags_to_addr_tags = {
		"addr:housenumber":"AddressNumber",
		"addr:street:prefix":"StreetNamePreDirectional",
		"addr:street:name":"StreetName",
		"addr:street:type":"StreetNamePostType",
		"addr:city":"PlaceName",
		"addr:state":"StateName",
		"addr:postcode":"ZipCode"}
	for address in address_list:
		addr_tokens = address['addr:full'].split()
		train_addr = etree.Element('AddressString')
		is_addr_taggable = True
		#loop through tokens & find tags for each
		for token in addr_tokens:
			is_token_taggable = False
			for key, value in address.items():
				if key in osm_tags_to_addr_tags.keys() and key != 'addr:full' and token in value.split():
					is_taggable = True
					token_xml = etree.Element(osm_tags_to_addr_tags[key])
					token_xml.text = token
					train_addr.append(token_xml)
			if is_token_taggable ==False:
				is_addr_taggable = False
		if is_addr_taggable == True:
			train_addr_list.append(train_addr)
	output = etree.tostring(train_addr_list, pretty_print=True)
	with open(trainFileName, 'w') as f:
		f.write(output)

# create synthetic addresses from osm xml data, then transform into training file
def osmSyntheticToTraining(xml_file):
	address_list = xmlToAddrList(xml_file)
	train_addr_list = etree.Element('AddressCollection')
	trainFileName = '../training_data/'+re.sub(r'\W+', '_', xml_file)+'.xml'
	synthetic_order = [
		('addr:housenumber', 'AddressNumber', 'Street'),
		('addr:street:prefix', 'StreetNamePreDirectional', 'Street'),
		('addr:street:name', 'StreetName', 'Street'),
		('addr:street:type', 'StreetNamePostType', 'Street'),
		('addr:city', 'PlaceName', 'City'),
		('addr:state', 'StateName', 'Area'),
		('addr:postcode', 'ZipCode', 'Area')]
	for address in address_list:
		train_addr = etree.Element('AddressString')
		components = {'Street' : [], 'City' : [], 'Area' : []}
		for source_tag, target_tag, tag_type in synthetic_order:
			if source_tag in address.keys():
				token_xml = etree.Element(target_tag)
				token_xml.text = address[source_tag]
				components[tag_type].append(token_xml)
		compnent_list = []
		for tag_type in ('Street','City', 'Area') :
			l = components[tag_type]
			if l :
				l[-1].tail = ','
		address_xml = components['Street'] + components['City'] + components['Area']
		address_xml[-1].tail = None
		for xml_element in address_xml:
			train_addr.append(xml_element)
		train_addr_list.append(train_addr)
	output = etree.tostring(train_addr_list, pretty_print=True)
	with open(trainFileName, 'w') as f:
		f.write(output)

# create training file (in training_data) for us50 data
def trainFileFromLines(addr_file):
	lines = open(addr_file, 'r')
	addr_index = 0
	token_index = 0
	trainFileName = '../training_data/'+re.sub(r'\W+', '_', addr_file)+'.xml'
	tag_list = [None, 'AddressNumber', 'USPSBox', 'StreetName', 'StreetNamePostType',
                'PlaceName', 'StateName', 'ZipCode', 'suffix']
	addr_list = etree.Element('AddressCollection')
	addr = etree.Element('AddressString')
	for line in lines:
		if line =='\n':
			addr_index += 1
			token_index = 0
			addr_list.append(addr)
			addr = etree.Element('AddressString')
		else:
			split = line.split(' |')
			token_string = split[0]
			token_num = int(split[1].rstrip())
			token_tag = tag_list[token_num]
			token_xml = etree.Element(token_tag)
			token_xml.text = token_string
			addr.append(token_xml)
	output = etree.tostring(addr_list, pretty_print=True)
	with open(trainFileName, 'w') as f:
		f.write(output)



