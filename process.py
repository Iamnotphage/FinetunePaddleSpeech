import os
import re
from pathlib import Path
from pypinyin import pinyin, Style

def generate_pinyin_labels(data_dir="./jinxi", output_file="./jinxi/labels.txt"):
    data_path = Path(data_dir)
    lab_files = sorted(data_path.glob("*.lab"))

    results = []
    # 过滤掉标点，只留汉字
    zh_pattern = re.compile(r'[\u4e00-\u9fa5]')

    for lab_file in lab_files:
        file_id = lab_file.stem
        try:
            with open(lab_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                chinese_chars = "".join(zh_pattern.findall(content))
                
                # 获取拼音
                py_list = pinyin(chinese_chars, style=Style.TONE3)
                
                final_py = []
                for item in py_list:
                    p = item[0].lower()
                    # 关键逻辑：如果拼音末尾不是数字，说明是轻声，强制加 5
                    if not p[-1].isdigit():
                        p = p + "5"
                    
                    # 针对 n2 的手动修正逻辑
                    if p == "n2":
                        p = "en2"

                    final_py.append(p)
                
                py_str = " ".join(final_py)
                if py_str.strip():
                    results.append(f"{file_id}|{py_str}")
                
        except Exception as e:
            print(f"处理 {lab_file.name} 出错: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    print(f"处理完毕")

if __name__ == "__main__":
    generate_pinyin_labels()