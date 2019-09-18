from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View
import json



from .predict.predict_main import Predict, load_flags_config, load_idxmap
from .predict.extract_feature_main import ExtractFeature
from utils.logger import Logger
from config.video_classification_conf import PROJECT_LOG_FILE


def init():
    logger = Logger('video_classification_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
    logger.info("Initialization start...")
    logger.info("Loading tensorflow models and idx2map...")
    flags = load_flags_config()
    logger.info("Successfully load tensorflow flags")
    idxmap = load_idxmap(flags.vocabulary_file)
    logger.info("Successfully cache idx2map")
    ef = ExtractFeature(flags, logger=logger)
    p = Predict(flags, logger=logger)

    return logger, ef, p, idxmap

log, ef, p, idxmap = init()

def index_view(request):
    return HttpResponse("Hello World!")

class Category(View):
    global ef, p, idxmap

    def get(self, request):
        pass

    def post(self, request):
        """
        返回视频分类
        :param request:
        :return: {"video_cats": [{"id":"","category":"","proba":""}]}
        """
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        task_id = request_data.get("video_id", default='')
        log.info('Successfully received task_id {} sent by the client {}'.format(task_id, client_host))
        video_url = request_data.get("video_url", default='')
        feature = ef.extract(video_url)
        log.info("Successfully encoded video")
        p.predict(feature, idxmap)
        if p.out:
            result = p.out[0]
        else:
            result = dict()
            log.info("Error with predict of video {}".format(video_url))

        return JsonResponse(result, safe=False)
        # return HttpResponse(json.dumps(result),content_type="application/json",charset="utf-8")
