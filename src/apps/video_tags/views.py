import json
import os
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View

from .classification.en_vtag_process import EnProcess
from .classification.load_mapdata import LoadDict
from utils.logger import Logger
from config.video_tags_conf import PROJECT_LOG_FILE, NLP_MODEL_PATH



logger = Logger('nlp_v_tags_predict', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
logger.info("Initialization start...")
logger.info("Loading models and idx2map...")
vtags_file = os.path.join(NLP_MODEL_PATH, 'vtags.0413')
trim_file = os.path.join(NLP_MODEL_PATH, 'trim2')
stopwords_file = os.path.join(NLP_MODEL_PATH, 'stopwords.txt')
ld = LoadDict(vtags_file, trim_file, stopwords_file)
vtag2kwline = ld.en_vtag2kwline
fix2list = ld.en_fix2list
word2fix = ld.en_word2fix
kw2vtag = ld.en_kw2vtag
stopwords = ld.stopwords
logger.info("Successfully cache idx2map")
pred = EnProcess(vtag2kwline, fix2list, word2fix, kw2vtag, stopwords, logger=logger)


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
        request_meta = request.META
        client_host = request_meta['HTTP_HOST']
        request_data = request.POST  # 查看客户端发来的请求内容
        request_info = {}
        task_id = request_data.get("newsid", default="")
        logger.info('Successfully received task_id {} sent by the client {}'.format(task_id, client_host))
        title = request_data.get("title", default="")
        text = request_data.get("content", default="")
        vtaglist = request_data.get("vtaglist", default="")
        topn = request_data.get("topn", default="")
        category = request_data.get("category", default="")
        resource_type = request_data.get("resource_type", default="")
        source_url = request_data.get("source_url", default="")
        business_type = request_data.get("business_type", default="")

        requestjson = json.dumps(request_data, ensure_ascii=False)

        logger.info("Request:" + requestjson)
        if title.strip() == '' and vtaglist.strip() == '':
            logger.info("Response:Title is empty, vtaglist is empty")
            return HttpResponse("")

        taglist = vtaglist.split(',')

        nlp_vtagres, resultdict = pred.process_vtag(title, taglist)
        if len(nlp_vtagres) == 0:
            nlp_vtagres = pred.extract_tag(title, text)

        tagresult = '\t'.join(nlp_vtagres)
        if tagresult == None:
            tagresult = ''

        request_info['nlp_vtag'] = nlp_vtagres
        result = {}
        result['nlp_vtag'] = nlp_vtagres
        responsejson = json.dumps(request_info, ensure_ascii=False)

        # responseinfo = "Title["+title+"],Oldtaglist["+vtaglist+"], Vtag_result["+tagresult+']'
        # print(loginfo)
        # print(responsejson)
        logger.info("Response:" + responsejson)
        return HttpResponse(tagresult)



class VtagProcess(object):

    def __init__(self, title, content, lang, taglist):
        self.title = title
        self.content = content
        self.lang = lang.lower()
        self.taglist = taglist
        self.nlp_vtag = list()

    def nlp_vtag_process(self):
        taglist = self.taglist.split(',')
        if self.lang == "en":
            nlp_vtagres, resultdict = pred.process_vtag(self.title, taglist)
            if len(nlp_vtagres) == 0:
                nlp_vtagres = pred.extract_tag(self.title, self.content)
        elif self.lang == 'es':
            pass
        else:
            pass


