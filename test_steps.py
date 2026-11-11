import json

with open(r'C:\Users\INDIA\.gemini\antigravity-ide\brain\490974d7-9ddd-4d6c-a44a-e0012d181a2c\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(max(0, len(lines)-15), len(lines)):
    obj = json.loads(lines[i])
    t = obj.get('type')
    st = obj.get('status')
    tcs = [tc.get('name') for tc in obj.get('tool_calls', [])]
    content = str(obj.get('content', ''))[:120].replace('\n', ' ')
    print(f"Step {i}: type={t} status={st} tools={tcs} content={content}")
