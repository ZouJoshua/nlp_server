from django.test import TestCase

# Create your tests here.

from unittest import main, TestCase
import time
from .regional_processer.load_regional_map import LoadRegionalMap
from .regional_processer.predict import Predict

NLP_REGIONAL_FILE_PATH = r'/home/zoushuai/algoproject/nlp_server/src/data/india_names2regions.json'
regional_map = LoadRegionalMap().load_regional_map(path=NLP_REGIONAL_FILE_PATH)
pred = Predict(regional_map=regional_map)


class TestPredict(TestCase):
    # id = "1502889409622478"
    title = "2 kids die in different incidents"
    content = """Erode, Aug 16 (PTI) A three-year-old child died in a road accident, while a 11-month-old was electrocuted while playing in his house at suburban Karungalpalayam in two different incidents in the district, police said. they said the 3-year-old male child died on the spot when he was thrown off after a college van rammed the motorcycle he was travelling with his parents from the rear at Bhavani Both the husband and wife were seriously injured and have been hospitalised. In the second incident late last night,the 11 month child accidentally came in contact with a live wire, attached to the television. The parents rushed him to a private nursing home from where he was referred to Government Headquarters Hospital late last night, but the toddler died, police said. This is published unedited from the PTI feed."""

    @classmethod
    def setUpClass(cls):
        print(">>>>>>>>>>测试环境已准备好！")
        print(">>>>>>>>>>即将测试 Case ...")

    @classmethod
    def tearDownClass(cls):
        print(">>>>>>>>>>Case 用例已测试完成 ...")
        print(">>>>>>>>>>测试环境已清理完成！")

    def test_time_use(self):
        s = time.time()
        text = self.content + '.' + self.title
        out_count = pred.get_detail_regional(text, regional_map)
        s1 = time.time()
        print(">>>>>>>>>>查找地域耗时： {}".format(s1 - s))
        regional_ct = pred._count_regional(out_count, regional_map)
        s2 = time.time()
        print(">>>>>>>>>>地域统计耗时： {}".format(s2 - s1))
        result = pred._get_regional(regional_ct, text)
        e = time.time()
        print(">>>>>>>>>>分地域耗时： {}".format(e - s2))

        print(">>>>>>>>>>查找结果 {}\n 总体耗时： {}".format(result, e - s))

    def test_multithread_time_use(self):
        s = time.time()
        text = self.content + '.' + self.title
        out_count = pred._find_regional_multithread(text, regional_map)
        s1 = time.time()
        print(">>>>>>>>>>查找地域耗时： {}".format(s1 - s))
        regional_ct = pred._count_regional(out_count, regional_map)
        s2 = time.time()
        print(">>>>>>>>>>地域统计耗时： {}".format(s2 - s1))
        result = pred._get_regional(regional_ct, text)
        e = time.time()
        print(">>>>>>>>>>分地域耗时： {}".format(e - s2))

        print(">>>>>>>>>>查找结果 {}\n 总体耗时： {}".format(result, e - s))

if __name__ == '__main__':
    main()