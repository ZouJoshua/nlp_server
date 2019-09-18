# NLP本地 Django 服务文档

本项目记录了NLP Django本地微服务相关文档，包括如下方面：

- 在本框架内新增app服务配置
- 已支持服务调用
    - 项目概况
    - 服务配置
    - 服务部署
    - 服务API Demo
- 已支持服务现状、优化方向
    - 目前情况
    - 后续优化

目前，支持如下几种服务：
- [x] NLP新闻分类服务
- [x] NLP新闻地域服务
- [x] NLP新闻爬虫解析服务
- [x] NLP新闻浏览口味服务
- [x] 视频标签服务
- [x] 视频分类映射服务
- [x] 视频理解分类服务
---------------

## 新增本地服务app

1. 增加服务app逻辑，放置在 `./apps/xxx`内

    *建议*以服务应用名称为app文件名，app目录下可以另起一个文件存放主逻辑模块

2. 配置app相关的django模块
    
    主要修改app的 `url.py`，`views.py`

3. app服务Django配置文件，放置在 `./config`内
    
    *建议*以服务应用名称识别不同app的配置文件
4. app服务相关数据文件，放置在 `./data/xxx`内
    
    *建议*以服务应用名称识别不同app的数据文件
5. 修改路由文件，配置 `./server/urls.py`
6. 修改部署文件，配置 `./run.py`
    
    新增服务名称及端口等信息
7. 相关请求demo可放置在 `./client`内

---------------
## 已支持服务概况

### NLP新闻分类服务(news_category)

>- 项目概况

爬虫服务端抓取新闻，经过nlp服务，自动为抓取文章进行分类，将文章的一级、二级分类返回，进入cms后台。

利用人工标注的一级分类、二级分类，进行数据清洗后，用fasttext算法进行文本分类。

    训练语料（人工标注数据，未整理）
    cms标注后台
    mongodb://article_repo_rw:Z5ROAsDCUwKxUFcoGtwv@content-mongodb001.apusdb.com:27060,content-mongodb002.apusdb.com:27060/article_repo.label_result
    
    训练语料（清洗整理后）
    work001：
    /data/zoushuai/handover_list/nlp_text_classification/traincorpus
    其中：
        9个分类名称对应的文件为训练语料

    模型路径（包含映射文件）
    work001：
    /data/zoushuai/handover_list/nlp_text_classification/classification_models
    其中：
        idx2label_map.json 为分类id映射文件
        top_content_model.bin 为一级分类模型
        *_sub_classification_model.bin 为二级分类模型



>- 服务配置

**服务名称**：news_category

``` python

# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口19901，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 19901) 

# 修改 news_category_conf.py 模型路径及日志
NLP_MODEL_PATH = ""     # nlp 模型数据路径(默认 ./data/news_category)
CATEGORY_LOG_FILE = ""  # 日志文件(默认 news_category_server.log)

```

>- 服务部署

- 部署方式1
``` bash
# 启动
python3 run.py news_category manage.py start

# 停止
python3 run.py news_category manage.py stop

# 重启
python3 run.py news_category manage.py restart

```
- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

``` bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)


``` python
# url
url1 = 'http://127.0.0.1:19901/nlp_category/category'
url2 = 'http://127.0.0.1:19901/nlp_category/top'
url3 = 'http://127.0.0.1:19901/nlp_category/sub'

## >>>>>>>>>> 请求一级和二级类参数
"""
请求参数（post）：
    title: string（必传）
    content: string（必传）
    thresholds: （float，float）（可不传，默认参数（0.3,0.2））
"""
# category test
parms = {"title": title, "content": content, "top_category": top_category}
resp1 = requests.post(url1, data=parms)  # 发送请求
print(resp1.text)

```

>- 现状及优化

    目前情况
    1. 一级分类达到9个类别（1个独立模型），准确率达到95%+，
    2. 二级分类达到88个类别（8个独立模型），整体准确率达到85%
    
    后续优化
    1. 优化线上模型大小，解决多个模型占内存的问题
    2. 处理尝试不同方法进行文本分类，优化准召率

---------------

### NLP新闻地域服务(news_regional)

>- 项目概况

爬虫服务端抓取新闻，经过nlp服务，自动判断文章是否属于地域性新闻（印度）。

用整理的印度行政划分，利用规则进行新闻地域的判别。

>- 服务配置

**服务名称**：news_regional

``` python
# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口18801，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 18801) 

# 修改 `news_regional_conf.py` 日志
REGIONAL_LOG_FILE = ""      # 日志文件(默认 news_regional_server.log)
```

>- 服务部署

- 部署方式1

```bash
# 启动
python3 run.py news_regional manage.py start

# 停止
python3 run.py news_regional manage.py stop

# 重启
python3 run.py news_regional manage.py restart
```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)

``` python
# url
url = '127.0.0.1:18801/nlp_regional/regional'

## >>>>>>>>>> 请求地域服务参数
"""
请求参数（post）：
    id: string or int (必传）
    title: string（必传）
    content: string（必传）
"""
# regional test 
parms = {"id":id,"title": title, "content": content}
resp = requests.post(url, data=parms)
result = resp.text
```

>- 现状及优化

    目前支持
    1. 支持印度地区邦（联盟）、县、分区、村识别，目前提供到邦级别
    2. 支持印度地区35个邦和联盟区域识别，并支持5个热门城市（Delhi，Mumbai, Bengaluru, Kolkata, Hyderabad）识别
    3. 目前抽样地域识别准确率达到85%
    
    后续优化
    1. 针对无明显地域名称的新闻，提供基于内容的地域识别
    2. 优化细分地域，提供到县级新闻识别

---------------

### NLP新闻爬虫解析服务(news_parser)

>- 项目概况

由于爬虫客户端未进行新闻tag、title等一些信息的详细抽取解析，重新进行新闻的爬取，提供所需的新闻tag等字段信息。


>- 服务配置

**服务名称**：news_parser

``` python
# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口18801，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 8020) 

# 修改 `news_parser_conf.py` 日志
PROJECT_LOG_FILE = ""  # 日志文件（默认 news_parser_server.log）
```

>- 服务部署

- 部署方式1

```bash
# 启动
python3 run.py nlp_parser_server manage.py start

# 停止
python3 run.py nlp_parser_server manage.py stop

# 重启
python3 run.py nlp_parser_server manage.py restart
```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)

``` python
# url
url = 'http://127.0.0.1:8020/nlp_parser/parser'

## >>>>>>>>>> 请求爬虫解析服务参数
"""
请求参数（post）：
    id: string（必传，打印日志）
    website: string（必传）
    lang: string(必传 "en","hi")
"""

# spider parser test
parms = {"id": id3, "website": parser_url, "lang": "en"}
resp1 = requests.post(url, data=parms)  # 发送请求
print(resp1.text)
```

>- 现状及优化

    目前支持
    1. 新闻html爬取、解析
    2. 支持印度英语130+主域名网站的解析规则
    3. 支持印地语60+主域名网站的解析规则，覆盖到历史400W+新闻的80%+的网址
    
    后续优化
    1. 优化解析规则，使提取的数据更精确
    2. 修复旧网址失效解析规则, 增加新网址的解析规则


------------------


### NLP新闻浏览口味服务(news_taste)

>- 项目概况

爬虫服务端抓取新闻，经过nlp服务，自动判断文章的浏览口味，返回文章的浏览口味，提供到cms后台。

利用人工标注的新闻数据，进行数据清洗后，用fasttext算法进行模型训练，进而进行文本分类。

    训练语料（人工标注数据，未整理）
    hdfs:
    /user/hive/warehouse/apus_ai.db/recommend/common/news_emotion_region_taste_timeliness
    
    训练语料（清洗整理后）
    work001：
    /data/zoushuai/handover_list/nlp_text_classification/traincorpus
    其中：
        taste_corpus 为浏览口味训练语料

    模型路径（包含映射文件）
    work001：
    /data/zoushuai/handover_list/nlp_text_classification/taste_models
    其中：
        idx2label_map.json 为分类id映射文件
        taste_classification_model.bin 为浏览口味分类模型


>- 服务配置

**服务名称**：news_taste

``` python

# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口19901，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 16601) 

# 修改 news_category_conf.py 模型路径及日志
NLP_MODEL_PATH = ""     # nlp 模型数据路径(默认 ./data/news_taste)
CATEGORY_LOG_FILE = ""  # 日志文件(默认 news_taste_server.log)

```

>- 服务部署

- 部署方式1
```bash
# 启动
python3 run.py news_taste manage.py start

# 停止
python3 run.py news_taste manage.py stop

# 重启
python3 run.py news_taste manage.py restart

```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)


``` python
# url
url1 = 'http://127.0.0.1:16601/nlp_category/taste'


## >>>>>>>>>> 请求一级和二级类参数
"""
传入参数：
    id: string(必传)
    title: string（必传）
    content: string（必传）
    thresholds: float（可不传，默认参数0.3）
"""
# category test
parms = {"id": _id, "title": title, "content": content, "thresholds": 0.3}
resp1 = requests.post(url1, data=parms)  # 发送请求
print(resp1.text)

```

>- 现状及优化

    目前情况
    1. 目前支持新闻浏览口味4种，准确率达到85%，
    2. 目前模型使用fasttext模型
    
    
    后续优化
    1. 支持深度学习模型，如textcnn、rnn、bert等


-----------------

### 视频标签服务(video_tags)

>- 项目概况

爬虫服务端抓取的视频，经过nlp服务，从视频相关的文本信息中抽取视频tag，作为推荐召回的特征。



>- 服务配置

**服务名称**：video_tags

``` python

# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口9022，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 9022) 

# 修改 video_tags_conf.py 模型路径及日志
NLP_MODEL_PATH = ""     # nlp 模型数据路径(默认 ./data/video_tags)
PROJECT_LOG_FILE = ""  # 日志文件(默认 video_tags_server.log)

```

>- 服务部署


- 部署方式1
```bash
# 启动
python3 run.py video_tags manage.py start

# 停止
python3 run.py video_tags manage.py stop

# 重启
python3 run.py video_tags manage.py restart

```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```

>- 服务API Demo(参见client)


``` python
# url
url1 = 'http://127.0.0.1:9022/polls/vtag'


## >>>>>>>>>> 请求参数
"""
传入参数：
    newsid: string(必传)
    title: string（必传）
    vtaglist: string（必传）
    content: string（必传）
    lang: string(必传)
    category: string()
    sub_category: string()
    resource_type: string(0：文章 1：视频)
    business_type: string(0:浏览器 1:游戏)
"""
# category test
parms = {"newsid": _id, "lang": lang, "title": title, "vtaglist": vtaglist, "content": content, "category": category, "business_type":business_type,"resource_type":resource_type}
resp1 = requests.post(url1, data=parms)  # 发送请求
print(resp1.text)

```

>- 现状及优化

    目前情况
    1. 目前英语、西班牙语、葡萄牙语（巴西）、德语、韩语、俄罗斯语的视频tag的处理及抽取
    2. 目前各语言基本tag统计
        英语：16大类
        西班牙语： 690
        葡萄牙语： 9440
        德语： 510
        韩语： 1310
        俄罗斯语： 7200
        日语： 4200
    
    
    后续优化
    1. 优化各语种的tag处理

----------

### 视频分类映射服务(video_category)

>- 项目概况

对视频分类，利用原始分类信息，配置运营团队自己的分类体系，将二级分类为-1的映射出对应的二级分类id。

>- 服务配置

**服务名称**：video_category

``` python
# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口17701，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 17701) 

# 修改定时更新文件映射文件
CRONJOBS = [] # crontab定时任务（默认 2小时更新）

# 修改 video_category_conf.py 日志
CRONJOBS_LOG_FILE = ""  # 定时日志文件（默认 crontab.log）
PROJECT_LOG_FILE = ""  # 日志文件（默认 video_category_server.log）
```

>- 服务部署

- 部署方式1

```bash
# 启动
python3 run.py video_category manage.py start
## 添加定时任务（加载映射文件）
python3 manage.py crontab add

# 停止
## 停止定时任务
python3 manage.py crontab remove
python3 run.py video_category manage.py stop

# 重启
python3 run.py video_category manage.py restart
```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)

``` python
# url
url1 = 'http://127.0.0.1:17701/nlp_category/v_category'

## >>>>>>>>>> 请求视频分类服务参数
"""
请求参数（post）：
    newsid: string(必传)
    title: string（必传）
    content: string（必传）
    category: string()
    sub_category: string()
    resource_type: string(0：文章 1：视频)
    business_type: string(0:浏览器 1:游戏)
    
"""
# video category test
parms = {"newsid": _id, "title": title, "content": content, "category": top_category, "sub_category":sub_category, "business_type":business_type,"resource_type":resource_type}
resp1 = requests.post(url1, data=parms)
result = resp1.text
```

>- 现状及优化

    目前支持
    1. 将二级分类为-1的映射出对应的二级分类id
    2. 每两个小时更新一次映射文件
    
    后续优化
    1.视频分类模型

--------------

### 视频理解分类服务(video_classification)

>- 项目概况

基于YouTube8M数据集，利用人工标注的视频帧的特征及label进行视频标签的在线分类。

    模型路径
    work001：
    特征抽取模型： /data/zoushuai/handover_list/nlp_video_classification/classification_models/preprocess_models（解压模型文件到在线服务对应路径）
    分类预测模型： /data/zoushuai/handover_list/nlp_video_classification/classification_models/models（解压模型文件到在线服务对应路径）
    分类id映射文件：/data/zoushuai/handover_list/nlp_video_classification/classification_models/models/vocabulary.csv


>- 服务配置

**服务名称**：video_classification

``` python

# 修改 run.py 服务ip及端口
server_host= "127.0.0.1"
# 默认端口19901，如需修改修改 set_environ()
server_port = os.environ.get('PORT', 17001) 

# 修改 video_classification_conf.py 模型路径及日志
NLP_PREP_MODEL_PATH = ""     # 视频特征抽取模型数据路径(默认 ./data/video_classification/preprocess_model)
NLP_MODEL_PATH = ""          # 视频预测模型数据路径（默认 ./data/video_classification/model）
PROJECT_LOG_FILE = ""  # 日志文件(默认 video_classification_server.log)

```

>- 服务部署

- 部署方式1
```bash
# 启动
python3 run.py video_classification manage.py start

# 停止
python3 run.py video_classification manage.py stop

# 重启
python3 run.py video_classification manage.py restart

```

- 部署方式2(提前修改run.sh文件，注释不需启动的服务)

```bash
# 启动
sh run.sh start

# 停止
sh run.sh stop

# 重启
sh run.sh restart

```


>- 服务API Demo(参见client)


``` python
# url
url1 = 'http://127.0.0.1:17001/nlp_category/video_cats'


## >>>>>>>>>> 请求参数
"""
传入参数：
    video_id: string(必传)
    video_url: string（必传）
"""
# category test
parms = {"video_id": _id, "video_url": url}
resp1 = requests.post(url1, data=parms)  # 发送请求
print(resp1.text)

```

>- 现状及优化

    目前情况
    1. 基于YouTube8M标注数据，利用深度学习tensorflow 模型进行基于视频内容的打标签服务，
    目前可识别视频5分钟以内的短视频，基于视频帧进行特征提取，并利用tensorflow模型进行线上
    分类预测，可支持多达3862个分类
    2. 目前模型使用第二届YouTube8M视频理解挑战赛冠军模型，模型综合评分达到84%+
    3. 3分钟+的视频特征抽取在50s左右，特征预测在10s左右
    
    
    后续优化
    1. 缩短线上视频特征抽取及视频内容标签预测时间
    2. 支持并行视频帧特征抽取
