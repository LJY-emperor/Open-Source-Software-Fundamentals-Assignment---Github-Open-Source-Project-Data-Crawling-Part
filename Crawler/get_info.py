import requests
import os
import certifi
import base64
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# 设置全局字体为SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def get_repo_info(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch repository information (status code {response.status_code})")
        return None


# 获取仓库的基本信息
owner = "beeware"
# repo = "beeware"
repo = "toga"
repo_info = get_repo_info(owner, repo)



if repo_info:
    print("beeware仓库信息：")
    print("仓库名称:", repo_info['name'])
    print("仓库描述:", repo_info['description'])
    print("创建日期:", repo_info['created_at'])
    print("语言:", repo_info['language'])
    print("星标数量:", repo_info['stargazers_count'])
    print("Fork数量:", repo_info['forks_count'])


def parse_repo_info(repo_info):
    repo_data = {
        'name': repo_info['name'],
        'description': repo_info['description'],
        'created_at': repo_info['created_at'],
        'language': repo_info['language'],
        'stargazers_count': repo_info['stargazers_count'],
        'forks_count': repo_info['forks_count']
    }
    return repo_data


# 解析仓库信息
repo_data = parse_repo_info(repo_info)
print("仓库信息（json）:")
print(repo_data)


def get_repo_files(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch repository files (status code {response.status_code})")
        return None


# 获取仓库中的文件列表
repo_files = get_repo_files(owner, repo)

# 显示文件信息
if repo_files:
    print("仓库文件：")
    for file in repo_files:
        print(file['name'], file['size'])




def get_file_content(owner, repo, file_path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        file_info = response.json()
        content = base64.b64decode(file_info['content']).decode('utf-8')
        return content
    else:
        print(f"Error: Unable to fetch file content (status code {response.status_code})")
        return None


# 获取某个文件的内容
file_path = 'README.rst'  # 示例文件路径
file_content = get_file_content(owner, repo, file_path)
if file_content:
    print("README内容：")
    print(file_content[:200])  # 打印前200个字符


def get_contributors(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch contributors data (status code {response.status_code})")
        return None


# 获取贡献者数据
contributors = get_contributors(owner, repo)

# 显示贡献者信息
if contributors:
    print("贡献者信息：")
    for contributor in contributors:
        print(contributor['login'], contributor['contributions'])




def parse_contributors(contributors):
    data = []
    for contributor in contributors:
        data.append({
            'username': contributor['login'],
            'contributions': contributor['contributions']
        })

    return pd.DataFrame(data)


# 解析贡献者数据
contributors_df = parse_contributors(contributors)
print("贡献者数据：")
print(contributors_df)

'''
def get_commits(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch commits data (status code {response.status_code})")
        return None


# 获取提交记录
commits = get_commits(owner, repo)
'''

'''
# 翻页
def get_all_commits(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    all_commits = []
    while url:
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            commits_page = response.json()
            if not commits_page:  # 如果当前页面为空，结束循环
                break
            all_commits.extend(commits_page)

            # 获取分页信息
            link_header = response.headers.get('Link')
            if link_header:
                links = link_header.split(', ')
                url = None
                for link in links:
                    (link_url, link_rel) = link.split('; ')
                    if 'next' in link_rel and 'rel="next"' in link_rel:
                        url = link_url.strip('<>')
                        break
            else:
                url = None  # 如果没有更多的分页，则停止
        else:
            print(f"Error: Unable to fetch commits data (status code {response.status_code})")
            url = None  # 结束循环

    return all_commits
'''

'''
def get_all_commits(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    all_commits = []
    headers = {'User-Agent': 'Mozilla/5.0'}  # 必须包含 User-Agent

    page = 1  # 从第一页开始
    per_page = 100  # 每页返回100条记录（最大100条）

    while True:
        params = {'page': page, 'per_page': per_page}  # 添加分页参数
        response = requests.get(url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            commits_page = response.json()
            if not commits_page:  # 如果当前页面为空，结束循环
                break
            all_commits.extend(commits_page)

            # 如果获取到的提交数量小于per_page，说明已经没有更多提交了
            if len(commits_page) < per_page:
                break
            page += 1  # 继续获取下一页

        else:
            print(f"Error: Unable to fetch commits data (status code {response.status_code})")
            break  # 如果遇到错误，结束循环

    return all_commits
'''

def get_all_commits(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    all_commits = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 起始日期和结束日期
    start_date = datetime(2018, 8, 1)  # 根据实际情况设定
    end_date = datetime.now()

    # 每次请求的时间窗口大小
    window_size = timedelta(days=100)  # 设置为30天

    while start_date < end_date:
        since = start_date.isoformat()
        until = (start_date + window_size).isoformat()

        params = {'since': since, 'until': until, 'per_page': 100}
        response = requests.get(url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            commits_page = response.json()
            if not commits_page:  # 如果当前页面为空，结束循环
                break
            all_commits.extend(commits_page)
            start_date += window_size  # 继续拉取下一个时间窗口
        else:
            print(f"Error: Unable to fetch commits data (status code {response.status_code})")
            break  # 结束循环

    return all_commits



# 使用示例
commits = get_all_commits(owner, repo)

# 显示提交信息
if commits:
    print("历史提交信息：")
    for commit in commits:
        print(commit['commit']['author']['name'], commit['commit']['message'], commit['commit']['author']['date'])


def parse_commits(commits):
    data = []
    for commit in commits:
        data.append({
            'author': commit['commit']['author']['name'],
            'message': commit['commit']['message'],
            'date': commit['commit']['author']['date']
        })

    return pd.DataFrame(data)


# 解析提交记录
commits_df = parse_commits(commits)
print(commits_df)




def plot_contributions(contributors_df):
    plt.bar(contributors_df['username'], contributors_df['contributions'])
    plt.xticks(rotation=90)
    plt.xlabel('贡献者')
    plt.ylabel('贡献次数')
    plt.title('GitHub仓库贡献者贡献次数')
    plt.show()


# 绘制贡献者贡献次数图
plot_contributions(contributors_df)


def plot_commits_over_time(commits_df):
    commits_df['date'] = pd.to_datetime(commits_df['date'])
    commits_df.set_index('date', inplace=True)
    commits_df.resample('M').size().plot()
    plt.title('GitHub提交记录的时间分布')
    plt.xlabel('日期')
    plt.ylabel('提交数量')
    plt.show()


# 绘制提交记录的时间分布图
plot_commits_over_time(commits_df)