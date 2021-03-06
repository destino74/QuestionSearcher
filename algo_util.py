import jieba
import jieba.analyse
import numpy as np

jieba.initialize()

K = 5


def cut_word(sentence):
    result = jieba.cut(sentence)
    return result


def extract_tags(sentence):
    result = jieba.analyse.extract_tags(sentence, topK=K, withWeight=True, allowPOS=())
    keywords = []
    for r in result:
        keywords.append(r[0])
    return keywords


def get_weight(option, page_rank, segments):
    count = 0
    for i, seg in segments:
        for j, s in seg:
            if option in s:
                count = count + page_rank[i]
    return count


def get_answer(options, respones):
    page_rank = []
    segments = []
    score = 0.5
    min_score = 0.00001
    for i, res in enumerate(respones):
        page_rank.append(score)
        score = score / 2.0
        if score < min_score:
            score = 1.0 - np.sum(page_rank)
        words = cut_word(res)
        segments.append(words)

    weights = []
    for i, opt in enumerate(options):
        w = get_weight(opt, page_rank, segments)
        weights.append(w)

    result = []
    s = np.sum(weights)
    for i, w in enumerate(weights):
        result.append((options[i], w / s))

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def test():
    pass


if __name__ == '__main__':
    test()
