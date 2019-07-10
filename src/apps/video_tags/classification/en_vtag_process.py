#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/4 12:26
@File    : predict.py
@Desc    : 印度英语视频tag处理
"""

from pyquery import PyQuery
import re
import logging
import json
import requests
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree




class EnProcess(object):

    def __init__(self, vtag2kwline, fix2list, word2fix, kw2vtag, stopwords, logger=None):
        self.fix2list = fix2list
        self.vtag2kwline = vtag2kwline
        self.kw2vtag = kw2vtag
        self.stopwords = stopwords
        self.word2fix = word2fix
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)

    def process_vtag(self, title, taglist):
        self.log.info("process video tag of taglist")
        newtaglist = []
        # 保留tf>=5的tag
        resultdict = {}
        oldtagdict = {}

        title_lower = title.lower()
        tmp_title = ''
        tmp_title2 = ''
        old_tagdeleteset = set()
        for vtag in taglist:
            vtag = vtag.lower()
            token = vtag.split(' ')
            if len(token) == 1:
                tmp_title2 += vtag + ' '
                if title_lower.find(tmp_title2.strip()) >= 0:
                    tmp_title = tmp_title2
                    old_tagdeleteset.add(vtag)
                    continue
                else:
                    break
            else:
                break
        taglist2 = []
        if tmp_title != '' and len(tmp_title.strip().split(' ')) >= 2:
            # print(title_lower)
            # print(tmp_title.strip())
            for vtag in taglist:
                vtag = vtag.lower()
                if vtag not in old_tagdeleteset:
                    taglist2.append(vtag)
        else:
            taglist2 = taglist

        taglist = taglist2
        for vtag in taglist:
            vtag = vtag.lower()
            if vtag.endswith('video') or vtag.endswith('song') or vtag.endswith('movie') or vtag.endswith('show'):
                vtag = vtag + 's'
            if vtag not in oldtagdict:
                oldtagdict[vtag] = 1
            else:
                oldtagdict[vtag] += 1

            vtag2, cresultdict, details = self.trim_vtag(vtag)

            # print(title)
            # print(vtag+'==>'+'#'.join(vtag2))
            # for debug_word in details:
            #     print('\t'+debug_word)

            for k, v in cresultdict.items():
                if k not in resultdict:
                    resultdict[k] = v
                else:
                    resultdict[k].extend(v)

            newtaglist.extend(vtag2)

        # newtaglist process
        x2list = []
        x2dict = {}
        mergetaglist = []
        mergetagdict = {}

        tmp_title = tmp_title.strip()
        if tmp_title != '' and len(tmp_title.split(' ')) >= 2:
            if tmp_title not in mergetagdict:
                mergetaglist.append((tmp_title, 30, 'onegramemerge'))
                mergetagdict[tmp_title] = 'onegramemerge'

        for ntag in newtaglist:
            ntag = ntag.strip()
            if ntag != '' and ntag not in self.fix2list:
                if ntag not in x2dict:
                    x2dict[ntag] = 1
                else:
                    x2dict[ntag] += 1

                x2list.append(ntag)

        # step0:title split
        pattern1 = r'(\||\-\s{1}|\s{1}\-|\(|\)|\?|!|–\s{1}|\s{1}–|│|' \
                   r'\"|\'\s{1}|\s{1}\'|‘\s{1}|\s{1}‘|’\s{1}|\s{1}’|:|\s{1}\[|\]\s{1}|~|\/\s{1}|\s{1}\/|🔴|•)'
        res = re.compile(pattern1, flags=0)

        title2 = res.sub("#", title.lower())

        for trunk in title2.split('#'):
            trunk = trunk.strip()
            if trunk == '': continue
            ntaglist = []
            foundit = 0
            if trunk in self.vtag2kwline:
                if self.vtag2kwline[trunk][4] == 0 and self.vtag2kwline[trunk][0] >= 2:
                    ntaglist.append(trunk)
                    foundit = 1
            if foundit == 0 and trunk in self.kw2vtag:
                tagset = self.kw2vtag[trunk]
                for ntag in tagset:
                    if ntag in self.vtag2kwline:
                        if self.vtag2kwline[ntag][4] == 0 and self.vtag2kwline[ntag][0] >= 2:
                            ntaglist.append(ntag)
            for xtag in ntaglist:
                if xtag not in mergetagdict:
                    mergetaglist.append((xtag, 25, 'trunk'))
                    mergetagdict[xtag] = 'trunk'
            # if trunk in title_split_tag and trunk not in mergetagdict:
            #     trunkres = title_split_tag[trunk]
            #     mergetaglist.append((trunkres, 25, 'trunk'))
            #     mergetagdict[trunkres] = 'trunk'

        # step1:
        for k, v in x2dict.items():
            if v >= 2 and k not in mergetagdict:
                mergetaglist.append((k, 10 * v, 'tf>=2'))
                mergetagdict[k] = 'tf>=2'

        # step2:
        step2_dict = {}
        for x in x2list:

            for y in x2list:
                if len(x) < len(y) and x in oldtagdict and (y.startswith(x + ' ') or y.endswith(' ' + x)):
                    if x not in step2_dict:
                        step2_dict[x] = 1 + len(x.split(' '))
                    else:
                        step2_dict[x] += 1 + len(x.split(' '))

        sortedtstep2_dict = sorted(step2_dict.items(), key=lambda k: k[1], reverse=True)
        for k, v in sortedtstep2_dict:
            if v >= 3:
                if k not in mergetagdict:
                    mergetagdict[k] = 'fix'
                    mergetaglist.append((k, v, 'fix'))

        # stpe3: x2list 剩下的
        step3dict = {}
        for k in x2list:
            ff = 0

            if k in self.vtag2kwline:
                ff = 1
            elif title.lower().strip().startswith(k) or title.lower().strip().endswith(k):
                ff = 1
            else:
                pass
            if ff == 0: continue
            if k not in step3dict:
                step3dict[k] = ff
            else:
                step3dict[k] += ff

        sortedtstep3_dict = sorted(step3dict.items(), key=lambda k: k[1], reverse=True)
        for k, v in sortedtstep3_dict:
            if k not in mergetagdict:
                mergetagdict[k] = 'x2'
                if len(mergetaglist) < 7:
                    mergetaglist.append((k, v, 'x2'))

        # step4: type period lang
        for k, vlist in resultdict.items():

            max_dict = {}
            for v in vlist:
                v = v.strip()
                if v not in max_dict:
                    max_dict[v] = 1
                else:
                    max_dict[v] += 1
            sortedmax_dict = sorted(max_dict.items(), key=lambda k: k[1], reverse=True)

            if k == 'period':

                for kk, vv in sortedmax_dict:
                    if kk not in ['best', 'top', 'latest', 'updates', 'today', 'new']:
                        ptag = kk
                        if ptag != '' and ptag not in mergetagdict:
                            mergetagdict[ptag] = 'ptag'
                            mergetaglist.append(('p_' + ptag, 0.5, 'ptag'))
                        break
            if k == 'lang':
                for kk, vv in sortedmax_dict:
                    ltag = kk
                    if ltag != '' and ltag not in mergetagdict:
                        mergetagdict[ltag] = 'ltag'
                        mergetaglist.append(('l_' + ltag, 0.5, 'ltag'))
                    break
            if k == 'type':

                if len(sortedmax_dict) > 0:
                    cc_tag = sortedmax_dict[0][0]
                    if cc_tag != '' and cc_tag not in mergetagdict:
                        mergetagdict[cc_tag] = 'ttag'
                        mergetaglist.append((cc_tag, 0.5, 'ttag'))
                for kk, vv in sortedmax_dict:
                    if len(kk.split(' ')) >= 2:
                        if kk != '' and kk not in mergetagdict:
                            mergetagdict[kk] = 'ttag'
                            mergetaglist.append((kk, 0.5, 'ttag'))

        return [item[0] for item in mergetaglist], resultdict

    def extract_tag(self, title, text):
        self.log.info("extracting tags from title and text...")
        mergetaglist = []
        mergetagdict = {}
        lasttaglist = []
        pattern1 = r'(\||\-\s{1}|\s{1}\-|\(|\)|\?|!|–\s{1}|\s{1}–|│|' \
                   r'\"|\'\s{1}|\s{1}\'|‘\s{1}|\s{1}‘|’\s{1}|\s{1}’|:|\s{1}\[|\]\s{1}|~|\/\s{1}|\s{1}\/|🔴|•)'
        res = re.compile(pattern1, flags=0)

        title2 = res.sub("#", title)
        title2_lower = title2.lower()

        if text.startswith(title):
            text = text[len(title):]
        text2 = text.replace('\\n', ' #')
        pattern_http = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        pattern_replace = re.compile(r'(▬|=)')

        text2 = pattern_http.sub("#", text2)
        text2 = pattern_replace.sub("#", text2)
        text2_lower = text2.lower()

        text2_ner_list = self.get_continuous_chunks(text2)

        debug_list1 = []
        debug_list2 = []
        title_nerlist = []
        for title_trunk in title2.split('#'):
            title_trunk = title_trunk.strip()
            title_trunk_lower = title_trunk.lower()
            if title_trunk == '': continue
            if text2_lower.find(title_trunk_lower) >= 0 and title_trunk != title2:
                debug_list1.append(title_trunk_lower)
            if title_trunk_lower in self.vtag2kwline:
                if title_trunk_lower not in mergetagdict:
                    mergetaglist.append([title_trunk_lower, 'title_trunk_vtag'])
                    mergetagdict[title_trunk_lower] = None
            elif title_trunk_lower in self.kw2vtag:
                for vtag in self.kw2vtag[title_trunk_lower]:
                    if vtag not in mergetagdict:
                        mergetaglist.append([title_trunk_lower, 'title_trunk_kw'])
                        mergetagdict[title_trunk_lower] = None
                # debug_list2.append(title_trunk_lower)

            title_trunk_list = self.get_continuous_chunks(title_trunk)
            title_nerlist.extend(title_trunk_list)
        tfdict = {}
        for trunk in title_nerlist:
            trunk_lower = trunk.lower()
            if trunk_lower == '': continue
            if trunk_lower in self.stopwords: continue
            n = len(trunk_lower.split(' '))
            x = 1.5
            if n >= 2:
                x = 2
            if trunk_lower not in tfdict:
                tfdict[trunk_lower] = x
            else:
                tfdict[trunk_lower] += x
        for trunk in text2_ner_list:
            trunk_lower = trunk.lower()
            if trunk_lower in self.stopwords: continue
            if trunk_lower == '': continue
            if trunk_lower not in tfdict:
                tfdict[trunk_lower] = 1
            else:
                tfdict[trunk_lower] += 1
        sorted_tfdict = sorted(tfdict.items(), key=lambda k: k[1], reverse=True)
        sorted_tfdict2 = [x for x in sorted_tfdict if x[1] >= 2]

        for c_tag, c_tf in sorted_tfdict2:

            if c_tag in self.vtag2kwline or len(c_tag.split(' ')) >= 2:
                if c_tag not in mergetagdict:
                    mergetaglist.append([c_tag, 'tf_vtag'])
                    mergetagdict[c_tag] = None

        for i, (tag, reason) in enumerate(mergetaglist):
            if i >= 5: break
            lasttaglist.append(tag)

        return lasttaglist

    def trim_vtag(self, inputline):

        # inputline = 'latest news	2019 news 2018'

        inputraw = inputline
        resultdict = {}
        details = []

        # 1. 预清洗

        inputline = inputline.replace('#', ' ')
        inputtoken = []
        for w in inputline.split(' '):
            w = w.strip()
            if w != '':
                inputtoken.append(w)

        inputline = ' '.join(inputtoken)

        details.append(inputraw + '0==>' + inputline)

        # 2. 预判断:is in vtag2kwline or not

        c_tag = []
        if inputline in self.vtag2kwline:
            c_tag = [inputline]
        elif inputline in self.kw2vtag:
            c_tag = list(self.kw2vtag[inputline])
        if len(c_tag) >= 1:
            details.append(inputline + '1==>' + '#'.join(c_tag))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(inputtoken) < 2:
            details.append(inputline + '2==>' + inputline)
            return [inputline], resultdict, details
        else:
            pass

        # 3.trim1 process: period trim 时间性单词 或修饰行状语

        pattern_period = r'^top\s{1}\d.\s{1}|^best|^best of|^hit|2015|2016|2017|2018|2019|latest|updates|today| new$|new released|^new '
        res_period = re.compile(pattern_period, flags=0)

        res1 = res_period.sub('', inputline.strip())
        res1_tokens = []
        for w in res1.split(' '):
            w = w.strip()
            if w != '':
                res1_tokens.append(w)

        res1 = ' '.join(res1_tokens)

        res1findall = res_period.findall(inputline.strip())
        resultdict['period'] = res1findall
        details.append(inputline + '3==>' + res1)

        # 3. 预判断:is in vtag2kwline or not
        c_tag = []
        if res1 in self.vtag2kwline:
            c_tag = [res1]
        elif res1 in self.kw2vtag:
            c_tag = list(self.kw2vtag[res1])
        if len(c_tag) >= 1:
            details.append(inputline + '4==>' + '#'.join(c_tag))
            return c_tag, resultdict, details
        else:
            pass
        # 小于2元词不处理,直接返回
        if len(res1_tokens) < 2:
            details.append(inputline + '5==>' + inputline)
            return [inputline], resultdict, details
        else:
            pass

        # 4.trim2 process: language trim
        res1 = res1.replace('in english', 'english')
        res1 = res1.replace('in hindi', 'hindi')
        res1 = res1.replace('in hind', 'hindi')
        res1 = res1.replace('in hinid', 'hindi')
        res1 = res1.replace('in telugu', 'telugu')
        res1 = res1.replace('in tamil', 'tamil')
        res1 = res1.replace('in malayalam', 'malayalam')
        res1 = res1.replace('in bhojpuri', 'bhojpuri')
        res1 = res1.replace('in punjabi', 'punjabi')
        res1 = res1.replace('bangla', 'bengali')
        res1 = res1.replace('in bengali', 'bengali')
        res1 = res1.replace('in marathi', 'marathi')
        res1 = res1.replace('in kannada', 'kannada')
        res1 = res1.replace('in gujarati', 'gujarati')
        res1 = res1.replace('in rajasthani', 'rajasthani')
        res1 = res1.replace('haryanavi', 'haryanvi')
        res1 = res1.replace('in haryanvi', 'haryanvi')
        res1 = res1.replace('in assamese', 'assamese')
        res1 = res1.replace('in bodo', 'bodo')
        res1 = res1.replace('in dogri', 'dogri')
        res1 = res1.replace('in kashmiri', 'kashmiri')
        res1 = res1.replace('in konkani', 'konkani')
        res1 = res1.replace('in maithili', 'maithili')
        res1 = res1.replace('in manipuri', 'manipuri')
        res1 = res1.replace('in nepali', 'nepali')
        res1 = res1.replace('in odia', 'odia')
        res1 = res1.replace('in sanskrit', 'sanskrit')
        res1 = res1.replace('in santali', 'santali')
        res1 = res1.replace('in sindhi', 'sindhi')
        res1 = res1.replace('in urdu', 'urdu')

        # 4. 预判断:is in vtag2kwline or not
        c_tag = []
        if res1 in self.vtag2kwline:
            c_tag = [res1]
        elif res1 in self.kw2vtag:
            c_tag = list(self.kw2vtag[res1])
        if len(c_tag) >= 1:
            details.append(res1 + '6==>' + '#'.join(c_tag))
            return c_tag, resultdict, details
        else:
            pass
        # 小于2元词不处理,直接返回
        if len(res1.split(' ')) < 2:
            details.append(res1 + '7==>' + res1)
            return [res1], resultdict, details
        else:
            pass

        pattern_lang = r'english|hindi|telugu|tamil|malayalam|' \
                       r'bhojpuri|punjabi|bengali|marathi|kannada|' \
                       r'gujarati|rajasthani|haryanvi|assamese|bodo|' \
                       r'dogri|kashmiri|konkani|maithili|manipuri|nepali|' \
                       r'odia|sanskrit|santali|sindhi|urdu|haryanavi'

        res_lang = re.compile(pattern_lang, flags=0)
        res2 = res_lang.sub('', res1.strip())

        res2_tokens = []
        for w in res2.split(' '):
            w = w.strip()
            if w != '':
                res2_tokens.append(w)
        res2 = ' '.join(res2_tokens)
        if res2.endswith('video') or res2.endswith('song') or res2.endswith('movie') or res2.endswith('show'):
            res2 = res2 + 's'

        res2findall = res_lang.findall(res1.strip())
        resultdict['lang'] = res2findall
        details.append(res1 + '8==>' + res2)

        # 4. 预判断:is in vtag2kwline or not
        c_tag = []
        if res2 in self.vtag2kwline:
            c_tag = [res2]
        elif res2 in self.kw2vtag:
            c_tag = list(self.kw2vtag[res2])
        if len(c_tag) > 1:
            details.append(res2 + '9==>' + '#'.join(c_tag))
            return c_tag, resultdict, details
        else:
            pass
        # 小于等于2元词不处理,直接返回
        if len(res2_tokens) < 2:
            details.append(res1 + '10==>' + res1)
            return [res1], resultdict, details
        else:
            pass

        # 5.trim3 process: type

        # trim2: type
        word = res2
        word2 = word

        resultdict['type'] = []
        for k, v in self.word2fix.items():

            if word.find(k + ' ') >= 0 or word.find(' ' + k) >= 0 or word == k:
                word2 = word.replace(k, '').strip()
                resultdict['type'].append(k)
                word = word2

        if word2 in self.word2fix:
            word2 = ''
        res3_tokens = []
        for x in word2.split(' '):
            if x != '' and x != 's':
                res3_tokens.append(x)

        res3 = ' '.join(res3_tokens)

        # 5. 预判断:is in vtag2kwline or not
        c_tag = []
        if res3 in self.vtag2kwline:
            c_tag = [res3]
        elif res3 in self.kw2vtag:
            c_tag = list(self.kw2vtag[res3])
        if len(c_tag) > 1:
            details.append(res3 + '11==>' + '#'.join(c_tag))
            return c_tag, resultdict, details
        else:
            pass
        # 小于等于2元词不处理,直接返回
        if len(res3_tokens) < 2:
            details.append(res2 + '12==>' + res2)
            return [res2], resultdict, details
        else:
            pass
        details.append(res3 + '13==>' + res3)
        return [res3], resultdict, details

    def get_continuous_chunks(self, text):

        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                continuous_chunk.append(" ".join(current_chunk))
                continuous_chunk.append(i[0])
                current_chunk = []
            else:
                continuous_chunk.append(i[0])
                continue
        if current_chunk:
            continuous_chunk.append(" ".join(current_chunk))
            current_chunk = []

        return continuous_chunk


