import json
import os
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views import View

from .classification.load_process_instance import LoadMultiCountryTagInstance

from utils.logger import Logger
from config.video_tags_conf import PROJECT_LOG_FILE, NLP_MODEL_PATH

logger = Logger('nlp_v_tags_process', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
lang_list = ["en", "es", "ko", "de", "pt"]
lmc = LoadMultiCountryTagInstance(lang_list, logger=logger)
multi_lang_instance_dict = lmc.load_process_instance()


def index_view(request):
    return HttpResponse("Hello World!")

class Category(View):
    global en_proc, es_proc, normal_proc

    def get(self, request):
        pass

    def post(self, request):
        """
        返回视频分类
        :param request:
        :return: "tag1\ttag2\ttag3"
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
        lang = request_data.get("lang", default="en")
        # topn = request_data.get("topn", default="")
        # category = request_data.get("category", default="")
        # resource_type = request_data.get("resource_type", default="")
        # source_url = request_data.get("source_url", default="")
        # business_type = request_data.get("business_type", default="")

        requestjson = json.dumps(request_data, ensure_ascii=False)

        logger.info("Request:" + requestjson)
        if title.strip() == '' and vtaglist.strip() == '':
            logger.info("Response:Title is empty, vtaglist is empty")
            return HttpResponse("")

        nlp_vtag = VtagProcess(title, text, lang, vtaglist).nlp_vtag
        tagresult = '\t'.join(nlp_vtag)
        if tagresult == None:
            tagresult = ''
        logger.info("Processed vtag 【{}】".format(tagresult))

        return HttpResponse(tagresult)



class VtagProcess(object):

    def __init__(self, title, content, lang, taglist):
        self.title = title
        self.content = content
        self.lang = lang.lower()
        self.taglist = taglist
        self.nlp_vtag = self.nlp_vtag_process()

    def nlp_vtag_process(self):
        tag_list = self.taglist.split(',')
        lang_instance = "{}_instance".format(self.lang)
        if lang_instance in multi_lang_instance_dict:
            if self.lang == "en":
                lang_process = multi_lang_instance_dict[lang_instance]
            elif self.lang == 'es':
                lang_process = multi_lang_instance_dict[lang_instance]
            elif self.lang == 'ko':
                lang_process = multi_lang_instance_dict[lang_instance]
            elif self.lang == 'de':
                lang_process = multi_lang_instance_dict[lang_instance]
                # print(lang_process)
            elif self.lang == 'pt':
                lang_process = multi_lang_instance_dict[lang_instance]
            else:
                lang_process = multi_lang_instance_dict[lang_instance]
        else:
            lang_process = multi_lang_instance_dict[lang_instance]

        if self.lang in lang_list:
            nlp_vtagres = lang_process.get_cleaned_tags(self.title, tag_list)
            logger.debug("Successfully process {} tag 【{}】".format(self.lang, nlp_vtagres))
            if len(nlp_vtagres) == 0:
                logger.info("the tag was not extracted from the taglist and is being extracted from the title and text")
                nlp_vtagres = lang_process.extract_tag(self.title, self.content)
        else:
            nlp_vtagres = lang_process.get_cleaned_tags(tag_list)

        return nlp_vtagres
