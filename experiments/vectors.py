import os
from pathlib import Path

import numpy as np
from paddlespeech.cli.vector import VectorExecutor


def get_vector(path: str, force_yes=True):
    path_obj = Path(path)
    if not os.path.exists(path_obj):
        raise FileNotFoundError("Can't find audio file, please check path:{}".format(path))

    ve = VectorExecutor()
    vec = ve(audio_file=path_obj, force_yes=force_yes)
    del ve

    print(vec[:10])
    return vec


vec1 = get_vector("123_wav.wav")
vec2 = get_vector("进程已退出_wav.wav")


def cosine_similarity(vec1, vec2):
    # 计算余弦相似度
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


similarity = cosine_similarity(vec1, vec2)
print(f'Cosine Similarity: {similarity}')
