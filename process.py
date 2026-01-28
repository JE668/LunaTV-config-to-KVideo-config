import requests
import json
import os

# 定义源链接
URL_JINGJIAN = "https://raw.githubusercontent.com/hafrey1/LunaTV-config/refs/heads/main/jingjian.json"
URL_TEST = "https://raw.githubusercontent.com/rapier15sapper/ew/refs/heads/main/test.json"

# 定义输出文件名
OUTPUT_FILE = "merged.json"

def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def process_data():
    print("开始拉取数据...")
    data_jingjian = fetch_json(URL_JINGJIAN)
    data_test = fetch_json(URL_TEST)

    if data_jingjian is None or data_test is None:
        print("数据拉取失败，终止运行")
        return

    # 1. 处理 test.json (基准数据)
    existing_urls = set()
    current_max_priority = 0
    
    # 确保 data_test 是列表
    if not isinstance(data_test, list):
        print("Test.json 格式错误，应为列表，尝试初始化为空列表")
        data_test = []

    for item in data_test:
        if not isinstance(item, dict):
            continue
        # 获取 URL 用于去重 (去除首尾空格)
        url = item.get("baseUrl", "").strip()
        if url:
            existing_urls.add(url)
        
        # 获取当前最大优先级
        p = item.get("priority", 0)
        if isinstance(p, int) and p > current_max_priority:
            current_max_priority = p

    print(f"Test.json 加载完成，包含 {len(data_test)} 条数据，最大优先级: {current_max_priority}")

    # 2. 处理 jingjian.json 并转换格式
    new_items = []
    
    if isinstance(data_jingjian, dict):
        for key, value in data_jingjian.items():
            # =========== 修复核心开始 ===========
            # 增加类型检查：如果 value 不是字典（比如是版本号 int），则跳过
            if not isinstance(value, dict):
                # 可以在日志里打印跳过的项，方便调试
                # print(f"跳过非字典项: {key}") 
                continue
            # =========== 修复核心结束 ===========

            # 提取关键字段
            api_url = value.get("api", "").strip()
            name = value.get("name", "")
            
            # --- 去重逻辑 ---
            if not api_url or api_url in existing_urls:
                continue
            
            # --- 转换格式逻辑 ---
            current_max_priority += 1
            new_item = {
                "id": key,
                "name": name,
                "baseUrl": api_url,
                "group": "normal",
                "enabled": True,
                "priority": current_max_priority
            }
            
            new_items.append(new_item)
            existing_urls.add(api_url)
    else:
        print("Jingjian.json 格式错误，应为字典")

    print(f"从 Jingjian.json 转换并新增了 {len(new_items)} 条不重复数据")

    # 3. 合并数据
    final_list = data_test + new_items

    # 4. 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
    
    print(f"处理完成！结果已保存到 {OUTPUT_FILE}")

if __name__ == "__main__":
    process_data()
