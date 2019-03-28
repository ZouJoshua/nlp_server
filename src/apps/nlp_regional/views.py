from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View

from .regional_processer.load_regional_map import LoadRegionalMap
from .regional_processer.predict import Predict
from utils.logger import Logger
from web.settings import PROJECT_LOG_FILE, NLP_MODEL_PATH


logger = Logger('nlp_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
logger.info("Initialization start...")

logger.info("Loading models and idx2map...")
regional_map = LoadRegionalMap(logger=logger).load_regional_map(path=NLP_MODEL_PATH)
pred = Predict(logger=logger)


def index_view(request):
    return HttpResponse("Hello World!")

class Regional(View):
    global regional_map

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻地域分类
        :param request:
        :return: {"regional": []}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        logger.info('Successfully received the request content sent by the client {}'.format(client_host))
        text = request_data.get("content", default='')
        title = request_data.get("title", default='')
        task_id = request_data.get("id", default='')
        if text or title:
            res = pred.get_regional(content=text, title=title, classifier_dict=classifier_dict, idx2label=idx2label_map, thresholds=threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
