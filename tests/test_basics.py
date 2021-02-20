import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):  # 测试之前运行
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # 创建一个全新的数据库供测试使用

    def tearDown(self):  # 测试之后运行
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):  # 确保应用实例存在
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):  # 确保应用在测试配置中运行
        self.assertTrue(current_app.config['TESTING'])