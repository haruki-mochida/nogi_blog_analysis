# ビューのユニットテストを記述します。ここでは Flask の testing クライアントを使用してリクエストをシミュレートします。

import unittest
from app import create_app

class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page(self):
        # ホームページが正常に表示されることをテストします。
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 他のページや動作に対するテストケースを追加します。

if __name__ == "__main__":
    unittest.main()
