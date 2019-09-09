# EntityRelation
A package to extract relations between entities. this maybe helpful and a important link for constructing KG. base on DSNF(Dependency Semantic Normal Forms) for now.


# 使用及效果示例
（第一次使用由于需要去下载ltp模型，所以实例化的时候可能会等待几分钟）
<p align="center"><img src="images/sample.png?raw=true"/></p>

# 安装
可以直接通过pip安装
``` bash
pip install EntityRelation
``` 

或者：
``` bash
git clone https://github.com/LG-1/EntityRelation.git
cd EntityRelation
python setup.py install
``` 


# 为什么要封装这个包
在知识图谱的构建过程中很重要的一步是实体关系的提取，看了一些关于知识图谱的项目大都是全过程的(有些可能存在硬编码)，导致想要进行其他领域的实体关系提取（知识图谱构建）时都不会十分顺畅。
所以看到[lemonhu](https://github.com/lemonhu)的开放领域实体关系提取项目（[open-entity-relation-extraction](https://github.com/lemonhu/open-entity-relation-extraction)）觉得很有意义。
但是原项目也有一些硬编码的地方，而且其他项目想要使用可能不是那么方便。
基于以上原因，动手在lemonhu项目的基础上封装了一个python包，便于插拔使用。
目前包的方法并不针对特定领域，一种比较简单的迁移到专有领域的方法是替换resource文件夹的user_dict.txt分词词典。
默认包含的词典只是一个比较基础的版本。


# 其它
还有很多需要优化的地方，非常欢迎大家提供意见建议或者issue。

目前DSNF的效率还可以，但准确率还有待进一步的测试覆盖。

后续还考虑添加其他的关系提取实现，从而使得模型选择参数化。



# Refrence
主要参考了: https://github.com/lemonhu/open-entity-relation-extraction
进行了封装组件化便于使用。

[Jia S, Li M, Xiang Y. Chinese Open Relation Extraction and Knowledge Base Establishment[J]. ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP), 2018, 17(3): 15.](https://www.researchgate.net/profile/Shengbin_Jia2/publication/323198509_Chinese_Open_Relation_Extraction_and_Knowledge_Base_Establishment/links/5ad80644aca272fdaf802ff1/Chinese-Open-Relation-Extraction-and-Knowledge-Base-Establishment.pdf)