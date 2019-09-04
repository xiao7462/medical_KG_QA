# medical_KG_QA


# 1. 项目背景


新学知识图谱知识，这是入门的一个项目， 跟着一步步完成了整个项目，疾病的网站是 http://jbk.39.net/

整个项目的构建框架如下

![pgn](https://i.loli.net/2019/05/20/5ce27fa3887ba23846.png)

## 效果图如下：

![pgn](https://i.loli.net/2019/05/20/5ce28600bfcf815888.png)

# 2.利用neo4j来储存数据

neo4j学习 [neo4j语法初学](https://xiao7462.github.io/2019/05/06/neo4j%E8%AF%AD%E6%B3%95%E5%88%9D%E5%AD%A6/) [linux安装neo4j](https://xiao7462.github.io/2019/04/24/linux%E5%AE%89%E8%A3%85neo4j/)

![pgn](https://i.loli.net/2019/05/20/5ce286b76b1b533797.png)

## 2.1 知识图谱实体类型

| 实体类型 | 中文含义 | 实体数量 | 举例 |
| --- | --- | --- | --- |
| Check | 诊断检查项目 | 1697 | 输卵管通液检查；葡萄糖氧化酶生化分析仪法 |
| Department | 医疗科目 | 49 | 妇产科；乳腺外科 |
| Disease | 疾病 | 601 | 淋巴瘤；股骨头骨折 |
| Drug | 药品 | 2629 | 哈西奈德溶液；参茸白凤丸 |
| Food | 食物 | 637 | 煎炸类食品；黑鱼头 |
| Symptom | 疾病症状 | 1646 | 点状出血；高眼压 |
| Total | 总计 | 7259 | 约7千实体量级 |

## 2.2知识图谱实体关系类型

| 实体关系类型 | 中文含义 | 举例 |
| --- | --- | --- |
| belongs_to | 属于 | <妇科,属于,妇产科> |
| common_drug | 疾病常用药品 | <阳强,常用,甲磺酸酚妥拉明分散片> |
| do_eat | 疾病宜吃食物 | <胸椎骨折,宜吃,黑鱼> |
| drugs_of | 药品在售药品 | <青霉素V钾片,在售,通药制药青霉素V钾片> |
| need_check | 疾病所需检查 | <单侧肺气肿,所需检查,支气管造影> |
| no_eat | 疾病忌吃食物 | <唇病,忌吃,杏仁> |
| recommand_drug | 疾病推荐药品 | <混合痔,推荐用药,京万红痔疮膏> |
| has_symptom | 疾病症状 | <早期乳腺癌,疾病症状,乳腺组织肥厚> |
| acompany_with | 疾病并发疾病 | <下肢交通静脉瓣膜关闭不全,并发疾病,血栓闭塞性脉管炎> |

## 2.3知识图谱属性类型

| 属性类型 | 中文含义 | 举例 |
| --- | --- | --- |
| name | 疾病名称 | 喘息样支气管炎 |
| desc | 疾病简介 | 又称哮喘性支气管炎... |
| cause | 疾病病因 | 常见的有合胞病毒等... |
| prevent | 预防措施 | 注意家族与患儿自身过敏史... |
| cure_lasttime | 治疗周期 | 6-12个月 |
| cure_way | 治疗方式 | "药物治疗","支持性治疗" |
| cured_prob | 治愈概率 | 95% |
| easy_get | 疾病易感人群 | 无特定的人群 |

# 3.医疗知识图谱构建

Question_Classifier.py：问句类型分类脚本
 Question_Paser.py：问句解析脚本
 Answer_Searcher.py：问答查找脚本

| 问句类型 | 中文含义 | 问句举例 |
| --- | --- | --- |
| disease_symptom | 疾病症状 | 乳腺癌的症状有哪些？ |
| symptom_disease | 已知症状找可能疾病 | 最近老流鼻涕怎么办？ |
| disease_cause | 疾病病因 | 为什么有的人会失眠？ |
| disease_acompany | 疾病的并发症 | 失眠有哪些并发症？ |
| disease_not_food | 疾病需要忌口的食物 | 失眠的人不要吃啥？ |
| disease_do_food | 疾病建议吃什么食物 | 耳鸣了吃点啥？ |
| food_not_disease | 什么病最好不要吃某事物 | 哪些人最好不好吃蜂蜜？ |
| food_do_disease | 食物对什么病有好处 | 鹅肉有什么好处？ |
| disease_drug | 啥病要吃啥药 | 肝病要吃啥药？ |
| drug_disease | 药品能治啥病 | 板蓝根颗粒能治啥病？ |
| disease_check | 疾病需要做什么检查 | 脑膜炎怎么才能查出来？ |
| check_disease | 　检查能查什么病 | 全血细胞计数能查出啥来？ |
| disease_prevent | 预防措施 | 怎样才能预防肾虚？ |
| disease_lasttime | 治疗周期 | 感冒要多久才能好？ |
| disease_cureway | 治疗方式 | 高血压要怎么治？ |
| disease_cureprob | 治愈概率 | 白血病能治好吗？ |
| disease_easyget | 疾病易感人群 | 什么人容易得高血压？ |
| disease_desc | 疾病描述 | 糖尿病 |

# 4.项目运行方式

所有的文件都在主目录下，可以从头开始构建，也可以利用 `database_new.zip` 文件解压后运行 `python build_medical.py`

要求配置neo4j数据库已经对应的py2neo的包，本来用的mongodb来储存数据，但是发现直接储存为json格式更方便

文件介绍

| 文件名称 | 作用 |
| --- | --- |
| data_spider_new.py | 网站数据爬取 |
| database_new.zip | 爬取后获得的文件，解压可得到data_spider_new.py运行的文件 |
| build_medical.py | 将database_new文件加载进neo4j数据库 |
| Question_Classifier.py | 将输入的问题进行分类 |
| Question_Paser.py | 问题分类解析 |
| Answer_Searcher.py | 查找问题的答案 |
| chat_graph.py |  直接运行可以与bot进行对话 |

```python
python data_spider_new.py  # 可省略
python build_medical.py # 知识图谱数据导入
python chat_graph.py # 启动问答
```

# 5.总结

-   对结构化的网站采用了xpath+正则匹配来进行数据生成
    
-   本项目以neo4j作为存储，并基于传统规则的方式完成了知识问答，并最终以cypher查询语句作为问答搜索sql，支持了问答服务。
    

-   对于一些大段的文字可以再进行拆分，eg： 症状可以分为早期，晚期，典型症状

