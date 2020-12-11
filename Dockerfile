FROM python:3.7

MAINTAINER zouxlin3 "zouxlin3@qq.com"

WORKDIR /todo

RUN ln -s -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

WORKDIR /todo

COPY requirements.txt ./

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]

