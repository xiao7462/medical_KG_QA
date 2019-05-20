import urllib.request
import urllib.parse
import re
from lxml import etree
import pymongo
import traceback
import json

class Medical_spider:
    def __init__(self):
        self.conn = pymongo.MongoClient() #创建数据库需要使用 MongoClient 对象，可以指定连接的 URL 地址和要创建的数据库名。
        #conn.list_database_names() 可以判断是否有database存在
        self.db = self.conn['medical'] #创建 medical的数据库
        self.col = self.db['data'] # 创建data的集合

        '''根据url，请求html'''
    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'} # 请求头，用来伪装成浏览器
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        return html # 返回一个utf-8编码的字符串

    def get_str(self,ps): #获得页面下所有的文本
        str1 = ''
        for i in ps:
            try:
                str1 += i.text
            except:
                pass
        str2 = str1.replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
        return str2

    '''获得所有的疾病网址 '''
    def get_jibin_list(self):
        url = 'http://jbk.39.net/'
        html = self.get_html(url)
        selector = etree.HTML(html)
        jbk_list =[] # 获取所有疾病的子页面链接
        for i in selector.xpath('//p[@class="menu_item_box_txt"]/a/@href'):
            if 'http' in i and 'jiancha' not in i and 'shoushu' not in i: #去除掉大科室，检查和手术的链接
                jbk_list.append(i)
        return jbk_list

    def basicinfo_spider(self,url):
        # url = 'http://jbk.39.net/pnz1/jbzs/'
        html = self.get_html(url)
        html1 = html.replace(' ','').replace('/n','')  # 用于xpath解决不了的html，改成用正则来解决
        selector = etree.HTML(html)
        # title = 脾囊肿
        pattern_biaoti = re.compile(r'<h1>(.*)</h1>')
        title = pattern_biaoti.findall(html1)[0]
        # 就诊科室
        #category = selector.xpath('//div[3]/ul/li[1]/span[2]/a/text()')
        # 简介
        desc =  selector.xpath('//p[@class = "introduction"]')[0].text

        # 医保= 是
        pattern_yibao = re.compile(r'是否属于医保：</span>\r\n<spanclass="disease_basic_txt">([\u4e00-\u9fa5]+)</span>')
        medical_insurance ='是否属于医保：%s' %(pattern_yibao.findall(html1,re.S)[0])
        # 传染性
        pattern_chuanran = re.compile(r'传染性：</span>\r\n<span>([\u4e00-\u9fa5]+)</span>')
        contagious = '传染性:%s'%(pattern_chuanran.findall(html1)[0])
        # 发病部位
        pattern_buwei = re.compile(r'发病部位：</span>\r\n<span>\r\n<ahref=".*">([\u4e00-\u9fa5]+)</a>')
        incidence_site = "发病部位: %s"%(pattern_buwei.findall(html1)[0])
        # 多发人群
        pattern_renqun = re.compile(r'多发人群：</span>\r\n<span>(.*)</span>')
        people = "多发人群 : %s" %(pattern_renqun.findall(html1)[0])
        # 治疗周期
        try:
            pattern_zhouqi = re.compile(r'治疗周期：</span>\r\n<spanclass="disease_basic_txt">(.*)</span>')
            time = "治疗周期 : %s" %(pattern_zhouqi.findall(html1)[0])
        except:
            time = "治疗周期 : %s" %('无')
        # 治愈率
        try:
            pattern_zhiyulv = re.compile(r'治愈率：</span>\r\n<span>(.*)</span>')
            cure_rate = "治愈率: %s"%(pattern_zhiyulv.findall(html1)[0])
        except:
            cure_rate = "治愈率: %s"%('无')
        # 别名
        try:
            pattern_bieming = re.compile(r'别名：</span>\r\n<spanclass="disease_basic_txt">(.*)</span>')
            alias = '别名 ：%s'%(pattern_bieming.findall(html1)[0])
        except:
            alias = '别名 ：%s'%('无')
        
        attributes_list = [medical_insurance,contagious,incidence_site,people,time,cure_rate,alias]
        infobox = []
        infobox.extend(attributes_list)
        
        basic_data = {}
        basic_data['name'] = title
        #basic_data['category'] = category
        basic_data['desc'] = desc
        basic_data['attributes'] = infobox
        return basic_data

    def symptom_spider(self,url): #治疗症状,预防，诊断，治疗，检查，饮食，护理解析
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//p[@class= "article_content_text" or @class= "article_text" or @class = "article_title_num"]')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)
        #return infoboxs.split('二、')[0].split('一、')[1], infoboxs.split('二、')[1]


    def bingfazheng(self,url): #并发症
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps1 = selector.xpath('//div[1]/div[2]/p[2]/a')
        ps2 = selector.xpath('//div[1]/div[2]/div/p')
        infobox1 = []
        infobox2 = []
        for m,n in zip(ps1,ps2):
            info_m = m.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            info_n = n.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info_m:
                infobox1.append(info_m)
            if info_n:
                infobox2.append(info_n)
        return ','.join(infobox1),','.join(infobox2)



    def zhengzhuang(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//div[1]/div[2]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info:
                infobox.append(info)
        early_sym =''
        last_sym =''
        related_sym =''
        typical_sym =''
        for i in infobox:
            if '早期症状' in i:
                early_sym = i
            if '晚期症状' in i:
                last_sym = i
            if '相关症状' in i:
                related_sym = i
            if '典型症状' in i :
                typical_sym = i
        return early_sym, last_sym, typical_sym,related_sym
        
    
    
    def jiancha_spider(self,url): # 获得检查的项目
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//table/tbody/tr/td[1]/a')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    def food(self,url): # 宜吃食物和忌吃食物
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps1 = selector.xpath('//table[1]/tbody/tr/td[1]')
        infobox_1 = []
        ps2 = selector.xpath('//table[2]/tbody/tr/td[1]')
        infobox_2 = []

        for p in ps1:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info:
                infobox_1.append(info)

        for p in ps2:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '').replace(u'\u3000',u' ')
            if info:
                infobox_2.append(info)
        return '\n'.join(infobox_1), '\n'.join(infobox_2)

    def drug_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        infobox = selector.xpath('//div/ul[@class="drug-list"]/li/a/@title')
        return infobox

    def jiuzhen_spider(self,url): #治疗症状,并发症,病因，预防，诊断，治疗，检查，饮食，护理解析
        html = self.get_html(url)
        selector = etree.HTML(html)
        infobox = []
        for i in range(1,10):
            infobox_sub =[]
            ps_title = selector.xpath('//*[@id="contentText"]/dl[%s]/dt'%(i))
            ps_answer = selector.xpath('//*[@id="contentText"]/dl[%s]/dd'%(i))
            infobox_sub.append(self.get_str(ps_title))
            infobox_sub.append(self.get_str(ps_answer))
            infobox.append(infobox_sub)
        return infobox


    def data_spider(self,list):
        database = []
        count = 0
        max_count  = len(list)
        for i in list:
            basic_url = i + 'jbzs/'
            zhengzhuang_url = i + 'zztz/'
            bingyin_url = i + 'blby/'
            bingfazheng_url = i + 'bfbz/'
            yufang_url = i + 'yfhl/'
            jianbie_url = i + 'jb/'
            zhiliao_url = i + 'yyzl/'
            jiuzheng_url = i + 'jzzn/'
            jiancha_desc_url = i + 'jcjb/'
            huli_url = i + 'hl/'
            yinshi_url = i + 'ysbj/'
            drug = i + 'cyyp/'

            try:
                data = {}
                data['url'] = basic_url
                data['basic_info'] = self.basicinfo_spider(basic_url)
                data['early_sym'], data['last_sym'], data['typical_sym'], data['related_sym'] = self.zhengzhuang(zhengzhuang_url)
                data['bingyin'] = self.symptom_spider(bingyin_url)
                data['bingfazheng'], data['bingfazheng_desc'] =self.bingfazheng(bingfazheng_url)
                data['yufang'] = self.symptom_spider(yufang_url)
                data['jianbie'] = self.symptom_spider(jianbie_url)
                data['zhiliao'] = self.symptom_spider(zhiliao_url)
                data['jiuzheng'] = self.jiuzhen_spider(jiuzheng_url)
                data['jiancha_desc'] = self.symptom_spider(jiancha_desc_url)
                data['jiancha'] = self.jiancha_spider(jiancha_desc_url)
                data['huli'] = self.symptom_spider(huli_url)
                data['yinshi_desc'] = self.symptom_spider(yinshi_url)
                data['eat'],data['no_eat'] = self.food(yinshi_url)
                data['drug'] = self.drug_spider(drug)  
                
                #self.col.insert(data)
                database.append(data)
                count +=1
                print (count/max_count)
            except:
                traceback.print_exc()
                print (data['url'])
        return database
if __name__ == "__main__":
    med = Medical_spider()
    jbk_list = med.get_jibin_list()
    # 测试
    database = med.data_spider(jbk_list)
    with open("./database_new.json","w") as f:
        json.dump(database,f)
        print ("加载入文件完成...")
