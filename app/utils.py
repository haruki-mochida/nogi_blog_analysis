import requests
from bs4 import BeautifulSoup
import MeCab
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# MeCabのインスタンスを生成
mecab = MeCab.Tagger("-Ochasen")

# ブログリストURLから各ブログエントリのURLを抽出する関数
def get_blog_urls(blog_list_base_url, page):
    # Check if blog_list_base_url is a string
    if not isinstance(blog_list_base_url, str):
        print("Error: blog_list_base_url should be a string.")
        return []

    # Check if page is a positive integer
    if not isinstance(page, int) or page < 1:
        print("Error: page should be a positive integer.")
        return []

    # 'ima'の値はページ番号によって変わるため、ここで計算
    ima = 1717 if page % 2 == 0 else 1659
    blog_list_url = blog_list_base_url.format(ima=ima, page=page)

    # HTTPリクエストを送信してHTMLを取得し、エラーハンドリングも実施
    try:
        response = requests.get(blog_list_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # HTTPエラーが発生した場合のエラーメッセージ
        print(f'HTTP error occurred: {http_err}')
        return []
    except Exception as err:
        # その他のエラーが発生した場合のエラーメッセージ
        print(f'Other error occurred: {err}')
        return []
    else:
        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = "https://www.nogizaka46.com"
        # 各ブログエントリのURLをリストとして返す
        return [base_url + a['href'] for a in soup.select('a.bl--card')]



# テキストから名詞を抽出する関数
def extract_nouns(text):
    # 抽出した名詞を格納するリスト
    nouns = []
    # テキストを形態素解析
    node = mecab.parseToNode(text)
    # 名詞を抽出
    while node:
        if node.feature.startswith('名詞,固有名詞') and node.surface not in ['乃木坂', 'https']:
            nouns.append(node.surface)
        node = node.next
    # 名詞のリストを返す
    return nouns


# ブログエントリのURLからテキストを取得する関数
def fetch_blog_text(blog_url):
    # HTTPリクエストを送信してHTMLを取得し、エラーハンドリングも実施
    try:
        response = requests.get(blog_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # HTTPエラーが発生した場合のエラーメッセージ
        print(f'HTTP error occurred: {http_err}')
        return ''
    except Exception as err:
        # その他のエラーが発生した場合のエラーメッセージ
        print(f'Other error occurred: {err}')
        return ''
    else:
        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        # ブログエントリのテキスト部分を抽出
        blog_text = soup.select_one('.bd--edit').get_text()
        # テキストを返す
        return blog_text

def create_word_cloud(nouns):
    # ワードクラウドの生成
    wordcloud = WordCloud(background_color='white',width=900,height=500).generate(' '.join(nouns))

    # ワードクラウドを表示
    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
