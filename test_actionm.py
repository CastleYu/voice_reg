import json
import os

import numpy as np
from LAC import LAC
from pymilvus import DataType, FieldSchema, connections, Collection, CollectionSchema
from pymilvus.orm import utility
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import config
from dao import MilvusClient
from wrappers.timer import timerC


# 百度LAC分词器，带<去停用词>功能
class LACTokenizer:
    def __init__(self, seg_mode='lac', stopwords_file=r'H:\Documents\Prometheus\Python\Speech\action\stopwords.txt'):
        if stopwords_file:
            self.load_stopwords(stopwords_file)
        else:
            self._stopwords = []
        self._lac = LAC(mode=seg_mode)

    def load_stopwords(self, filepath):
        if not os.path.exists(filepath):
            filepath = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'stopwords.txt')
        with open(filepath, 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()
        self._stopwords = set(stopwords)

    def segment(self, text):
        lac_result = self._lac.run(text)
        words = list(zip(*lac_result))
        words = [word for word in words if word[0] not in self._stopwords and word[0].strip()]
        return words


class MicomlMatcher:
    def __init__(self, model_name=None):
        self.model_name = model_name or 'paraphrase-multilingual-MiniLM-L12-v2'
        self._lac = LACTokenizer()  # 百度LAC分词
        self._model_bert = None
        self.threshold = 0.8
        self.cached_embeddings = None  # 缓存指令集向量
        self.cached_commands = None  # 缓存原始指令集

    def do_cut(self, input_command):
        i_list = self._lac.segment(input_command)
        input_command = ''.join([i[0] for i in i_list])
        return input_command

    def load_model(self, model_dir):
        model_full_path = str(os.path.join(model_dir, self.model_name))
        self._model_bert = SentenceTransformer(model_full_path)
        return self

    @timerC
    def encode(self, command):
        command = self.do_cut(command)
        return self._model_bert.encode([command])


action_matcher = MicomlMatcher('paraphrase-multilingual-MiniLM-L12-v2').load_model(config.Update.ModelDir)

milvus_client = MilvusClient(config.Milvus.host, config.Milvus.port)

# 定义集合名称和向量维度
collection_name = 'test_vec_384_2'
dim = 384


# milvus_client.get_dao()


@timerC
def search(action):
    query_vector = action_matcher.encode(action)
    # 连接到 Milvus
    connections.connect(host=config.Milvus.host, port=config.Milvus.port)

    # 加载集合
    collection_name = 'test_vec_384_2'
    collection = Collection(name=collection_name)
    collection.load()

    # 构造查询向量（shape必须和集合维度一致，这里是384）
    query_vector = np.random.rand(384).astype('float32').tolist()

    # 执行搜索
    search_params = {
        "metric_type": "COSINE",
        "params": {
            "nprobe": 10}
    }

    results = collection.search(
        data=[query_vector],
        anns_field="vec",
        param=search_params,
        limit=3,
        output_fields=["id"]
    )
    print(results)
    return results


def load(path):
    connections.connect(host=config.Milvus.host, port=config.Milvus.port)

    # 如果集合已存在则删除
    if utility.has_collection(collection_name):
        print(f"集合 {collection_name} 已存在，删除中...")
        utility.drop_collection(collection_name)

    # 定义字段结构
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='vec', dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description="Test collection with COSINE")

    # 创建集合
    collection = Collection(name=collection_name, schema=schema)

    # 创建索引，指定为 COSINE
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {
            "nlist": 128}
    }
    collection.create_index(field_name="vec", index_params=index_params)

    # 加载集合
    collection.load()
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def record(li):
    result = None
    for i in li:
        result = milvus_client.insert(collection_name, action_matcher.encode(i))
    return result


# search("开灯")
# 比较两个文本
text1 = "开门"
text2 = "打开天窗"

vec1 = action_matcher.encode(text1)
vec2 = action_matcher.encode(text2)
# 计算余弦相似度
similarity = cosine_similarity(vec1, vec2)[0][0]
print(f"【{text1}】与【{text2}】的相似度为：{similarity:.4f}")
