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
### 方法一：Using docker
创建一个目录用于存放db文件
```bash
# 拉取镜像并创建容器
sudo docker pull zouxlin3/todo
sudo docker run --name todo -d -p 5000:5000 -v /你创建的目录:/todo/data zouxlin3/todo
```
```bash
# 进入容器，初始化数据库
sudo docker exec -it todo bash
flask initdb --drop
```
### 方法二：Manually
```bash
# 下载所有文件并安装运行环境
git clone https://github.com/zouxlin3/flask-todolist.git
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
```bashe
# 初始化数据库并运行
flask run
flask initdb --drop 
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
[MIT](LICENSE) © zouxlin3
