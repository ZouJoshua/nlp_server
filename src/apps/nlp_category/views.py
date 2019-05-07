from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View

from .classification.predict import Predict
from utils.logger import Logger
from web.settings import PROJECT_LOG_FILE
from .classification.crontab_load_idxlabel import crontab_load


logger = Logger('nlp_v_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
logger.info("Initialization start...")
logger.info("Loading models and idx2map...")
idx2label_map = crontab_load()
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
        title = request_data.get("title", default='')
        text = request_data.get("content", default='')
        top = request_data.get("category", default='')
        sub = request_data.get("sub_category", default='')
        r_type = request_data.get("resource_type", default='1')
        b_type = request_data.get("business_type", default='0')
        # idx2label_map = cache.get("IDX2LABEL_MAP")
        res = pred.get_category(top_c=top, sub_c=sub, idx2label=idx2label_map)
        if res == {"top_category": [{"id": top, "category": "", "proba": 0.0}],
                                "sub_category": [{"id": sub, "category": "", "proba": 0.0}]}:
            res = dict()
            result["status"] = 'Error'
            result["result"] = res
            logger.error("No classification found in the mapping table")
        else:
            result["status"] = 'Successful'
            result["result"] = res
            logger.info("Successfully resolved classification")

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
