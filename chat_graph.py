from Question_Classifier import *
from Question_Paser import *
from Answer_Searcher import *
from build_medical import *

handler = Build_medical()
handler.create_graphnodes()
handler.create_graphrels()
#handler.export_data()


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = Question_Classifier()
        self.parser = Quesion_Paser()
        self.searcher = Answer_Searcher()

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理，未查询到结果'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('User:')
        answer = handler.chat_main(question)
        print('Bot:', answer)