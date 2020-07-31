import pandas as pd
import numpy as np
import requests
import time
import bs4
import os

br=requests.Session()

def search(key):
    global a,soup
    url="https://www.xrzww.com/module/novel/search.php?key=%s"%key
    res='频繁刷新'
    while '频繁刷新' in res:
        res=br.get(url).text
    soup=bs4.BeautifulSoup(res,'html.parser')
    for a in soup.find_all(class_='mod_book_cover db'):
        if a['title']==key:
            return int(a['href'].split('=')[-1])

def getNovelInfo(nid):
    res=br.get(book_info%nid)
    vids=[1]
    for volume in res.json()['data']:
        vids.append(int(volume['volume_id']))
    for vid in vids:
        res=br.get(volume_info%(nid,vid))
        if res.json()['data']:
            cid=int(res.json()['data'][0]['chapter_id'])
            res=br.get(chapter_info%cid)
            tid=int(res.json()['data']['type_id'])
            aid=int(res.json()['data']['author_id'])
            res=br.get('https://www.xrzww.com/module/novel/info.php?tid=%d&nid=%d&pt=m'%(tid,nid))
            soup=bs4.BeautifulSoup(res.text,'html.parser')
            fl=soup.find(class_='in_textone_type').text[1:-1]
            author=soup.find(class_='in_texttwo').text[3:]
            return fl,author


book_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.getvolumelist&nid=%d"
volume_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.getchapterlist&nid=%d&vid=%d"
chapter_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.getchapter&cid=%d"
type_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.gettype&tid=%d"

tids={}
for i in range(1,20):
    res=br.get(type_info%i).json()
    if res['data']:
        tids[res['data']['type_name']]=i

count_data=['8','1']
info_txt='_'.join(count_data)+'.txt'
info_csv='_'.join(count_data)+'.csv'
result_csv='_'.join(count_data)+'_result.csv'

#生成规则书籍信息
if not os.path.exists(info_csv):
    df=pd.read_csv(info_txt,sep='\t')
    fout=open(info_csv,'w',encoding='utf-8')
    fout.write('分类\t书名\t书号\t作者\n')
    for index,row in df.iterrows():
        name=row['书名']
        if '书号' in row:
            nid=row['书号']
        else:
            nid=search(name)
        fl=row['分类'].replace('二次元','轻小说').replace('女频','女生频道')
        if '作者' in row:
            author=row['作者']
        else:
            _,author=getNovelInfo(nid)
        print('%s\t%s\t%d\t%s'%(fl,name,nid,author))
        fout.write('%s\t%s\t%d\t%s\n'%(fl,name,nid,author))
    fout.close()

if not os.path.exists(result_csv):
    df=pd.read_csv(info_csv,sep='\t')
    fout=open(result_csv,'w',encoding='utf-8')
    #fout.write('分类\t书名\t书号\t首日总订\t首日最高订\t首日均订\n')
    fout.write('分类\t书名\t书号\t作者\t首日总订\t首日最高订\t首日均订\n')
    for index,row in df.iterrows():
        fl=row['分类']
        name=row['书名']
        nid=row['书号']
        author=row['作者']
        res=br.get(book_info%nid)
        vids=[1]
        for volume in res.json()['data']:
            vids.append(int(volume['volume_id']))
        subcounts=[]
        for vid in vids:
            res=br.get(volume_info%(nid,vid))
            if res.json()['data']:
                for chapter in res.json()['data']:
                    if int(chapter['chapter_ispay']):
                        subcounts.append(int(chapter['chapter_subcount']))
        if len(subcounts):
            print('%s\t%s\t%d\t%d\t%s\t%d\t%.2f'%(fl,name,nid,author,sum(subcounts),max(subcounts),np.mean(subcounts)))
            fout.write('%s\t%s\t%d\t%s\t%d\t%d\t%.2f\n'%(fl,name,nid,author,sum(subcounts),max(subcounts),np.mean(subcounts)))
        else:
            print('%s\t%s\t%d\t%s\tNaN\tNaN\tNaN'%(fl,name,nid,author))
            fout.write('%s\t%s\t%d\t%s\tNaN\tNaN\tNaN\n'%(fl,name,nid,author))
    fout.close()