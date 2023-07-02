from collections import Counter

# 名詞とその出現回数を管理するクラス
class WordCounter:
    # 初期化メソッドでカウンターを初期化
    def __init__(self):
        self.word_counter = Counter()

    # 単語のリストを引数に取り、それぞれの単語の出現回数をカウントするメソッド
    def count(self, words):
        for word in words:
            self.word_counter[word] += 1

    # 最も出現回数が多い上位n語を取得するメソッド
    def most_common(self, n):
        return self.word_counter.most_common(n)
