import os
import re
import jieba
import requests
import zipfile
from tqdm import tqdm

from pyltp import Postagger, NamedEntityRecognizer, Parser

from EntityRelation.core.core import EntityCombine, WordUnit, SentenceUnit
from EntityRelation.core.extractor import Extractor


class EntityRelation:
    """对句子进行实体关系提取
    """

    def __init__(self, model_pth=None,
                 user_dict_pth=os.path.dirname(__file__) + '/resource/user_dict.txt'):
        """
        :param model_pth: 模型路径，如果不存在将下架至此路径下
        :param user_dict_pth: 分词词典，可以自定义指定自己的分词词典
        """
        self.user_dict_pth = user_dict_pth

        try:
            jieba.load_userdict(self.user_dict_pth)
        except Exception as e:
            print('not load custom dict into jieba, be care......')
            pass

        if model_pth:
            self.model_pth = model_pth
        else:
            self.model_pth = '/Users/' + os.environ['USER'] + '/ltp_model'

        if not os.path.exists(self.model_pth):
            os.mkdir(self.model_pth)

        pos_pth = self.model_pth + '/ltp_data_v3.4.0/pos.model'
        ner_pth = self.model_pth + '/ltp_data_v3.4.0/ner.model'
        parser_pth = self.model_pth + '/ltp_data_v3.4.0/parser.model'
        if (not os.path.isfile(pos_pth)) or (not os.path.isfile(ner_pth)) or (not os.path.isfile(parser_pth)):
            self.download_ltp_models(self.model_pth)

        try:
            # 加载ltp模型
            # 词性标注模型
            self.postagger = Postagger()
            self.postagger.load(pos_pth)
            # 命名实体识别模型
            self.recognizer = NamedEntityRecognizer()
            self.recognizer.load(ner_pth)
            # 依存句法分析模型
            self.parser = Parser()
            self.parser.load(parser_pth)
        except Exception as e:
            print('Failed to load ltp model')

    def get_entity_relation(self, sentence):
        sub_sentences = [i for i in re.split('[。？！；]|\n', sentence) if len(i) >= 6]  # 简单的长句切分策略
        res = []
        for sub_sentence in sub_sentences:
            sen_lemmas = self.segment(sub_sentence)
            sen_pos = self.postag(sen_lemmas)
            sen_ner_tag = self.ner_tag(sen_pos)
            ltp_sentence = self.parse(sen_ner_tag)

            temp = Extractor().extract(sub_sentence, ltp_sentence)
            res.extend(temp)
        return res

    def segment(self, sentence, entity_postag=dict()):
        """采用NLPIR进行分词处理
        Args:
            sentence: string，句子
            entity_postag: dict，实体词性词典，默认为空集合，分析每一个案例的结构化文本时产生
        Returns:
            lemmas: list，分词结果
        """
        # 添加实体词典
        if entity_postag:
            for entity in entity_postag:
                jieba.add_word(entity)

        lemmas = jieba.lcut(sentence)
        return lemmas

    def postag(self, lemmas):
        """对分词后的结果进行词性标注
        Args:
            lemmas: list，分词后的结果
        Returns:
            words: WordUnit list，包含分词与词性标注结果
        """
        words = []  # 存储句子处理后的词单元
        # 词性标注
        postags = self.postagger.postag(lemmas)

        for i in range(len(lemmas)):
            # 存储分词与词性标记后的词单元WordUnit，编号从1开始
            word = WordUnit(i + 1, lemmas[i], postags[i])
            words.append(word)
        return words

    def get_postag(self, word):
        """获得单个词的词性标注
        Args:
            word: str，单词
        Returns:
            post_tag: str，该单词的词性标注
        """
        post_tag = self.postagger.postag([word, ])
        return post_tag[0]

    def ner_tag(self, words):
        """命名实体识别，并对分词与词性标注后的结果进行命名实体识别与合并
        Args:
            words: WordUnit list，包含分词与词性标注结果
        Returns:
            words_netag: WordUnit list，包含分词，词性标注与命名实体识别结果
        """
        lemmas = []  # 存储分词后的结果
        postags = []  # 存储词性标书结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 命名实体识别
        netags = self.recognizer.recognize(lemmas, postags)
        words_netag = EntityCombine().combine(words, netags)
        return words_netag

    def parse(self, words):
        """对分词，词性标注与命名实体识别后的结果进行依存句法分析(命名实体识别可选)
        Args:
            words: WordUnit list，包含分词，词性标注与命名实体识别结果
        Returns:
            *: SentenceUnit，该句子单元
        """
        lemmas = []  # 分词结果
        postags = []  # 词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 依存句法分析
        arcs = self.parser.parse(lemmas, postags)
        for i in range(len(arcs)):
            words[i].head = arcs[i].head
            words[i].dependency = arcs[i].relation
        return SentenceUnit(words)

    @staticmethod
    def download_ltp_models(save_path):
        print('Downloading ltp models from: http://ospm9rsnd.bkt.clouddn.com/model/ltp_data_v3.4.0.zip')
        url = 'http://ospm9rsnd.bkt.clouddn.com/model/ltp_data_v3.4.0.zip'
        file_name = save_path + '/ltp_data_v3.4.0.zip'
        r = requests.get(url, stream=True)
        with open(file_name, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=1024), total=623041):
                if chunk:
                    f.write(chunk)
        zf = zipfile.ZipFile(file_name)
        zf.extractall(save_path)
        zf.close()
        os.remove(file_name)
        pass


if __name__ == '__main__':
    test_sentence1 = '中国国家主席习近平访问韩国，并在首尔大学发表演讲！中国国家主席习近平访问韩国，并在首尔大学发表演讲！中国国家主席习近平访问韩国，并在首尔大学发表演讲'
    test_sentence2 = '李晨 黄渤 范冰冰在上海参加国际电影节'
    er = EntityRelation()
    ress = er.get_entity_relation(test_sentence1)
    print(ress)
