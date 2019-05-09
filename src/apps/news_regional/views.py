from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View

from .regional_processer.load_regional_map import LoadRegionalMap
from .regional_processer.predict import Predict
from utils.logger import Logger
from config.news_regional_conf import REGIONAL_LOG_FILE, NLP_REGIONAL_DATA_PATH
import os

logger = Logger('nlp_regional_predict', log2console=False, log2file=True, logfile=REGIONAL_LOG_FILE).get_logger()
logger.info("Initialization start...")

logger.info("Loading regional map...")
NLP_REGIONAL_FILE_PATH = os.path.join(NLP_REGIONAL_DATA_PATH, 'india_names2regions.json')
regional_map = LoadRegionalMap(logger=logger).load_regional_map(path=NLP_REGIONAL_FILE_PATH)
pred = Predict(regional_map=regional_map, logger=logger)


def index_view(request):
    return HttpResponse("Hello World!")

class Regional(View):
    global pred

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻地域分类
        :param request:
        :return: {"status": "Successful", result:{"name":"Odisha", "prob":1.0}}
                    {"status": "Error", "result":{"name": "unknown", "prob": 1.0}}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        text = request_data.get("content", default='')
        title = request_data.get("title", default='')
        task_id = request_data.get("newsid", default='NoID')
        logger.info('Successfully received the task_id {} sent by the client {}'.format(task_id, client_host))
        if text or title:
            res = pred.get_regional(content=text, title=title)
            # res = pred.get_regional(content=text, title=title)
            result["status"] = 'Successful'
        else:
            res = {"name": "unknown", "prob": 1.0}
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据