from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import csv
import os

# 超参数设置
EPOCHS = 6  # 训练轮次
BATCH_SIZE = 16  # 每批次的样本数
LEARNING_RATE = 2e-5  # 学习率
WARMUP_STEPS = 100  # 预热步数
OUTPUT_PATH = 'output/sbert-lcqmc-finetuned'  # 模型输出路径
LCQMC_DATA_PATH = '../data/lcqmc/lcqmc_dev.txt'  # LCQMC数据集路径
MAX_SEQ_LENGTH = 128  # 最大序列长度

# 1. 加载预训练模型
model = SentenceTransformer('../../../action/bert_models/paraphrase-multilingual-MiniLM-L12-v2')

# 2. 加载 LCQMC 数据集
def load_lcqmc_data(file_path):
    examples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row[2] != 'label':
                text_a, text_b, label = row[0], row[1], int(row[2])
                examples.append(InputExample(texts=[text_a, text_b], label=label))
    return examples


# 加载 LCQMC 训练数据
train_examples = load_lcqmc_data(LCQMC_DATA_PATH)

# 3. 创建数据加载器
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)

# 4. 定义损失函数
train_loss = losses.CosineSimilarityLoss(model=model)

# 5. 模型微调
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=EPOCHS,
    warmup_steps=WARMUP_STEPS,
    output_path=OUTPUT_PATH
)

# 6. 微调后的模型保存并可用于推理
model = SentenceTransformer(OUTPUT_PATH)

# 示例推理
sentences = ['这是一个测试句子', '这是另一个测试句子']
embeddings = model.encode(sentences[0])
embeddings = model.encode(sentences[0])
print(embeddings)
