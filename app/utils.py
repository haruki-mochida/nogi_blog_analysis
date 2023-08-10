import requests
from bs4 import BeautifulSoup
import MeCab
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# MeCabのインスタンスを生成
mecab = MeCab.Tagger("-Ochasen")

# ブログリストURLから各ブログエントリのURLを抽出する関数
BASE_BLOG_URL = "https://www.nogizaka46.com/"

def get_blog_urls(member_path, num_posts):
    urls = []
    page_number = 0

    # member_pathをBASE_BLOG_URLと結合する
    full_url = BASE_BLOG_URL + member_path

    while len(urls) < num_posts:
        response = requests.get(full_url)

        if response.status_code != 200:
            break  # エラーが発生した場合、ループを抜ける

        soup = BeautifulSoup(response.content, 'html.parser')
        for anchor in soup.select('a.bl--card'):
            if len(urls) >= num_posts:
                break  # 要求された数だけURLを取得したらループを終了する

            urls.append(anchor["href"])



    return urls





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

def create_word_cloud(word_dict, output_path="wordcloud.png"):
    wordcloud = WordCloud(background_color='white', width=900, height=500).generate_from_frequencies(word_dict)

    plt.figure(figsize=(15, 12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return output_path
