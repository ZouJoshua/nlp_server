
- [x] NLP分类服务
- [x] NLP地域服务
- [x] NLP爬虫解析服务
---------------

## NLP分类服务(nlp_category_server)

### 配置

修改 run.py 服务ip及端口

```python
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
SERVER_PORT = os.environ.get('PORT', 19901)
```

修改 settings.py 模型路径及日志

```python
NLP_MODEL_PATH = ""  # nlp 模型路径
PROJECT_LOG_FILE = ""  # 日志文件
```

### 服务设置

#### 启动

```bash
python3 run.py nlp_category_server manage.py start
```

#### 停止

```bash
python3 run.py nlp_category_server manage.py stop
```

#### 重启

```bash
python3 run.py nlp_category_server manage.py restart
```

### API Demo

```python
# url
url1 = 'http://127.0.0.1:19901/nlp_category/category'
url2 = 'http://127.0.0.1:19901/nlp_category/top'
url3 = 'http://127.0.0.1:19901/nlp_category/sub'

# post data format(请求二级分类必须传一级分类，其他可不传) 
parms = {"title": title, "content": content, "top_category": top_category}

# 发送请求
resp1 = requests.post(url1, data=parms)

# 获取结果
result = resp1.text
```

### 目前情况
* 一级分类达到9个类别（1个独立模型），准确率达到95%+，
* 二级分类达到88个类别（8个独立模型），整体准确率达到85%


### 后续优化
* 优化线上模型大小，解决多个模型占内存的问题


---------------

## NLP地域服务(nlp_regional_server)


### 配置

修改 `run.py` 服务端口及ip

```python
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
SERVER_PORT = os.environ.get('PORT', 18801)
```

修改 `settings.py` 地域映射文件及日志

```python
NLP_REGIONAL_DATA_PATH = ""  # nlp 地域映射
PROJECT_LOG_FILE = ""  # 日志文件
```

### 服务设置

#### 启动

```bash
python3 run.py nlp_regional_server manage.py start
```

#### 停止

```bash
python3 run.py nlp_regional_server manage.py stop
```

#### 重启

```bash
python3 run.py nlp_regional_server manage.py restart
```

### API Demo

```python
# url
url = '127.0.0.1:18801/nlp_regional/regional'

# post data format(请求地域服务，传id、title、content) 
parms = {"id":id,"title": title, "content": content}

# 发送请求
resp = requests.post(url, data=parms)

# 获取结果
result = resp.text
```


### 目前支持
* 支持印度地区邦（联盟）、县、分区、村识别，目前提供到邦级别
* 支持印度地区35个邦和联盟区域识别，并支持5个热门城市（Delhi，Mumbai, Bengaluru, Kolkata, Hyderabad）识别
* 目前抽样地域识别准确率达到85%

### 后续优化
* 针对无明显地域名称的新闻，提供基于内容的地域识别
* 优化地域查找时间
* 优化细分地域，提供到县级新闻识别


---------------

## NLP爬虫解析服务(nlp_parser_server)


### 配置

修改 `run.py` 服务端口及ip

```python
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
SERVER_PORT = os.environ.get('PORT', 8020)
```

修改 `settings.py` 日志

```python
PROJECT_LOG_FILE = ""  # 日志文件
```

### 服务设置

#### 启动

```bash
python3 run.py nlp_parser_server manage.py start
```

#### 停止

```bash
python3 run.py nlp_parser_server manage.py stop
```

#### 重启

```bash
python3 run.py nlp_parser_server manage.py restart
```

### API Demo

```python
# url
url = 'http://127.0.0.1:8020/nlp_parser/parser'

id1 = "1502776564471413"
parser_url = "https://www.sciencedaily.com/releases/2019/02/190225123449.htm"
parms1 = {"id": id1, "website": parser_url}

# spider parser test
resp1 = requests.post(url, data=parms1)  # 发送请求
# Decoded text returned by the request
print(resp1.text)
```


### 目前支持
* 新闻html爬取、解析
* 支持130+网站的解析规则

### 后续优化
* 优化解析规则，使提取的数据更精确
* 修复旧网址失效解析规则, 增加新网址的解析规则
