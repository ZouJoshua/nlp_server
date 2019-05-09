from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View

from .classification.load_model import LoadModel
from .classification.predict import Predict
from utils.logger import Logger
from web.settings import PROJECT_LOG_FILE, NLP_MODEL_PATH


logger = Logger('nlp_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
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
        返回新闻分类
        :param request:
        :return: {"top_category":
                        [{"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""}]
                        },
                "sub_category":
                        [{"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""}]
                        }
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        logger.info('Successfully received the request content sent by the client {}'.format(client_host))
        text = request_data.get("content", default='')
        title = request_data.get("title", default='')
        threshold = request_data.get("thresholds", default=(0.3, 0.2))
        if text or title:
            res = pred.get_category(content=text, title=title, classifier_dict=classifier_dict, idx2label=idx2label_map, thresholds=threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据

class TopCategory(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        只返回新闻一级分类
        :param request:
        :return:{"top_category":
                        [{"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""}]
                    }}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        logger.info('Successfully received the request content sent by the client {}'.format(client_host))
        title = request_data.get("title", default='')
        text = request_data.get("content", default='')
        top_threshold = request_data.get("thresholds", default=0.3)
        content_list = []
        content_list.append(pred.clean_string(title + '.' + text))
        if content_list:
            res = pred.get_topcategory(content_list=content_list, classifier_dict=classifier_dict, idx2label=idx2label_map, threshold=top_threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据


class SubCategory(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        只返回新闻二级分类
        :param request:
        :return: {"sub_category":
                        [{"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""},
                        {"id":"","category":"","proba":""}]
                        }
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        logger.info('Successfully received the request content sent by the client {}'.format(client_host))
        title = request_data.get("title", default='')
        text = request_data.get("content", default='')
        top_category = request_data.get("top_category", default='')
        sub_threshold = request_data.get("thresholds", default=0.2)
        content_list = []
        content_list.append(pred.clean_string(title + '.' + text))
        if top_category in classifier_dict.keys():
            classifier = classifier_dict[top_category]
            res = pred.get_subcategory(content_list=content_list, classifier=classifier, idx2label=idx2label_map, predict_res=None, threshold=sub_threshold)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('There is no model for this secondary classification {}'.format(top_category))
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据



def my_decorator(view_func):
    """
    定义装饰器，装饰类视图
    :param view_func: 被装饰的视图函数
    :return: wrapper，装饰的结果
    """
    def wrapper(request, *args, **kwargs):
        print('装饰器被调用了')
        print(request.method, request.path)

        # 调用给装饰的视图函数
        return view_func(request, *args, **kwargs)
    return wrapper
