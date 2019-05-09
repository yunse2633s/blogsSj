#分词工具
import jieba
import jieba.analyse


seg_list = jieba.cut("我来到北京清华大学找，我很开心",cut_all=True)
print("全模式: ", "/".join(seg_list))


seg_list2 = jieba.cut("我来到北京清华大学找，我很开心",cut_all=False)
print("精确模式: ", "/".join(seg_list2))


#jieba.cut() 默认是精确模式
seg_list3 = jieba.cut_for_search("我来到北京清华大学找，我很开心") # 搜索引擎模式
print("搜索引擎模式: ", "#".join(seg_list3))


sentence="我来到北京清华大学子，我很开心"
listGJC=jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
print("关键词提取：",",".join(listGJC))
