#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/2/28 18:41
@File    : client.py
@Desc    : 客户端
"""

import requests
import json

url = 'http://127.0.0.1:18801/nlp_regional/regional'

id1 = "1502764925793848"
title1 = "Celebrated independence in Burma, says old INA warhorse MK Valampuri"
content1 = """When India was declared independent, we were in (then) Burma and hoisted the tri-colour, celebrated the day and continued our service with the Indian National Army (INA) under Subash Chandra Bose, recalls MK Valampuri (89), who served as inspector in the force and was involved in training the sepoys Rengasamy Thiruchirapalli: Valampuri, presently residing at Ahamad Colony of Anna Nagar in Thanjavur, said that his family members were in Ramanathapuram when he left India to join the INA in 1943. “There were around one lakh members in Burma and many were from Tamil Nadu. We had even organised a community lunch on the day,” Valampuri further said. Meanwhile, Rengasamy (88), another freedom fighter from Varagupadi village in Perambalur district, said that he joined the INA at an early age with the help of a relative. “We fired several rounds in the air and sang nationalist songs after hoisting the Indian national flag in Burma”, Rengasamy reminisced. He said that until 1954, he could not reach India. When I returned to India, I was given a rousing reception by the people of my village that I still cherish,” Rengasamy said."""
parms1 = {"id": id1, "title": title1, "content": content1}

id2 = "1502776564471413"
title2 = "Independence Day 2017: These freedom fighters studied in foreign universities"
content2 = """We have heard and read how our freedom fighters fought bravely for an independent India. Most of these nationalists were well-educated and their education ignited their self-esteem to fight for the country’s freedom. Few of them got the chance to acquire knowledge from the reputed foreign universities. They used innovative methods like the boycott of foreign goods to rebel against the British empire. We bring to you a list of these nationalists who went to foreign universities. Mahatma Gandhi The ‘Father of the nation,’ Mahatma Gandhi shook the British empire with his non-violent protests. Born in Gujarat, he studied law at University College London and returned to India to work as a barrister. Dr BR Ambedkar Dr Bhimrao Ramji Ambedkar fought for equality for all, especially for the underprivileged. He was also a noted economist and lawyer. His keen interest in law, economics and political science made him secure multiple degrees from various Indian and foreign universities. He did PhD from the Columbia University and MSc from the London School of Economics. He also went to the University of Bonn in Germany to study economics. Jawaharlal Nehru Jawaharlal Nehru was India’s first Prime Minister who studied at Harrow which is one of England’s leading schools. He then completed his graduation with an honours degree in natural science in 1910. He later went to the Inner Temple where he trained to be a barrister at law. He found a mentor in Mahatama Gandhi and together they worked for an independent India. Varahagiri Venkata Giri Born on August 10, 1894 in Berhampore, Venkata Giri or VV Giri was the son of noted advocate and freedom fighter, Jogayya Panthulu. His early education was at the Kallikote College, Berhampur. He went to Dublin in 1913 to study law. Sarojini Naidu Sarojini Naidu was a bright student and daughter of principal of the Nizam’s College, Hyderabad. She got a scholarship and she entered the University of Madras at the age of 12 and studied (1895–98) at King’s College, London, and later at Girton College, Cambridge. For all the latest Education News, download Indian Express App"""
parms2 = {"id": id2, "title": title2, "content": content2}

id3 = "1502889409622478"
title3 = "2 kids die in different incidents"
content3 = """Erode, Aug 16 (PTI) A three-year-old child died in a road accident, while a 11-month-old was electrocuted while playing in his house at suburban Karungalpalayam in two different incidents in the district, police said. they said the 3-year-old male child died on the spot when he was thrown off after a college van rammed the motorcycle he was travelling with his parents from the rear at Bhavani Both the husband and wife were seriously injured and have been hospitalised. In the second incident late last night,the 11 month child accidentally came in contact with a live wire, attached to the television. The parents rushed him to a private nursing home from where he was referred to Government Headquarters Hospital late last night, but the toddler died, police said. This is published unedited from the PTI feed."""
parms3 = {"id": id3, "title": title3, "content": content3}



# regional test
resp1 = requests.post(url, data=parms1)  # 发送请求
# Decoded text returned by the request
print(resp1.text)

resp2 = requests.post(url, data=parms2)  # 发送请求
# Decoded text returned by the request
print(resp2.text)

resp3 = requests.post(url, data=parms3)  # 发送请求
# Decoded text returned by the request
print(resp3.text)