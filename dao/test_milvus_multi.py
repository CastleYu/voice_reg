from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import random

# 连接到Milvus
connections.connect(
    host="47.121.186.134",  # 用你的Milvus服务器IP替换
    port="19530"
)

# 创建模式
fields = [
    FieldSchema(name="film_id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="filmVector", dtype=DataType.FLOAT_VECTOR, dim=5),  # 用于电影向量的向量字段
    FieldSchema(name="posterVector", dtype=DataType.FLOAT_VECTOR, dim=5)]  # 用于海报向量的向量字段

schema = CollectionSchema(fields=fields, enable_dynamic_field=False)

# 创建集合
collection = Collection(name="test_collection", schema=schema)

# 为每个向量字段创建索引
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {
        "nlist": 128},
}

collection.create_index("filmVector", index_params)
collection.create_index("posterVector", index_params)

# 生成要插入的随机实体
entities = []

for _ in range(1000):
    # 为模式中的每个字段生成随机值
    film_id = random.randint(1, 1000)
    film_vector = [random.random() for _ in range(5)]
    poster_vector = [random.random() for _ in range(5)]

    # 为每个实体创建一个字典
    entity = {
        "film_id": film_id,
        "filmVector": film_vector,
        "posterVector": poster_vector
    }

    # 将实体添加到列表中
    entities.append(entity)

collection.insert(entities)
