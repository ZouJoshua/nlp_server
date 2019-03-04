from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View
import datetime
from .classification.load_model import LoadModel
from .classification.predict import Predict

from utils.logger import Logger
from web.settings import PROJECT_LOG_FILE, NLP_MODEL_PATH


logger = Logger('nlp_category_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()

classifier_dict, idx2label_map = LoadModel(logger=logger).load_models_and_idmap(path=NLP_MODEL_PATH)
logger.info("Loading models and idx2map...")

pred = Predict(logger=logger)

# Create your views here.

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
        :return:
        """
        # data = {"title": "", "content": ""}
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
        :return:
        """
        data = {"title": "", "content": ""}  # 返回给客户端的数据
        # print(request.POST)  # 查看客户端发来的请求内容
        return JsonResponse(data)  # 通过 django内置的Json格式 丢给客户端数据


class SubCategory(View):
    global classifier_dict
    global idx2label_map

    def get(self, request):
        pass

    def post(self, request):
        """
        只返回新闻二级分类
        :param request:
        :return:
        """
        data = {"topcategory": "xxx", "title": "", "content": ""}
        return JsonResponse(data)  # 通过 django内置的Json格式 丢给客户端数据
