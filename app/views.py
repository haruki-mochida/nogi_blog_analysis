from flask import request
from .utils import get_blog_urls, fetch_blog_text, extract_nouns
from .utils import create_word_cloud
from flask import Blueprint, render_template
from flask import request, abort
from bs4 import BeautifulSoup
import requests
from flask import session
from collections import Counter

bp = Blueprint('views', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/members')
def member_selection():
    # メンバー情報を格納するリスト
    members = []

    # 指定されたURLにリクエストを送る
    response = requests.get("https://www.nogizaka46.com/s/n46/diary/MEMBER")

    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(response.text, 'html.parser')

    # 各メンバー情報を取得
    member_links = soup.find_all(class_='ba--mmsel__pc__a hv--op')
    member_names = soup.find_all(class_='ba--mmsel__pc__neme f--head')

    # メンバー情報をリストに追加
    for link, name in zip(member_links, member_names):
        members.append({
            'id': link.get('href'),
            'name': name.text.strip(),
        })

    return render_template('member_selection.html', members=members)

@bp.route('/posts', methods=['POST'])
def blog_post_retrieval():
    # リクエストからメンバーIDと記事の件数を取得し、ブログ記事を取得します
    member_id = request.form.get('member_url')
    num_posts = request.form.get('num_blogs')

    # num_postsの存在チェックとバリデーション
    if num_posts is None or not num_posts.isdigit() or not 1 <= int(num_posts) <= 100:
        abort(400, description="Invalid number of blogs")  # 不適切な入力があった場合は400エラーを返す

    num_posts = int(num_posts)
    session['progress'] = 0

    blog_urls = []
    for i in range(num_posts):
        # 指定したメンバーの1つのブログ記事のURLを取得
        blog_urls = get_blog_urls(member_id, num_posts)
        session['progress'] = (i + 1) / num_posts * 100

    # Save blog URLs for later processing
    session['blog_urls'] = blog_urls

    return render_template('analysis_waiting.html')

@bp.route('/progress')
def progress():
    # 進行状況を返します。
    return str(session.get('progress', 0))

@bp.route('/analysis', methods=['POST'])
def analysis():
    blog_urls = session.get('blog_urls', [])

    # すべてのブログ記事から名詞を抽出
    all_nouns = []
    for blog_url in blog_urls:
        blog_text = fetch_blog_text(blog_url)
        nouns = extract_nouns(blog_text)
        all_nouns.extend(nouns)

    word_dict = Counter(all_nouns)

    wordcloud_image_path = create_word_cloud(word_dict)

    return render_template('word_cloud_display.html', word_cloud_path=wordcloud_image_path)
