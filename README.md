# flask-todolist
> A TODO list application developed with Flask, bootstrap4 and  SQLAlchemy.
# 简介
### 功能
- 用户登录
- 新用户注册
- 添加待办任务
- 删除待办任务
- 完成待办任务
- 修改密码
- 修改用户名
- 退出登录
### Demo:
# 安装
### Using docker
```bash
sudo docker pull zouxlin3/todo
sudo docker run --name todo -d -p 5000:5000 zouxlin3/todo
```
### Manually
```bash
git clone https://github.com/zouxlin3/flask-todolist.git
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
flask run
```
# 开发计划
- 添加任务deadline
- 搜索功能
- 待办任务分类
# 参考项目
- [greyli/watchlist](https://github.com/greyli/watchlist)
- [themaxsandelin/todo](https://github.com/themaxsandelin/todo)
- [nauvalazhar/bootstrap-4-login-page](https://github.com/nauvalazhar/bootstrap-4-login-page)
# 许可证
[MIT](license.md) © zouxlin3
