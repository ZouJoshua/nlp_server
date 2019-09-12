from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View

from .predict.predict_main import Predict
from utils.logger import Logger
from config.video_classification_conf import PROJECT_LOG_FILE



logger = Logger('nlp_v_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
logger.info("Initialization start...")
logger.info("Loading tensorflow models and idx2map...")
logger.info("Successfully cache idx2map")
pred = Predict(logger=logger)


def index_view(request):
    return HttpResponse("Hello World!")

class Category(View):
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        返回视频分类
        :param request:
        :return: {"top_category": [{"id":"","category":"","proba":""}],
                "sub_category": [{"id":"","category":"","proba":""}]}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        task_id = request_data.get("newsid", default='')
        logger.info('Successfully received task_id {} sent by the client {}'.format(task_id, client_host))
        video_url = request_data.get("url", default='')
        res = pred.get_category(top_c=top, sub_c=sub, idx2label=idx2label_map)
        if res == {"top_category": [{"id": top, "category": "", "proba": 0.0}],
                                "sub_category": [{"id": sub, "category": "", "proba": 0.0}]}:
            result["status"] = 'Error'
            result["result"] = res
            logger.error("No classification found in the mapping table")
        else:
            result["status"] = 'Successful'
            result["result"] = res
            logger.info("Successfully resolved classification")

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
