import json
from py2neo import Graph,Node

class Build_medical:
    def __init__(self):
        with open("./database_new.json",'r') as load_f:
                load_dict = json.load(load_f)
        self.load_dict = load_dict
        self.g =Graph(
                host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
                http_port=7474,  # neo4j 服务器监听的端口号
                user="lhy",  # 数据库user name，如果没有更改过，应该是neo4j
                password="lhy123") 
        #self.g.delete_all()
        
    def read_nodes(self,load_dict ):
            # 共７类节点
            drugs = [] # 药品 1
            foods = [] #　食物
            checks = [] # 检查 1
            departments = [] #科室 1
            diseases = [] #疾病 1
            symptoms = []#症状 1

            disease_infos = []#疾病信息

            # 构建节点实体关系
            rels_noteat = [] # 疾病－忌吃食物关系 1
            rels_doeat = [] # 疾病－宜吃食物关系 1

            rels_recommanddrug = [] # 疾病－热门药品关系 1
            rels_check = [] # 疾病－检查关系 1

            rels_symptom = [] #疾病-相关症状 关系 1
            rels_acompany = [] # 疾病-并发症 关系 1
            rels_category = [] #　疾病-科室之间的关系 1

            count = 0
            for data_json in load_dict:
                disease_dict = {}
                count += 1
                print(count)
                disease = data_json['basic_info']['name']
                disease_dict['name'] = disease
                diseases.append(disease)
                disease_dict['desc'] = '' # 疾病描述 1 
                disease_dict['prevent'] = '' # 预防 1 
                disease_dict['cause'] = '' # 病因  1
                disease_dict['easy_get'] = '' # 人群 1
                disease_dict['cure_department'] = '' #  就诊科室  1
                disease_dict['cure_way'] = '' # 治疗  1
                disease_dict['treatment_cycle'] = '' # 治疗周期 1
                disease_dict['symptom'] = ''  # 1
                # disease_dict['cured_prob'] = '' 
                disease_dict['contagious'] = '' # 传染性 1
                disease_dict['incidence_site'] = '' #发病部位 1
                disease_dict['cure_rate'] ='' # 治疗周期 1
                disease_dict['early_sym'] =''# 早期症状 1
                disease_dict['late_sym'] ='' #晚期症状 1
                disease_dict['typical_sym'] = '' # 典型症状
                #disease_dict['identification'] ='' # 鉴别
                disease_dict['best_time_for_consultation'] ='' # 最佳就诊时间
                disease_dict['duration_of_consulation'] = '' # 就诊时间
                disease_dict['inquiry_content'] = '' # 问诊内容
                disease_dict['diagnostic_criteria'] ='' # 诊断标准
                disease_dict['check_desc'] ='' # 检查的描述
                disease_dict['huli'] = '' # 护理
                disease_dict['food_desc'] ='' # 饮食描述
                disease_dict['jianbie'] ='' # 鉴别 1
                disease_dict['cure_rate'] = '' #治愈率
                
                try: # 相关症状
                    symptoms += data_json['related_sym'].split('： ')[1].strip().split(' ') # 对这个疾病的多症状描述
                    for symptom in data_json['related_sym'].split('： ')[1].strip().split(' '):
                        rels_symptom.append([disease, symptom])
                except:
                    rels_symptom.append([disease, '无'])
                    
                
                try:
                    disease_dict['cure_rate'] = data_json['basic_info']['attributes'][5]
                except:
                    disease_dict['cure_rate'] = '无'
                
                try: # 疾病-并发症 关系
                    for acompany in data_json['bingfazheng'].strip().split(','):
                        rels_acompany.append([disease, acompany])
                except:
                    rels_acompany.append([disease, '无'])
                
                try: #疾病描述
                    disease_dict['desc'] = data_json['basic_info']['desc']
                except:
                    disease_dict['desc'] = '无'

                try: # 疾病预防
                    disease_dict['prevent'] = data_json['yufang']
                except:
                    disease_dict['prevent'] = '无'

                try: # 病因
                    disease_dict['cause'] = data_json['bingyin']
                except:
                    disease_dict['cause']='无'

                try: #  鉴别
                    disease_dict['jianbie'] = data_json['jianbie']
                except:
                    disease_dict['jianbie'] = '无'

                try: # 多发人群
                    disease_dict['easy_get'] = data_json['basic_info']['attributes'][3].split(': ')[1]
                except:
                    disease_dict['easy_get'] = '无'
                    
                    
                try: # 就诊科室
                    rels_category.append([disease,data_json['jiuzheng'][1][1]])
                    disease_dict['cure_department'] = data_json['jiuzheng'][1][1]
                    departments += data_json['jiuzheng'][1][1].split('、')
                except:
                    rels_category.append([disease,'无'])
                    disease_dict['cure_department'] = '无'
                    departments += '无'
                    
                    
                try: # 治疗
                    disease_dict['cure_way'] = data_json['zhiliao']
                except:
                    disease_dict['cure_way'] = '无'
                
                try: # 治疗周期
                    disease_dict['treatment_cycle'] = data_json['basic_info']['attributes'][4]
                except:
                    disease_dict['treatment_cycle'] = '无'
                
                try: # 药品
                    recommand_drug = list(set(data_json['drug']))
                    drugs += recommand_drug
                    for drug in recommand_drug:
                        rels_recommanddrug.append([disease, drug])
                except:
                    rels_recommanddrug.append([disease, '无'])
                
                
                try: # 可以吃的
                    for eat in data_json['eat'].split('\n'):
                        rels_doeat.append([disease, eat])
                    foods += data_json['eat'].split('\n')
                except:
                    rels_doeat.append([disease,'无'])
                    
                    
                try: # 不可以吃的
                    for no_eat in data_json['no_eat'].split('\n'):
                        rels_noteat.append([disease,no_eat])
                    foods += data_json['no_eat'].split('\n')
                except:
                    rels_doeat.append([disease,'无'])

                try: # 检查
                    check = data_json['jiancha'].split('\n')
                    for _check in check:
                        rels_check.append([disease, _check])
                    checks += check
                except:
                    rels_check.append([disease, '无'])
                
                try: # 发病部位
                    incidence_site = data_json['basic_info']['attributes'][2].split(': ')[1]
                    disease_dict['incidence_site'] = incidence_site
                except:
                    disease_dict['incidence_site'] = '无'
                
                try: # 传染性
                    disease_dict['contagious'] = data_json['basic_info']['attributes'][1].split(':')[1]
                except:
                    disease_dict['contagious'] ='无'
                
                try: #  早期症状
                    disease_dict['early_sym'] = data_json['early_sym'].split('： ')[1]
                except :
                    disease_dict['early_sym'] = '无'
                
                
                try: # 晚期症状
                    disease_dict['late_sym'] = data_json['last_sym'].split('： ')[1]
                except:
                    disease_dict['late_sym'] = '无'
                
                
                try: # 最佳就诊时间
                    disease_dict['best_time_for_consultation'] = data_json['jiuzheng'][2][1] # 最佳就诊时间
                except:
                    disease_dict['best_time_for_consultation'] ='无'
                try:
                    disease_dict['duration_of_consulation'] = data_json['jiuzheng'][3][1] # 就诊时间
                except:
                    disease_dict['duration_of_consulation'] ='无'
                try:
                    disease_dict['inquiry_content'] = data_json['jiuzheng'][6][1]  # 问诊内容
                except:
                    disease_dict['inquiry_content'] = '无'
                try:
                    disease_dict['diagnostic_criteria'] = data_json['jiuzheng'][8][1] # 诊断标准
                except:
                    disease_dict['diagnostic_criteria'] = '无'
                
                try: #  护理
                    disease_dict['huli'] = data_json['huli']
                except:
                    disease_dict['huli'] ='无'
                try:
                    disease_dict['food_desc'] = data_json['yinshi_desc']
                except:
                    disease_dict['food_desc'] = '无'
                disease_infos.append(disease_dict)
            drugs = [i for i in set(drugs) if i.strip()!='']
            foods = [i for i in set(foods) if i.strip()!='']
            checks = [i for i in set(checks) if i.strip()!='']
            departments = [i for i in set(departments) if i.strip()!='']
            symptoms = [i for i in set(symptoms) if i.strip()!='']
            diseases = [i for i in set(diseases) if i.strip()!='']
            return drugs, foods, checks, departments,  symptoms, diseases, disease_infos,\
                   rels_check,  rels_noteat, rels_doeat,  rels_recommanddrug,\
                   rels_symptom, rels_acompany, rels_category
                   

    


    def create_node(self,label, nodes):
            count = 0
            for node_name in nodes:
                node = Node(label, name=node_name)
                self.g.create(node)
                count += 1
                print(count, len(nodes))
            return
            
    def create_diseases_nodes( self, disease_infos):
            count = 0
            for disease_dict in disease_infos: # 创建Node节点
                node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                            prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                            easy_get=disease_dict['easy_get'],cure_department=disease_dict['cure_department'],
                            cure_way=disease_dict['cure_way'], treatment_cycle = disease_dict['treatment_cycle'],
                            symptom =disease_dict['symptom'], contagious = disease_dict['contagious'],
                            incidence_site = disease_dict['incidence_site'], cure_rate = disease_dict['cure_rate'],
                            early_sym = disease_dict['early_sym'], late_sym = disease_dict['late_sym'],
                            typical_sym = disease_dict['typical_sym'],best_time_for_consultation = disease_dict['best_time_for_consultation'],
                            duration_of_consulation = disease_dict['duration_of_consulation'], inquiry_content = disease_dict['inquiry_content'],
                            diagnostic_criteria = disease_dict['diagnostic_criteria'],check_desc = disease_dict['check_desc'],
                            huli =  disease_dict['huli'], food_desc = disease_dict['food_desc'],
                            jianbie = disease_dict['jianbie'])
                self.g.create(node)
                count += 1
                print(count)
            return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self ):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat,   rels_recommanddrug,rels_symptom, rels_acompany, rels_category =  self.read_nodes(self.load_dict)  # 获取数据
        self.create_diseases_nodes(disease_infos) # 获得疾病为节点的数据
        self.create_node('Drug', Drugs)
        print(len(Drugs))
        self.create_node('Food', Foods)
        print(len(Foods))
        self.create_node('Check', Checks)
        print(len(Checks))
        self.create_node('Department', Departments)
        print(len(Departments))
        self.create_node('Symptom', Symptoms)
        return

    def create_relationship( self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges)) # 查看所有的对应关系数量
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0] # 对应的疾病
            q = edge[1] # 对应的food
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建实体关系边'''
    def create_graphrels( self):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat,   rels_recommanddrug,rels_symptom, rels_acompany, rels_category =  self.read_nodes(self.load_dict)
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    def export_data(self):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat,   rels_recommanddrug,rels_symptom, rels_acompany, rels_category =  self.read_nodes(self.load_dict)
        
        with open('./drug.txt','w+') as f:
            f.write('\n'.join(Drugs))
        with open('./food.txt','w+') as f:
            f.write('\n'.join(Foods))
        with open('./check.txt','w+') as f:
            f.write('\n'.join(Checks))
        with open('./departments.txt','w+') as f:
            f.write('\n'.join(Departments))
        with open('./symptoms.txt','w+') as f:
            f.write('\n'.join(Symptoms))
        with open('./diseases.txt','w+') as f:
            f.write('\n'.join(Diseases))    
            
        
if __name__ == '__main__':
    handler = Build_medical()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()
