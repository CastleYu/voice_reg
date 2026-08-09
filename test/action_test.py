import config
from action.action_matcher import *

# 测试数据（系统指令对应多个用户指令）
with open('unique_kv.json', 'r', encoding='utf8') as f:
    data = json.load(f)
    print(data)

# 系统指令列表（将 JSON 的 key 作为系统指令）
system_instructions = list(data.keys())

matcher = InstructionMatcher(config.Model.ModelDir).load(MicomlMatcher('paraphrase-multilingual-MiniLM-L12-v2'))

# 缓存系统指令的向量（这里直接缓存到内存中，不存盘）
matcher.cached_instructions = system_instructions
matcher.cached_embeddings = np.array(matcher._matcher._model_bert.encode(system_instructions))

# 对每个用户查询进行匹配，并打印匹配结果
match_results = {}
print("=== 匹配结果 ===")
for category, queries in data.items():
    print(f"\n【系统指令：{category}】")
    match_results[category] = []
    for query in queries:
        matched_instruction, score = matcher.match(query, system_instructions)
        print(f"用户查询：{query}")
        print(f"匹配到的系统指令：{matched_instruction}，相似度分数：{score}\n")
        match_results[category].append((query, matched_instruction, score))

# 统计样本分布数量：每个系统指令匹配到的次数
distribution = {}
for category, results in match_results.items():
    for query, matched_instruction, score in results:
        distribution[matched_instruction] = distribution.get(matched_instruction, 0) + 1

print("=== 测试结果样本分布数量 ===")
for instr, count in distribution.items():
    print(f"{instr}: {count}")
