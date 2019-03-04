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



class Category(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻分类
        :param request:
        :return: {"top_category_id":"","top_category":"","top_category_proba":"",
                    "sub_category_id":"", "sub_category":"","sub_category_proba":""}
        """
        print(request.POST)  # 查看客户端发来的请求内容
        print(type(request.POST))
        text = "xxxxx"
        title = "test"
        res = pred.get_category(content=text, title=title, classifier_dict=classifier_dict, idx2label=idx2label_map)
        return JsonResponse(res)  # 通过 django内置的Json格式 丢给客户端数据

class TopCategory(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        只返回新闻一级分类
        :param request:
        :return:{"top_category_id":"","top_category":"","top_category_proba":""}
        """
        print(request.POST)  # 查看客户端发来的请求内容
        title = ""
        content = ""
        content_list = []
        content_list.append(pred.clean_string(title + '.' + content))
        res = pred.get_topcategory(content_list=content_list, classifier_dict=classifier_dict, idx2label=idx2label_map)
        return JsonResponse(res)  # 通过 django内置的Json格式 丢给客户端数据


class SubCategory(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        只返回新闻二级分类
        :param request:
        :return: {"top_category":"", "sub_category_id":"", "sub_category":"","sub_category_proba":""}
        """

        title = ""
        content = ""
        top_category = ""
        content_list = []
        content_list.append(pred.clean_string(title + '.' + content))
        if top_category in classifier_dict:
            classifier = classifier_dict[top_category]
            res = pred.get_subcategory(content_list=content_list, classifier=classifier, idx2label=idx2label_map)
        else:
            res = dict()
            logger.warming('There is no model for this secondary classification {}'.format(top_category))

        return JsonResponse(res)  # 通过 django内置的Json格式 丢给客户端数据
