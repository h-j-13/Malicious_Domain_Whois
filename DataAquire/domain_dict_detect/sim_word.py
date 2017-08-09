# coding=utf-8
import itertools
import MySQLdb
import urllib2

def save_make_up(domain, domains,states):
	conn = MySQLdb.connect("172.26.253.3", "root", "platform", "keywords")
	cur = conn.cursor()  # 获得指向当前数据库的指针
	for i in range(len(domains)):
		# try:
		cur.execute("INSERT INTO forge(domain, make_up, domain_state) VALUES('" + domain + "','" + domains[i] + "', '" + states[i] + "')")
		conn.commit()
		# except:
			# pass
	print '============================'
	cur.close()  # 关闭指针对象
	conn.close()  # 关闭数据库连接对象
	print "domains save succeed!"


def get_sim_words_list(word_dict, word):
	TLDs = ['.cn', '.tk', '.top', '.pw', '.net', '.club', '.xyz', '.cf', '.co']
	sim_letters = []
	sim_words = []
	for k in range(len(word)):
			sim_letters.append(word_dict[word[k]])
	sim_letters = tuple(sim_letters)
	for letter in itertools.product(*sim_letters):
		forge = ''
		for x in letter:
			forge = forge + x
		sim_words.append(forge + '.com')
		for TLD in TLDs:
			sim_words.append(forge + '-com' + TLD)
	return sim_words


def get_state(url):
	resp = urllib2.urlopen(url)
	return resp.code


if __name__ == '__main__':
	word_dict = {'a': ['a', 'A', 'b', 'd', 'g'],
	'b': ['b', 'B', 'd', 'g', 'p', 'h', '6'],
	'c': ['c', 'C', 'o', '0'],
	'd': ['d', 'D', 'g'],
	'e': ['e', 'E', '8'],
	'f': ['f', 'F', 'l'],
	'g': ['g', 'G', '8'],
	'h': ['h', 'H', 'b'],
	'i': ['i', 'I', 'l', '1'],
	'j': ['j', 'J', 'i', 'l', '1'],
	'k': ['k', 'K'],
	'l': ['l', 'L', 'I', 'i', '1', 'il'],
	'm': ['m', 'M', 'n', 'h'],
	'n': ['n', 'N', 'h'],
	'o': ['o', 'O', '0', 'c', 'oc'],
	'p': ['p', 'P', 'q', '9', 'b', 'd'],
	'q': ['q', 'Q', 'p', '9', 'd'],
	'r': ['r', 'R', 'i', 'l'],
	's': ['s', 'S', '5'],
	't': ['t', 'T'],
	'u': ['u', 'U', 'v'],
	'v': ['v', 'V', 'v', 'w', 'y'],
	'x': ['x', 'X'],
	'w': ['w', 'W', 'vv', 'uu'],
	'y': ['y', 'Y', 'v'],
	'z': ['z', 'Z', '2']}
	domains = ['paypal']
	for ini_domain in domains:
		forge_words = get_sim_words_list(word_dict, ini_domain)
		states = []
		forge_words = list(set(forge_words))
		for domain in forge_words:
			print domain
			url = 'http://' + domain
			try:
				state = get_state(url)
				print url
				print state
				state = str(state)
			except:
				print url
				print '=========================='
				state = 'false'
			states.append(state)
		save_make_up(ini_domain, forge_words, states)
