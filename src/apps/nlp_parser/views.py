from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View

from .parser_processer.user_agents import user_agent_list
import random
from .start import init_start

rules_xpath, hd, hp, logger = init_start()


def get_http_header():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(user_agent_list)['User-Agent']
    }



class SpiderParser(View):
    global rules_xpath, hd, hp, logger

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻爬虫解析结果
        :param request: {"id":"","website":""}
        :return: {"category": [], "title": [], "tag": [],
                    "hyperlink_text": [], "hyperlink_url": []}

        """
        _result = {"category": [], "title": [], "tag": [], "hyperlink_text": [], "hyperlink_url": []}
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        url = request_data.get("website", default='')
        task_id = request_data.get("id", default='')
        logger.info('Successfully received the task_id {} sent by the client {}'.format(task_id, client_host))
        header = get_http_header()
        html = hd.download(url, header)
        if html == "timeout":
            return HttpResponse(status=408)
        elif html == "Others error":
            return JsonResponse(_result)
        else:
            result = hp.parse(url, html, rules_xpath)
            return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
