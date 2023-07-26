from flask import request
import os
print("Current Working Directory: ", os.getcwd())
from .utils import get_blog_urls, fetch_blog_text, extract_nouns
from .utils import create_word_cloud
from flask import Blueprint, render_template
from flask import request, abort
from bs4 import BeautifulSoup
import requests
from flask import session

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

    # 初期化
    session['progress'] = 0

    posts = []
    for i in range(num_posts):
        # 省略: ブログ記事の取得処理
        posts.append(...)

        # 進行状況を更新します。
        session['progress'] = (i + 1) / num_posts * 100

    return render_template('analysis_waiting.html', posts=posts)

@bp.route('/progress')
def progress():
    # 進行状況を返します。
    return str(session.get('progress', 0))

@bp.route('/analysis', methods=['POST'])
def analysis():
    # ブログリストのURLとページ数をリクエストから取得
    blog_list_base_url = request.form.get('blog_list_base_url')
    page = request.form.get('page')
    if page is not None:
        page = int(page)

    # ブログ記事のURLを取得
    blog_urls = get_blog_urls(blog_list_base_url, page)

    # すべてのブログ記事から名詞を抽出
    all_nouns = []
    for blog_url in blog_urls:
        blog_text = fetch_blog_text(blog_url)
        nouns = extract_nouns(blog_text)
        all_nouns.extend(nouns)

    # ワードクラウドを生成
    word_cloud = create_word_cloud(all_nouns)

    return render_template('word_cloud_display.html', word_cloud=word_cloud)
