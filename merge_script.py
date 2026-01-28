import json
import requests
from urllib.parse import urlparse

def fetch_json(url):
    """从URL获取JSON数据"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def transform_jingjian_data(jingjian_data):
    """转换jingjian.json数据格式"""
    transformed = []
    
    if not jingjian_data:
        return transformed
    
    for key, value in jingjian_data.items():
        # 使用域名作为ID，将点替换为下划线
        resource_id = key.replace('.', '_')
        
        # 创建新的格式
        transformed_item = {
            "id": resource_id,
            "name": value.get("name", ""),
            "baseUrl": value.get("api", ""),
            "group": "normal",
            "enabled": True,
            "priority": 2  # 默认优先级
        }
        
        # 过滤掉无效数据
        if transformed_item["name"] and transformed_item["baseUrl"]:
            transformed.append(transformed_item)
    
    return transformed

def merge_json_data(jingjian_transformed, test_data):
    """合并两个JSON数组，test.json优先"""
    if not test_data:
        test_data = []
    
    if not jingjian_transformed:
        return test_data
    
    # 创建字典以便快速查找
    result_dict = {}
    
    # 首先添加jingjian的数据
    for item in jingjian_transformed:
        result_dict[item["id"]] = item
    
    # 然后用test.json的数据覆盖（test.json优先）
    for item in test_data:
        if isinstance(item, dict) and "id" in item:
            result_dict[item["id"]] = item
    
    # 转回列表并按id排序
    result_list = list(result_dict.values())
    result_list.sort(key=lambda x: x.get("id", ""))
    
    return result_list

def main():
    # 定义URL
    jingjian_url = "https://raw.githubusercontent.com/hafrey1/LunaTV-config/refs/heads/main/jingjian.json"
    test_url = "https://raw.githubusercontent.com/rapier15sapper/ew/refs/heads/main/test.json"
    
    print("开始获取数据...")
    
    # 获取数据
    jingjian_data = fetch_json(jingjian_url)
    test_data = fetch_json(test_url)
    
    if jingjian_data is None:
        print("无法获取jingjian.json数据")
        return
    
    if test_data is None:
        print("无法获取test.json数据")
        # 如果没有test数据，使用空数组
        test_data = []
    
    print(f"获取到jingjian.json数据: {len(jingjian_data)}项")
    print(f"获取到test.json数据: {len(test_data) if isinstance(test_data, list) else 0}项")
    
    # 转换jingjian数据
    jingjian_transformed = transform_jingjian_data(jingjian_data)
    print(f"转换后jingjian数据: {len(jingjian_transformed)}项")
    
    # 合并数据
    merged_data = merge_json_data(jingjian_transformed, test_data)
    print(f"合并后总数据: {len(merged_data)}项")
    
    # 保存到文件
    with open('merged.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    
    print("数据已保存到 merged.json")
    
    # 打印一些示例
    print("\n示例数据（前3项）:")
    for i, item in enumerate(merged_data[:3]):
        print(f"{i+1}. {item}")

if __name__ == "__main__":
    main()
