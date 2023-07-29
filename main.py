from notion_client import Client
import arxiv
import os

# 会议列表，检索论文元信息comment的会议信息只会检测列表中存在的信息
conference_list = ['Findings of ACL', 'Findings of EMNLP', 'NAACL', 'EMNLP', 'ACL', 'ICLR', 'IJCAI', 'COLING', 'ICML',
                   'AAAI', 'TKDE', 'ICDE', 'SIGIR', 'WWW', 'ICBK', 'NIPS', 'ECML-PKDD', 'CIKM', 'ECAI']

# 提取文件中的论文标题
paper_title_list = []
with open('./paper_titles.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        paper_title_list.append(line.strip())
paper_title_list = list(set(paper_title_list))


# 通过给定arxiv返回的论文信息列表，将信息处理成notionAPI所需的json格式
def create_database_item(result_list):
    item_list = []
    for result in result_list:
        title = result.title

        # 根据会议列表提取comment中的会议信息
        comment = result.comment
        conference_journal = ''
        if comment is not None:
            for conference in conference_list:
                if conference in comment:
                    conference_journal = conference
                    break

        published_time = result.published.strftime('%Y-%m-%d')
        author_list = []
        for author in result.authors:
            author_list.append({"name": author.name})

        if conference_journal == '':
            item = {
                "Released Time": {
                    "id": "OOMq",
                    "type": "date",
                    "date": {
                        "start": published_time,
                        "end": None,
                        "time_zone": None
                    }
                },
                "Authors": {
                    "id": "oxTf",
                    "type": "multi_select",
                    "multi_select": author_list
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title,
                                "link": None
                            },
                        }
                    ]
                },
                "Status": {
                    "id": "4ce1d113-e2a6-47f2-b147-6934dcd09d6b",
                    "type": "status",
                    "status": {
                        "id": "e8b8656a-8280-4cb2-88e8-5ab9512caaea",
                        "name": "Not started",
                        "color": "default"
                    }
                }
            }
        else:
            item = {
                "Conference/Journal": {
                    "id": "M%3DpH",
                    "type": "select",
                    "select": {
                        "name": conference_journal,
                    }
                },
                "Released Time": {
                    "id": "OOMq",
                    "type": "date",
                    "date": {
                        "start": published_time,
                        "end": None,
                        "time_zone": None
                    }
                },
                "Authors": {
                    "id": "oxTf",
                    "type": "multi_select",
                    "multi_select": author_list
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title,
                                "link": None
                            },
                        }
                    ]
                },
                "Status": {
                    "id": "4ce1d113-e2a6-47f2-b147-6934dcd09d6b",
                    "type": "status",
                    "status": {
                        "id": "e8b8656a-8280-4cb2-88e8-5ab9512caaea",
                        "name": "Not started",
                        "color": "default"
                    }
                }
            }
        item_list.append(item)
    return item_list


# 创建notion API和初始化API所需的信息
paper_manager_TOKEN = ''
database_id = ''
database_URL = ''
notion = Client(auth=paper_manager_TOKEN)
parent = {
    'type': 'database_id',
    'database_id': database_id
}
icon = {
    'type': 'emoji',
    'emoji': '📖'
}

# 检索给定notion数据库，根据数据库中存在的论文标题去重，删除已经存在在数据库中给定标题
exist_paper_name_list = []
exist_list = notion.databases.query(database_id=database_id)['results']
for item in exist_list:
    name = item['properties']['Name']['title'][0]['text']['content']
    name = name.strip()
    name = name.replace('\n', ' ')
    exist_paper_name_list.append(name)
to_add_list = []
for title in paper_title_list:
    if title not in exist_paper_name_list:
        to_add_list.append(title)

# 通过去重后的论文标题使用arxiv API搜索论文信息并下载论文的pdf文件到制定文件夹
# 并将未检索到的论文标题写入到not_exist.txt文件中
if not os.path.exists('./download_papers'):
    os.mkdir('./download_papers')
pub_list = []
cnt_founded = 0
cnt_total = 0
not_found_list = []
print('Total:\t' + str(len(to_add_list)))
for title in to_add_list:
    cnt_total += 1
    print(str(cnt_total) + '/' + str(len(to_add_list)) + '：\t' + title)
    search = arxiv.Search(query=title, max_results=100)
    results = list(search.results())
    flag = True
    for result in results:
        if title == result.title:
            pub_list.append(result)
            result.download_pdf(dirpath="./download_papers")
            cnt_founded += 1
            flag = False
            break
    if flag:
        print('False')
        not_found_list.append(title)
print('Arxiv Success:\t' + str(cnt_founded) + '/' + str(len(to_add_list)))
with open('./not_exist.txt', 'w') as f:
    f.writelines(not_found_list)

# 通过API上传论文信息
item_list = create_database_item(pub_list)
for item in item_list:
    notion.pages.create(parent=parent, properties=item, icon=icon)
