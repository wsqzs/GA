#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import json
import io

# 强制设置标准输出为 UTF-8，防止 Windows 乱码
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate():
    commit_msg_file = sys.argv[1]

    # 1. 获取 diff 并截断
    try:
        diff = subprocess.check_output(['git', 'diff', '--cached'], stderr=subprocess.STDOUT).decode('utf-8', 'ignore')
        diff = diff[:2000] # 截取前2000个字符
    except Exception:
        return

    if not diff.strip():
        return

    print("正在调用小模型生成中文提交信息...")

    # 2. 调用 Ollama API
    payload = {
        "model": "g itmodel",
        "prompt": f"你是一个代码专家。请根据以下 Git Diff 内容，写一个简短的中文 Commit Message，只需输出一行：\n\n{diff}",
        "stream": False
    }

    try:
        # 使用 powershell 的 curl 或者 python 自带库，这里为了兼容性用 subprocess 调用 curl
        cmd = ['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-d', json.dumps(payload)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = process.communicate(timeout=15)
        
        # 3. 解析结果
        result = json.loads(out.decode('utf-8'))
        ai_msg = result.get('response', '').strip()

        if ai_msg:
            with open(commit_msg_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            with open(commit_msg_file, 'w', encoding='utf-8') as f:
                f.write(f"{ai_msg}\n\n# --- AI Generated ---\n{original_content}")
            print("生成成功！")

    except Exception as e:
        print(f"生成失败: {str(e)}")

if __name__ == "__main__":
    generate()