import unittest
from EntityRelation.EntityRelation import EntityRelation


class Test_ER(unittest.TestCase):
    er = EntityRelation()

    def test_exact(self):
        test_sentence = '李晨 黄渤 范冰冰在上海参加国际电影节和'
        res = self.er.get_entity_relation(test_sentence)
        print(res)


if __name__ == '__main__':
    unittest.main()