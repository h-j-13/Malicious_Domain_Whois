# -*- coding: UTF-8 -*-
'''
	功能： 提取预处理后文字内容中tf/idf 的前n个词语，存入文件
'''
import jieba
import jieba.analyse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_top_words(top, filename):
	topK = top
	content = open(filename, 'rb').read()
	tags = jieba.analyse.extract_tags(content, topK=topK)
	# items = str(tags).replace('u\'', '\'').decode("unicode-escape")
	return tags


def count_words(string):
	result = {}
	for word in string.split(','):
		if word not in result:
			result[word] = 0
		result[word] += 1
	result = sorted(result.items(), key=lambda result: result[1], reverse = True)
	# items = str(result).replace('u\'', '\'').decode("unicode-escape")
	return result


if __name__ == '__main__':
	total = ''
	for top in range(10, 16):
		print top
		string = ''
		for i in range(71, 94):
			items = get_top_words(top, '../fenci/code/words_2_' + str(i) + '.txt')
			for word in items:
				string = string + word + ','
		string = string[:len(string) - 1]
		res = count_words(string)
		items = str(res).replace('u\'', '\'').decode("unicode-escape")
		total = total + str(items) + '\n\n'
		string = string + '\n\n\n' + str(items)
	w_file = open('../fenci/fenci_res/色情total_71_94' + '.txt', 'w')
	w_file.write(total)
	w_file.close()
