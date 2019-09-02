

class EntityPair(object):
    """实体对
    Atrributes:
        entity1: WordUnit，实体1的词单元
        entity2: WordUnit，实体2的词单元
    """
    def __init__(self, entity1, entity2):
        self.entity1 = entity1
        self.entity2 = entity2

    def get_entity1(self):
        return self.entity1

    def set_entity1(self, entity1):
        self.entity1 = entity1

    def get_entity2(self):
        return self.entity2

    def set_entity2(self, entity2):
        self.entity2 = entity2


class SentenceUnit(object):
    """句子单元组成，每行为一个词单元，并获得每个词头部的词单元
    Attributes:
        words: WordUnit list，词单元列表
    """
    words = None

    def __init__(self, words):
        self.words = words
        for i in range(len(words)):
            self.words[i].head_word = self.get_word_by_id(self.words[i].head)

    def get_word_by_id(self, id):
        """根据id获得词单元word
        Args:
            id: int，词单元ID
        Returns:
            word: 词单元
        """
        for word in self.words:
            if word.ID == id:
                return word
        return None

    def get_head_word(self):
        """获得整个句子的中心词单元
        Returns:
            head_word: WordUnit，中心词单元
        """
        for word in self.words:
            if word.head == 0:
                return word
        return None

    def to_string(self):
        """将一句中包含的word转成字符串，词单元之间换行
        Returns:
            words_str: str，转换后的字符串
        """
        words_str = ''
        for word in self.words:
            words_str += word.to_string() + '\n'
        return words_str.rstrip('\n')

    def get_lemmas(self):
        """获得句子的分词结果
        Returns:
            lemmas: str，该句子的分词结果
        """
        lemmas = ''
        for word in self.words:
            lemmas += word.lemma + '\t'
        return lemmas.rstrip('\t')


class WordUnit(object):
    """词单元组成"""
    # 定义类变量
    # 当前词在句子中的序号，1开始
    ID = 0
    # 当前词语的原型(或标点)，就是切分后的一个词
    lemma = ''
    # 当前词语的词性
    postag = ''
    # 当前词语的中心词，及当前词的头部词
    head = 0  # 指向词的ID
    head_word = None  # 该中心词单元
    # 当前词语与中心词的依存关系
    dependency = ''  # 每个词都有指向自己的唯一依存

    def __init__(self, ID, lemma, postag, head=0, head_word=None, dependency=''):
        self.ID = ID
        self.lemma = lemma
        self.postag = postag
        self.head = head
        self.head_word = head_word
        self.dependency = dependency

    def get_id(self):
        return self.ID

    def set_id(self, ID):
        self.ID = ID

    def get_lemma(self):
        return self.lemma

    def set_lemma(self, lemma):
        self.lemma = lemma

    def get_postag(self):
        return self.postag

    def set_postag(self, postag):
        self.postag = postag

    def get_head(self):
        return self.head

    def set_head(self, head):
        self.head = head

    def get_head_word(self):
        return self.head_word

    def set_head_word(self, head_word):
        self.head_word = head_word

    def get_dependency(self):
        return self.dependency

    def set_dependency(self, dependency):
        self.dependency = dependency

    def to_string(self):
        """将word的相关处理结果转成字符串，tab键间隔
        Returns:
            word_str: str，转换后的字符串
        """
        word_str = ''
        word_str += (str(self.ID) + '\t' + self.lemma + '\t' + self.postag + '\t' +
                     str(self.head) + '\t' + self.dependency)
        return word_str


class EntityCombine(object):
    """将分词词性标注后得到的words与netags进行合并"""
    def combine(self, words, netags):
        """根据命名实体的B-I-E进行词合并
        Args:
            words: WordUnit list，分词与词性标注后得到的words
            netags: list，命名实体识别结果
        Returns:
            words_combine: WordUnit list，连接后的结果
        """
        words_combine = []  # 存储连接后的结果
        length = len(netags)
        n = 1  # 实体计数，从1开始
        i = 0
        while i < length:
            if 'B-' in netags[i]:
                newword = words[i].lemma
                j = i + 1
                while j < length:
                    if 'I-' in netags[j]:
                        newword += words[j].lemma
                    elif 'E-' in netags[j]:
                        newword += words[j].lemma
                        break
                    elif 'O' == netags[j] or (j+1) == length:
                        break
                    j += 1
                words_combine.append(WordUnit(n, newword, self.judge_postag(netags[j-1])))
                n += 1
                i = j
            else:
                words[i].ID = n
                n += 1
                words_combine.append(words[i])
            i += 1
        return self.combine_comm(words_combine)

    def combine_comm(self, words):
        """根据词性标注进行普通实体合并
        Args:
            words: WordUnit list，进行命名实体合并后的words
        Returns:
            words_combine: WordUnit list，进行普通实体连接后的words
        """
        newword = words[0].lemma  # 第一个词，作为新词
        words_combine = []  # 存储合并后的结果
        n = 1
        i = 1  # 当前词ID
        while i < len(words):
            word = words[i]
            # 词合并: (前后词都是实体) and (前后词的词性相同 or 前词 in ["nz", "j"] or 后词 in ["nz", "j"])
            if (self.is_entity(word.postag) and self.is_entity(words[i-1].postag)
                    and (word.postag in {'nz', 'j'} or words[i-1].postag in {'nz', 'j'})):
                newword += word.lemma
            else:
                words_combine.append(WordUnit(n, newword, words[i-1].postag))  # 添加上一个词
                n += 1
                newword = word.lemma  # 当前词作为新词
            i += 1
        # 添加最后一个词
        words_combine.append(WordUnit(n, newword, words[len(words)-1].postag))
        return words_combine

    @staticmethod
    def judge_postag(netag):
        """根据命名实体识别结果判断该连接实体的词性标注
        Args:
            netag: string，该词的词性标注
        Returns:
            entity_postag: string，判别得到的该连接实体的词性
        """
        entity_postag = ''
        if '-Ns' in netag:
            entity_postag = 'ns'  # 地名
        elif '-Ni' in netag:
            entity_postag = 'ni'  # 机构名
        elif '-Nh' in netag:
            entity_postag = 'nh'  # 人名
        return entity_postag

    @staticmethod
    def is_entity(netag):
        """根据词性判断该词是否是候选实体
        Args:
            netag: string，该词的词性标注
        Returns:
            flag: bool, 实体标志，实体(True)，非实体(False)
        """
        flag = False  # 默认该词标志不为实体
        # 地名，机构名，人名，其他名词，缩略词
        if netag in {'ns', 'ni', 'nh', 'nz', 'j'}:
            flag = True
        return flag
