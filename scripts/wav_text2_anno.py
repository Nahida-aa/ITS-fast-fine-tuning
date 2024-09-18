import os

# 定义音频文件和标注文件所在的目录
audio_dir = "./paimon"
output_file = "short_character_anno.txt"

# 获取目录中的所有文件 （包括子目录吗: 不包括）
files = os.listdir(audio_dir)

# 过滤出 .wav 和 .lab 文件
wav_files = [f for f in files if f.endswith('.wav')]
lab_files = [f for f in files if f.endswith('.lab')]

# 确保每个 .wav 文件都有对应的 .lab 文件
assert len(wav_files) == len(lab_files), "每个 .wav 文件必须有对应的 .lab 文件"

# 打开输出文件
with open(output_file, 'w', encoding='utf-8') as out_f:
    # 遍历 .wav 文件
    for wav_file in wav_files:
        # 获取对应的 .lab 文件名
        lab_file = wav_file.replace('.wav', '.lab')
        
        # 读取 .lab 文件中的文本内容
        with open(os.path.join(audio_dir, lab_file), 'r', encoding='utf-8') as lab_f:
            text = lab_f.read().strip()
        
        # 加上 [ZH] 标签
        text = f"[ZH]{text}[ZH]"
        
        # 获取说话者名字（假设文件名格式为 vo_ABDLQ001_1_paimon_01.wav）
        speaker = wav_file.split('_')[3]
        
        # 写入到输出文件
        out_f.write(f"{os.path.join(audio_dir, wav_file)}|{speaker}|{text}\n")

print(f"生成 {output_file} 文件成功")