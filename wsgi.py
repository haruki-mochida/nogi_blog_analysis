# Flask アプリケーションのエントリーポイントとして wsgi.py ファイルを作成します。

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
