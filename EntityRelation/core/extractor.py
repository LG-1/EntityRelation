from .core import EntityPair
from .extract_by_dsnf import ExtractByDSNF
from ..utils.utils import is_entity, get_entity_num_between


class Extractor(object):
    """抽取生成知识三元组
    """

    def extract(self, origin_sentence, sentence):
        """
        Args:
            origin_sentence: string，原始句子
            sentence: SentenceUnit，句子单元
        Returns:
            num： 知识三元组的数量编号
        """
        entity_pairs = self.get_entity_pairs(sentence)  # 存储该句子中(满足一定条件)的可能实体对
        res = []
        for entity_pair in entity_pairs:
            entity1 = entity_pair.entity1
            entity2 = entity_pair.entity2

            extract_dsnf = ExtractByDSNF(origin_sentence, sentence, entity1, entity2)
            # [DSNF2|DSNF7]，部分覆盖[DSNF5|DSNF6]
            re1 = extract_dsnf.SBV_VOB(entity1, entity2)

            # [DSNF4]
            re2 = extract_dsnf.SBV_CMP_POB(entity1, entity2)

            re3 = extract_dsnf.SBVorFOB_POB_VOB(entity1, entity2)

            # [DSNF3|DSNF5|DSNF6]，并列实体中的主谓宾可能会包含DSNF3
            re4 = extract_dsnf.coordinate(entity1, entity2)

            # ["的"短语]
            re5 = extract_dsnf.entity_de_entity_NNT(entity1, entity2)

            # # [DSNF1]
            # re6 = extract_dsnf.E_NN_E(entity1, entity2)

            for i in (re1, re2, re3, re4, re5):
                if i is not None:
                    res.append(i)

        return res

    @staticmethod
    def get_entity_pairs(sentence):
        """组成实体对，限制实体对之间的实体数量不能超过4
        Args:
            sentence: SentenceUnit，句子单元
        """
        entities = []
        entity_pairs = []
        for word in sentence.words:
            if is_entity(word):
                entities.append(word)

        length = len(entities)
        i = 0
        while i < length:
            j = i + 1
            while j < length:
                if (entities[i].lemma != entities[j].lemma and
                        get_entity_num_between(entities[i], entities[j], sentence) <= 4):
                    entity_pairs.append(EntityPair(entities[i], entities[j]))
                j += 1
            i += 1

        return entity_pairs


