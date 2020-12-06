import unittest
from app import app, db, Task, User, forge, initdb, admin


class WatchlistTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URL='sqlite:///:memory:')
        db.create_all()
        user = User(name='test')
        user.set_password('test')
        movie = Task(title='test movie', year='2020')
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('404 NOT FOUND', data)
        self.assertIn('返回首页', data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('test\'s Watchlist', data)
        self.assertIn('test movie - 2020', data)
        self.assertEqual(response.status_code, 200)

    # 辅助方法  登录用户
    def login(self):
        self.client.post('/login', data=dict(username='test', password='test'), follow_redirects=True)

    def test_add(self):
        self.login()

        response = self.client.post('/', data=dict(title='new movie', year='2020'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Created sucessfully!', data)
        self.assertIn('new movie - 2020', data)

        response = self.client.post('/', data=dict(title='', year='2020'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Created sucessfully!', data)
        self.assertIn('Invalid input.', data)

        response = self.client.post('/', data=dict(title='new movie', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Created sucessfully!', data)
        self.assertIn('Invalid input.', data)

    def test_edit(self):
        self.login()

        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Movie Edit', data)
        self.assertIn('test movie', data)
        self.assertIn('2020', data)

        response = self.client.post('/movie/edit/1',
                                    data=dict(title='edited movie', year='2020'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Done.', data)
        self.assertIn('edited movie - 2020', data)

        response = self.client.post('/movie/edit/1',
                                    data=dict(title='', year='2020'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Done.', data)
        self.assertIn('Invalid input.', data)

        response = self.client.post('/movie/edit/1',
                                    data=dict(title='edited movie', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Done.', data)
        self.assertIn('Invalid input.', data)

    def test_delete(self):
        self.login()

        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Done.', data)
        self.assertNotIn('test movie-2020', data)

    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('删除', data)
        self.assertNotIn('编辑', data)

    def test_login(self):
        response = self.client.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Login success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('删除', data)
        self.assertIn('编辑', data)
        self.assertIn('<form method="post">', data)

        # 测试使用错误的密码登录
        response = self.client.post('/login', data=dict(username='test', password='wrong'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的用户名登录
        response = self.client.post('/login', data=dict(username='wrong', password='test'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用空用户名登录
        response = self.client.post('/login', data=dict(username='', password='test'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

        # 测试使用空密码登录
        response = self.client.post('/login', data=dict(username='test', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('删除', data)
        self.assertNotIn('编辑', data)
        self.assertNotIn('<form method="post">', data)

    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('test\'s Settings', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(name='new test'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Done.', data)
        self.assertIn('new test', data)

        # 测试更新设置，名称为空
        response = self.client.post('/settings', data=dict(name=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Done.', data)
        self.assertIn('Invalid input.', data)

    # 测试虚拟数据
    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done.', result.output)
        self.assertNotEqual(Task.query.count(), 0)

    # 测试初始化数据库
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

    # 测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(admin, args=['--username', 'test', '--password', 'test'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().name, 'test')
        self.assertTrue(User.query.first().validate_password('test'))

    # 测试更新管理员账户
    def test_admin_command_update(self):
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(admin, args=['--username', 'new test', '--password', 'newtest'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().name, 'new test')
        self.assertTrue(User.query.first().validate_password('newtest'))


if __name__ == '__main__':
    unittest.main()
