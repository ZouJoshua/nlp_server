#!/usr/bin/env bash


if [ $# != 1 ] ; then
echo "Usage: $0 {news_category|news_regional|news_parser|news_taste|video_tags|video_category|video_classification}"
exit 1;
fi



stop(){
echo "支持如下服务：
      项目名称        |     ServerName
    --------------------------------------
    NLP新闻分类服务    | news_category
    NLP新闻地域服务    | news_regional
    NLP新闻爬虫解析服务 | news_parser
    NLP新闻浏览口味服务 | news_taste
    视频标签服务       | video_tags
    视频分类映射服务    | video_category
    视频理解分类服务    | video_classification
    ---------------------------------------"

echo "请关闭指定服务，传入对应 ServerName..."
echo "正在关闭服务 " $1

if [ $1 = "video_category" ];then
  python run.py $1 manage.py stop
  python manage.py crontab remove
else
  python run.py $1 manage.py stop
fi
}


stop $1

