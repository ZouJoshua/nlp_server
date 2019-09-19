#!/usr/bin/env bash

start(){
echo "第一个参数为 $1 !"
#python run.py news_category manage.py start
#python run.py news_regional manage.py start
#python run.py news_parser manage.py start
#python run.py news_taste manage.py start
#python run.py video_category manage.py start
#python run.py video_browser_category manage.py start
#python run.py video_tags manage.py start
python run.py video_classification manage.py start

}

stop(){
#python run.py news_category manage.py stop
#python run.py news_regional manage.py stop
#python run.py news_parser manage.py stop
#python run.py news_taste manage.py stop
#python run.py video_category manage.py stop
#python run.py video_browser_category manage.py stop
#python run.py video_tags manage.py stop
python run.py video_classification manage.py stop
}

restart(){
#python run.py news_category manage.py restart
#python run.py news_regional manage.py restart
#python run.py news_parser manage.py restart
#python run.py news_taste manage.py restart
#python run.py video_category manage.py restart
#python run.py video_browser_category manage.py restart
#python run.py video_tags manage.py restart
python run.py video_classification manage.py restart
}

case "$1" in
'start')
start
;;
'stop')
stop
;;
'restart')
restart
;;
*)
echo "Usage: $0 {start|stop|restart}"
exit 1
esac
exit 0