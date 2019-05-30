from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View

from .classification.load_model import LoadModel
from .classification.predict import Predict
from utils.logger import Logger
from config.news_taste_conf import CATEGORY_LOG_FILE, NLP_MODEL_PATH


logger = Logger('nlp_category_predict', log2console=False, log2file=True, logfile=CATEGORY_LOG_FILE).get_logger()
logger.info("Initialization start...")

logger.info("Loading models and idx2map...")
model, idx2label_map = LoadModel(logger=logger).load_models_and_idmap(path=NLP_MODEL_PATH)
pred = Predict(logger=logger)


def index_view(request):
    return HttpResponse("Hello World!")

class TasteCategory(View):
    global model
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻分类
        :param request:
        :return: {"taste_category":
                        [{"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""}]}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        task_id = request_data.get("id", default='NOID')
        logger.info('Successfully received the task_id {} sent by the client {}'.format(task_id, client_host))
        text = request_data.get("content", default='')
        title = request_data.get("title", default='')
        threshold = float(request_data.get("thresholds", default=0.3))
        if text or title:
            res = pred.get_category(content=text, title=title, model=model, idx2label=idx2label_map, thresholds=threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据

