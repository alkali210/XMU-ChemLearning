# 转换目录下的文件编码从gbk到utf8. 如果文件在utf8编码下已经能正常显示, 不要运行这个脚本

import os

def convert_to_utf8(file):
    print(f"Processing {file} ...")
    with open(file, 'r', encoding='gbk') as f:
        content = f.read()
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
if __name__ == "__main__":
    fileslist = os.walk('.')
    for root, dirs, files in fileslist:
        for file in files:
            if file.endswith('.c'):
                convert_to_utf8(os.path.join(root, file))
    print("Done!")