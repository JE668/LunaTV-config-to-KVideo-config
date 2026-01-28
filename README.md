# 📺 TVBox 影视源配置自动合并 (Auto-Merge Config)

[![Update JSON Config](https://github.com/JE668/LunaTV-config-to-KVideo-config/actions/workflows/update_json.yml/badge.svg)](https://github.com/JE668/LunaTV-config-to-KVideo-config/actions/workflows/update_json.yml)

本项目利用 **GitHub Actions** 每天自动拉取、转换、去重并合并影视配置接口数据，生成适用于 TVBox/KVideo 等影视软件的标准 JSON 订阅文件。

## ✨ 项目特性

1.  **多源合并**：自动从多个上游仓库拉取 JSON 配置。
2.  **格式转换**：将 `jingjian.json` 的字典格式自动转换为列表格式（适配 TVBox 标准）。
3.  **智能去重**：
    *   以 `baseUrl`（API 地址）为去重标准。
    *   **保留策略**：若数据重复，严格保留基准文件 (`test.json`) 中的配置，忽略新转换的数据。
4.  **自动排序**：自动识别现有数据的最大 `priority`（优先级），并为新加入的源自动生成递增的优先级序号。
5.  **定时更新**：每天北京时间早上 08:00 自动运行，保持数据最新。

## 🛠️ 数据处理逻辑

脚本 (`process.py`) 按照以下逻辑处理数据：

### 1. 数据源
*   **基准数据 (Primary)**: [test.json](https://raw.githubusercontent.com/rapier15sapper/ew/refs/heads/main/test.json)
    *   *作为主库，所有数据均保留。*
*   **补充数据 (Secondary)**: [jingjian.json](https://raw.githubusercontent.com/hafrey1/LunaTV-config/refs/heads/main/jingjian.json)
    *   *作为补充库，需进行格式转换。*

### 2. 转换规则
将 `jingjian.json` 中的数据按如下映射转换：

| 目标字段 | 来源字段/逻辑 | 备注 |
| :--- | :--- | :--- |
| `id` | 原数据的 Key (如 `iqiyizyapi.com`) | 保证唯一性 |
| `name` | `name` | 显示名称 |
| `baseUrl`| `api` | 核心 API 地址 |
| `priority`| 自动计算 | 在 `test.json` 最大值基础上递增 |
| `group` | 固定为 `"normal"` | |

### 3. 去重逻辑
*   程序会优先加载 `test.json` 中的所有 `baseUrl`。
*   在处理 `jingjian.json` 时，如果发现其 `api` 地址已存在于基准数据中，**该条目将被丢弃**。
*   如果 `jingjian.json` 中包含非字典格式的元数据（如版本号），程序会自动跳过，防止报错。

## 🚀 使用方法

### 获取订阅链接
合并后的文件名为 `merged.json`。你可以直接在电视盒子或影视 APP 中使用以下链接：

```text
https://gh.llkk.cc/https://raw.githubusercontent.com/JE668/LunaTV-config-to-KVideo-config/refs/heads/main/merged.json
