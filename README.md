# 创建自己的 Notion 论文数据库
### Arxiv 论文信息检索并上传 Notion
- **_简介（代码流程）_**：
  - 首先读取给定 `paper_titles.txt` 文件中的论文标题(_这里也对文件中的论文标题进行去重_)，使用 _Notion Python API_ 读取给定数据库中的所有论文标题，根据数据库中的论文标题进行去重。
  - 然后使用 _Arxiv Python API_ 对去重后的论文标题列表进行检索，将检索到的论文 pdf 下载到 `download_papers` 文件夹中，并将未检索到的论文标题写入 `not_exist.txt` 文件中。
  - 最后使用 _Notion Python API_ 将检索到的论文信息上传到 Notion 数据库中。 
- **_使用方法_**：
  - 创建自己的 _Notion Python API_ 并将给定 `database_id` 和 API 信息写入 `main.py` 文件中
  - 读取一个数据库的数据项，并根据数据项中的数据格式修改 `main.py` 中的 `create_database_item` 函数中的数据库信息格式字典
  - 运行 `main.py` 文件