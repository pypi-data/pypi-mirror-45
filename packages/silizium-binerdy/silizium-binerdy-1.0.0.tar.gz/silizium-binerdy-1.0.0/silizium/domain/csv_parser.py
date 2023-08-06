import os


def words_as_list(file='data/words.csv'):
    file = os.path.join(os.path.dirname(__file__), file)
    with open(file, 'r', encoding='utf-8') as file:
        lines = list(filter(lambda x: x != '\n', file.readlines()))
        return list(map(split_test_data, lines))

def split_test_data(line):
    line = line.strip()
    line = line.split(',')
    while(len(line) < 3):
        line.append(None)
    line[1] = None if line[1] is None or line[1] == 'None' else line[1] == 'True'
    line[2] = None if line[2] is None or line[2] == 'None' else int(line[2])
    return line

def update_words(words, word, test_result, links_visited):
    if any(line == [word, test_result, links_visited] or line == [word, None, None] for line in words):
        return [[word, test_result, links_visited] if line == [word, test_result, links_visited] or line == [word, None, None] else line for line in words]
    else:
        words.append([word, test_result, links_visited])
        return words

def words_to_csv(words, file='data/words.csv'):
    file = os.path.join(os.path.dirname(__file__), file)
    with open(file, 'w', encoding='utf-8') as file:
        [file.write(f'{l[0]},{l[1]},{l[2]}\n') for l in words]
