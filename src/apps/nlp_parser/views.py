from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views import View


class SpiderParser(View):
    global pred

    def get(self, request):
        pass

    def post(self, request):
        """
        返回新闻地域分类
        :param request:
        :return: {"regional": ["Odisha",""]}
        """
        result = dict()
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        text = request_data.get("content", default='')
        title = request_data.get("title", default='')
        task_id = request_data.get("id", default='')
        logger.info('Successfully received the task_id {} sent by the client {}'.format(task_id, client_host))
        if text or title:
            res = pred.get_regional_multithread(content=text, title=title)
            # res = pred.get_regional(content=text, title=title)
            result["status"] = 'Successful'
        else:
            res = dict()
            result["status"] = 'Error'
            logger.warming('User-delivered content and title fields were not found.')
        result["result"] = res

        return JsonResponse(result)  # 通过 django内置的Json格式 丢给客户端数据
