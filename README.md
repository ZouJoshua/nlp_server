# nlp_category_server
NLP分类服务

## 配置

修改 run.py

```python
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
```

修改 settings.py

```python
NLP_MODEL_PATH = ""  # nlp 模型路径
PROJECT_LOG_FILE = ""  # 日志文件
```

## 服务设置

### 启动

```bash
python3 run.py manage.py {port} start
```

### 停止

```bash
python3 run.py manage.py {port} stop
```

### 重启

```bash
python3 run.py manage.py {port} restart
```

## API

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

# nlp_regional_server
NLP地域服务


## 配置

修改 run.py

```python
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
SERVER_PORT = os.environ.get('PORT', 18801)
```

修改 settings.py

```python
NLP_REGIONAL_DATA_PATH = ""  # nlp 地域映射
PROJECT_LOG_FILE = ""  # 日志文件
```

## 服务设置

### 启动

```bash
python3 run.py nlp_regional_server manage.py start
```

### 停止

```bash
python3 run.py nlp_regional_server manage.py stop
```

### 重启

```bash
python3 run.py nlp_regional_server manage.py restart
```

## API

```python
# url
url = 'http://127.0.0.1:18801/nlp_regional/regional'

# post data format(请求地域服务，传id、title、content) 
parms = {"id":id,"title": title, "content": content}

# 发送请求
resp = requests.post(url, data=parms)

# 获取结果
result = resp.text
```
