import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import precision_score, f1_score, accuracy_score
from sklearn.metrics import recall_score
from tqdm import tqdm


# Step 1: 加载数据集
def load_dataset(file_path):
    df = pd.read_csv(file_path, sep='\t')
    print(df.head(5))
    return df


# Step 2: 计算相似度
def compute_similarity(model, sentence1, sentence2):
    # 生成句子嵌入
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)

    # 计算余弦相似度
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    return cosine_scores.item()


def evaluate_model(file_path, threshold=0.5):
    # 加载预训练模型
    model = SentenceTransformer('./sbert-lcqmc-finetuned')

    # 加载数据集
    dataset = load_dataset(file_path)

    # 存储真实标签和预测标签
    true_labels = []
    predicted_labels = []

    # 遍历数据集并计算相似度
    for index, row in tqdm(dataset.iterrows(), total=len(dataset)):
        query = row['text_a']
        answer = row['text_b']
        label = row['label']

        # 计算相似度
        similarity = compute_similarity(model, query, answer)

        # 基于相似度阈值的预测标签
        predicted_label = 1 if similarity > threshold else 0
        # if int(label) != int(predicted_label):
            # print(f"{index}\t{query}\t{answer}\t{similarity}\t{predicted_label}\t{label}")
        # 保存真实标签和预测标签
        true_labels.append(int(label))
        predicted_labels.append(predicted_label)

    # 计算基本四项分数
    precision = precision_score(true_labels, predicted_labels)
    recall = recall_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels)
    accuracy = accuracy_score(true_labels, predicted_labels)

    # 打印评估结果
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1-Score: {f1:.4f}')
    print(f'Accuracy: {accuracy:.4f}')


# 示例调用
file_path = 'lcqmc_test.txt'
evaluate_model(file_path, threshold=0.9)  # 阈值可以调整
