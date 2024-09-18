# aa の analysis

## scripts

- video2audio.py
- denoise_audio.py
- long_audio_transcribe.py
  - 使用 Whisper 模型进行转录,分割并标注长音频, 生成 long_character_anno.txt
  - --languages：指定支持的语言（例如 CJE 表示中文、日文和英文）
  - --whisper_size：指定 Whisper 模型的大小（例如 large
  - long_character_anno.txt: <音频片段路径>|<说话者名字>|<转录文本>
    - eg.
      ```c
      ./segmented_character_voice/speaker1/speaker1_001_0.wav|speaker1|[ZH]你好[ZH]
      ./segmented_character_voice/speaker1/speaker1_001_1.wav|speaker1|[JA]こんにちは[JA]
      ./segmented_character_voice/speaker1/speaker1_001_2.wav|speaker1|[EN]Hello[EN]
      ```
- short_audio_transcribe.py
  - 使用 Whisper 模型进行转录，并生成对应的标注文件 short_character_anno.txt
  - --languages：指定支持的语言（例如 CJE 表示中文、日文和英文）
  - --whisper_size：指定 Whisper 模型的大小（例如 large
  -short_character_anno.txt : <音频片段路径>|<说话者名字>|<转录文本>
    - eg.
      ```c
      ./segmented_character_voice/speaker1/speaker1_001_0.wav|speaker1|[ZH]你好[ZH]
      ./segmented_character_voice/speaker1/speaker1_001_1.wav|speaker1|[JA]こんにちは[JA]
      ./segmented_character_voice/speaker1/speaker1_001_2.wav|speaker1|[EN]Hello[EN]
      ```
- preprocess_v2.py
  - 将两个格式相同的标注文件（short_character_anno.txt 和 long_character_anno.txt）整合成一个，并拆分成训练和验证数据集，同时修改配置文件，为训练（微调）做准备
  - sys.setrecursionlimit(500000)：设置递归深度，以避免递归深度超限错误
  - 解析命令行参数
    - --add_auxiliary_data：是否添加额外的数据作为微调辅助
    - --languages：指定支持的语言（例如 CJE 表示中文、日文和英文）
  - 读取标注文件
    - 读取 short_character_anno.txt 和 long_character_anno.txt 文件中的标注数据，并将其合并到 new_annos 列表中
  - 遍历 new_annos 列表，提取说话者名字，并存储在 speakers 列表中
  - 可选：添加额外的辅助数据
    - 如果指定了 --add_auxiliary_data 参数，则读取 sampled_audio4ft.txt 文件中的标注数据，并根据支持的语言进行过滤
    - 将过滤后的标注数据合并到 new_annos 列表中，并更新 speakers 列表
  - 修改配置文件
    - 读取 finetune_speaker.json 配置文件，修改其中的 n_speakers 和 speakers 字段，并保存为 modified_finetune_speaker.json
  - 清理标注数据
    - 遍历 new_annos 列表，清理文本数据，并将说话者名字替换为分配的说话者 ID
    - 如果指定了 --add_auxiliary_data 参数，则还会清理 old_annos 列表中的标注数据
  - 合并标注数据
    - 将清理后的新标注数据和旧标注数据合并，生成最终的标注数据 final_annos
  - 保存标注数据
    - 将最终的标注数据保存为 final_annotation_train.txt 和 final_annotation_val.txt 文件
