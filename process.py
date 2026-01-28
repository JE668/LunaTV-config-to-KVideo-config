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
    # 这一步建立一个已有URL的集合，用于后续去重
    existing_urls = set()
    current_max_priority = 0
    
    # 确保 data_test 是列表
    if not isinstance(data_test, list):
        print("Test.json 格式错误，应为列表")
        data_test = []

    for item in data_test:
        # 获取 URL 用于去重 (去除首尾空格)
        url = item.get("baseUrl", "").strip()
        if url:
            existing_urls.add(url)
        
        # 获取当前最大优先级，以便后续追加
        p = item.get("priority", 0)
        if isinstance(p, int) and p > current_max_priority:
            current_max_priority = p

    print(f"Test.json 加载完成，包含 {len(data_test)} 条数据，最大优先级: {current_max_priority}")

    # 2. 处理 jingjian.json 并转换格式
    new_items = []
    
    # 确保 data_jingjian 是字典
    if isinstance(data_jingjian, dict):
        for key, value in data_jingjian.items():
            # 提取关键字段
            api_url = value.get("api", "").strip()
            name = value.get("name", "")
            
            # --- 去重逻辑 ---
            # 如果这个 API 地址已经在 test.json 里存在，则跳过
            if not api_url or api_url in existing_urls:
                continue
            
            # --- 转换格式逻辑 ---
            current_max_priority += 1
            new_item = {
                "id": key,  # 使用原数据的 key (域名) 作为 id
                "name": name,
                "baseUrl": api_url,
                "group": "normal",
                "enabled": True,
                "priority": current_max_priority
            }
            
            new_items.append(new_item)
            # 添加到集合中，防止 jingjian.json 内部也有重复
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
