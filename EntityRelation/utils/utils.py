
def is_entity(entry):
    """判断词单元是否实体
    Args:
        entry: WordUnit，词单元
    Returns:
        *: bool，实体(True)，非实体(False)
    """
    # 候选实体词性列表
    entity_postags = {'nh', 'ni', 'ns', 'nz', 'j'}
    if entry.postag in entity_postags:
        return True
    else:
        return False


def get_entity_num_between(entity1, entity2, sentence):
    """获得两个实体之间的实体数量
    Args:
        entity1: WordUnit，实体1
        entity2: WordUnit，实体2
        sentence:
    Returns:
        num: int，两实体间的实体数量
    """
    num = 0
    i = entity1.ID + 1
    while i < entity2.ID:
        if is_entity(sentence.words[i]):
            num += 1
        i += 1
    return num
