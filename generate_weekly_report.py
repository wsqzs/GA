import subprocess
import os
from openai import OpenAI  # 需要 pip install openai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def get_git_logs(days=7):
    """获取过去 N 天的提交记录"""
    # 格式：哈希 - 作者 - 提交信息
    cmd = ['git', 'log', f'--since="{days} days ago"', '--pretty=format:%h - %an: %s']
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
    return result.stdout

def generate_report(logs):
    if not logs:
        return "最近没有提交记录。"

    prompt = f"""
    你是一个高级技术文档工程师。请根据以下 Git 提交日志，为我生成一份 Markdown 格式的项目开发周报。
    
    要求：
    1. 语气专业、学术。
    2. 分为 "Feature Highlights" (功能亮点), "Bug Fixes" (修复问题), "Refactoring" (重构) 三个部分。
    3. 如果日志太琐碎，请进行归纳总结，不要流水账。
    
    【Git 日志】：
    {logs}
    """
    
    print("正在发送给云端大模型进行深度总结...")
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # 1. 获取最近 7 天的记录
    logs = get_git_logs(days=7)
    print(f"扫描到以下提交记录:\n{logs}\n{'-'*30}")
    
    # 2. 生成文档
    if logs:
        report = generate_report(logs)
        
        # 3. 保存结果
        with open("WEEKLY_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)
        print("文档已生成：WEEKLY_REPORT.md")
    else:
        print("没找到提交记录，不用写周报了！")
        print("提示：请确保你在一个 Git 仓库内，并且最近有提交记录。")