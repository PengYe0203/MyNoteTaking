import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 尝试在项目根加载 .env（确保无论 cwd 在哪都能找到）
ROOT = Path(__file__).resolve().parent.parent
env_path = ROOT / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    # 仍然尝试默认位置
    load_dotenv()

# 优先兼容两个常见变量名
token = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
if not token:
    print("Missing API token. Set GITHUB_TOKEN or OPENAI_API_KEY in your environment or create a .env in project root.")
    raise SystemExit(1)

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

# A function to call an LLM model and return the response
def call_llm_model(model_name, messages, temperature=1.0, top_p=1.0):
    client = OpenAI(base_url=endpoint, api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model_name
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("LLM module loaded. Token present:", "yes")