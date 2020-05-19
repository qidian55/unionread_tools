import requests
import bs4

errors=20
error=0
user_id=1
url='http://unionread.vip/module/user/fhome.php?uid=%d'
br=requests.Session()
f=open('info.csv','w',encoding='utf-8')
f.write('user_id\tuser_name\tuser_sign\tuser_regtime\tuser_logintime\n')
while error<errors and user_id<100:
    try:
        res=br.get(url%user_id,timeout=1).text
    except:
        print('%5d错误'%user_id)
        continue
    if '查看好友资料' in res:
        error=0
        soup=bs4.BeautifulSoup(res,'html.parser')
        user_name=soup.find_all('h2')[-1].text
        user_sign,user_logintime,user_regtime=[str(c.parent.contents[1]) if len(c.parent.contents)>1 else None for c in soup.find_all('em')[-3:]]
        f.write('%s\t%s\t%s\t%s\t%s\n'%(user_id,user_name,user_sign,user_regtime,user_logintime))
    else:
        error+=1
    user_id+=1
    print('user_id:%d\terrors:%d/%d'%(user_id,error,errors),end='\r')
f.close()