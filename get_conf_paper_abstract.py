import arxiv
from tqdm import tqdm


# 提取论文标题
paper_title_list = []
with open('./paper_titles.txt', 'r') as f:
    lines = f.readlines()
    for i in range(0, len(lines), 3):
        paper_title_list.append(lines[i].strip())
paper_title_list = list(set(paper_title_list))

# 通过论文标题搜索论文信息
pub_list = []
not_exist = []
cnt = 0
print('Total:\t' + str(len(paper_title_list)))
for title in tqdm(paper_title_list):
    try:
        search = arxiv.Search(query=title, max_results=100)
        results = list(search.results())
        flag = True
        for result in results:
            if title == result.title:
                summary = result.summary.replace('\n', '')
                pub_list.append((title, summary))
                cnt += 1
                flag = False
                break
        if not flag:
            not_exist.append(title)
    except Exception as e:
        print(e)
        not_exist.append(title)
print('Arxiv Success:\t' + str(cnt) + '/' + str(len(paper_title_list)))

with open('./not_exist.txt', 'w') as f:
    for paper_title in not_exist:
        f.write(paper_title + '\n')


# 写markdown
with open('./paper_summary.md', 'w') as f:
    for paper in tqdm(pub_list):
        f.write('## ' + paper[0] + '\n')
        f.write(paper[1] + '\n')
