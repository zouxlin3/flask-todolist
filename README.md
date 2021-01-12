# flask-todolist
> 使用Flask, bootstrap4 和 SQLAlchemy 开发的todo webapp
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
### Demo: https://todo.nuture.group
# 安装
### 方法一：Using docker
```bash
# 拉取镜像并创建容器
sudo docker pull zouxlin3/todo
sudo docker run --name todo -d -p 5000:5000 -v /root/.todo:/todo/data zouxlin3/todo
```
映射目录`/root/.todo`可更换
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

# 参考项目
- [greyli/watchlist](https://github.com/greyli/watchlist)
- [themaxsandelin/todo](https://github.com/themaxsandelin/todo)
- [nauvalazhar/bootstrap-4-login-page](https://github.com/nauvalazhar/bootstrap-4-login-page)
# 许可证
[MIT](LICENSE) © zouxlin3
