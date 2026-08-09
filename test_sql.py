from pymilvus import connections

import config
from dao import MilvusClient

milvus_client = MilvusClient(config.Milvus.host, config.Milvus.port)
dao = milvus_client.get_dao(config.AUDIO_TABLE)
print(connections.get_server_version())
