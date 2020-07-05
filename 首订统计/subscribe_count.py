import requests
import time
import bs4

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

#整理书籍信息（需要7.1.txt）
'''
fin=open('7.1.txt',encoding='utf-8')
fout=open('7.1.csv','w',encoding='utf-8')
for line in fin.read().split('\n'):
    if '分类' in line:
        fout.write('分类\t书名\t书号\t作者\n')
    elif '\t' in line:
        info=line.split('\t')
        if len(info)>2:
            fl=info[0]
            info=info[1:]
        if '（' in info[0]:
            name,nid=info[0].split('（')
            nid=int(nid[nid.find(':')+1:nid.rfind('）')])
        else:
            name=info[0]
            nid=search(name)
        author=info[1]
        print('\t'.join([fl,name,str(nid),author]))
        fout.write('\t'.join([fl,name,str(nid),author])+'\n')
fin.close()
fout.close()
'''

#首订统计（需要7.1.csv）
book_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.getvolumelist&nid=%d"
chapter_info="https://www.xrzww.com/wmcms/ajax/index.php?action=novel.getchapterlist&nid=%d&vid=%d"

fout=open('7_1_result.csv','w',encoding='utf-8')
fout.write('分类\t书名\t书号\t作者\t首日总订\t首日最大订\n')
for book in open('7.1.csv',encoding='utf-8').read().split('\n')[1:-1]:
    nid=int(book.split('\t')[2])
    res=br.get(book_info%nid)
    vids=[1]
    for volume in res.json()['data']:
        vids.append(int(volume['volume_id']))
    subcount=0
    m_subcount=0
    for vid in vids:
        res=br.get(chapter_info%(nid,vid))
        if res.json()['data']:
            for chapter in res.json()['data']:
                subcount+=int(chapter['chapter_subcount'])
                if int(chapter['chapter_subcount'])>m_subcount:
                    m_subcount=int(chapter['chapter_subcount'])
    print(book+'\t%d\t%d'%(subcount,m_subcount))
    fout.write(book+'\t%d\t%d\n'%(subcount,m_subcount))
fout.close()