import json
import string

from random import shuffle


def read(file):
    n = []
    lines = []
    cnt = 0
    with open(file) as data:
        lines = [x['_source']['text'] for x in json.load(data)['hits']['hits']]
    return lines


def length_filter(sentence):
    """sentece must be at least 15 chars long"""
    return len(sentence) >= 15 and len(sentence) <= 200

def appears_once(sentence, words):
    """each object should appear exactly once"""
    count = 0
    for word in words:
        count += sentence.lower().count(word.lower())
    return count is len(words)

def not_contains(sentence,words):
    count = 0
    for word in words:
        count += sentence.count(word)
    return count == 0


def symbols(sentence, max=7):
    """not to much punctuation"""
    count = 0
    for punct in string.punctuation:
        count += sentence.count(punct)
    return count <= max

def replace_objects(sentence, objects):
    sentence_lower = sentence.lower()
    a_start = sentence_lower.index(objects[0].lower())
    b_start = sentence_lower.index(objects[1].lower())
    if a_start < b_start:
        first = sentence[:
                         a_start] + '<span style="color: #9A14B2; font-weight: bold">' + objects[0] + ':[OBJECT_A]</span>'
        middle = sentence[a_start+len(objects[0]):b_start]
        end = '<span style="color: #6CB219; font-weight: bold">' + objects[1] + ':[OBJECT_B]</span>' + sentence[b_start + len(
            objects[1]):]
        return {'original': sentence, 'replaced': first + middle + end}
    else:
        first = sentence[:
                         b_start] + '<span style="color: #9A14B2; font-weight: bold">' + objects[1] + ':[OBJECT_A]</span>'
        middle = sentence[b_start + len(objects[1]):a_start]
        end = '<span style="color: #6CB219; font-weight: bold">' + objects[0] + ':[OBJECT_B]</span>' + sentence[a_start + len(
            objects[0]):]
        return {'original': sentence, 'replaced': first + middle + end}



if __name__ == '__main__':

    s = []
    objs = [['ruby', 'python'], ['android',
                                 'iphone'], ['cat', 'dog'], ['car', 'bicycle'],
            ['summer', 'winter'], ['bmw', 'mercedes'], ['wine', 'beer'],
            ['usa', 'europe'], ['football', 'baseball'], ['chicken', 'beef']]
    with open('data-annotation/result-replaced-objects.json') as js:
        sentences = json.load(js)
        for d in sentences:
            org = d['text']['original']
            for pair in objs:
                if pair[0].lower() in org.lower() and pair[1].lower(
                ) in org.lower():
                    re = replace_objects(org, pair)
                    if re['replaced'][0] is '"':
                        sen = re['replaced'][1:]
                    else:
                        sen = re['replaced']
                    s.append(sen)


    with open('foo.txt','w') as f:
        for se in s:
            f.write(se+'\n')

    #objs = [['ruby', 'python'], ['android','iphone'],['cat','dog'], ['car','bicycle'], ['summer', 'winter'],
    #['bmw','mercedes'], ['wine','beer'], ['usa', 'europe'], ['football','baseball'],['chicken', 'beef']]

    #sentences = []
    #for pair in objs:
    #    files = {
    #        '-'.join(pair): [pair,('better', 'worse', 'superior', 'inferior'), 25],
    #        '{}-better'.format('-'.join(pair)): [pair,[],75]
    #    }
    #    for file, objects in files.items():
    #        lines = read('data-annotation/{}.json'.format(file))
    #        filtered = [{'source': file, 'text':replace_objects(line,objects[0:1][0])} for line in lines if length_filter(line) and appears_once(line, objects[0]) and symbols(line) and not_contains(line, objects[1])]
    #        shuffle(filtered)
    #        sentences += filtered[:objects[2]]


    #with open('result-replaced-objects.json', 'w') as file:
    #    json.dump(sentences, file)
    #
    #with open('result-replaced-sentences.txt', 'w') as file1:
    #    for obj in sentences:
    #        file1.write(obj['text']['replaced']+'\n')