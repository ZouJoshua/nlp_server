from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View

from .classification.load_model import LoadModel
from .classification.predict import Predict
from utils.logger import Logger
from config.video_browser_category_conf import PROJECT_LOG_FILE, NLP_MODEL_PATH



logger = Logger('nlp_v_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
logger.info("Initialization start...")
logger.info("Loading models and idx2map...")
classifier_dict, idx2label_map = LoadModel(logger=logger).load_models_and_idmap(path=NLP_MODEL_PATH)
pred = Predict(logger=logger)


def index_view(request):
    return HttpResponse("Hello World!")

class Category(View):
    global classifier_dict
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
        tag = request_data.get("tag_list", default='')
        threshold = request_data.get("thresholds", default=(0.3, 0.2))

        if text or title:
            res = pred.get_category(title=title, content=text, tags=tag, classifier_dict=classifier_dict, idx2label=idx2label_map,
                                    thresholds=threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
