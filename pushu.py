import requests
from bs4 import BeautifulSoup 
import jieba

pushu_url='http://www.xiami.com/artist/album-IOd0c43?spm=a1z1s.6659509.6856549.3.p4Tsid';
host='http://www.xiami.com'

headers={
         'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}


def get_html(url):
    '''获取指定url的页面，返回经过处理后的html页面'''
    s=requests.session()
    response=s.get(url,headers=headers);
    bs_html=BeautifulSoup(response.text,'lxml')
    return bs_html

def get_album(url):
    '''获取所有的专辑url，传入页面的参数'''
    bsHtml=get_html(url)
    albumUrl=bsHtml.select('div.detail p.name a')
    Albums=[]
    for item in albumUrl:
        album={}
        album['href']=host+item['href']
        album['title']=item['title']
        Albums.append(album)
    return Albums

def is_song(a):
    '''判断是否是歌的链接'''
    return not a.has_attr('class')

def get_song(url):
    ''' 获取某专辑所有的歌的url,传入的是专辑的url'''
    albumHtml=get_html(url)
    songs=albumHtml.select('td.song_name a')
    songs=filter(is_song,songs)
    song=[]
    for i in songs:
        item={}
        item['href']=host+i['href']
        item['text']=i.text
        song.append(item)    
    return song

def get_song_lyric(url):
    '''获取歌的歌词，传入的是歌的url'''
    lyric_html=get_html(url)
    AllLyric=lyric_html.select('div.lrc_main')
    try:
        return AllLyric[0].text
    except IndexError:
        return ''

def tokenize(str):
    ''' 结巴分词，对输入参数str进行分词，返回分词后的结果'''
    seg_list=jieba.cut(str,cut_all=True)
    for word in seg_list:
        if(words.__contains__(word)):
            words[word]=words[word]+1
        else:
            words[word]=1

words={}

if __name__=='__main__':
    '''不作为模块名的时候运行'''
    count=0                                # 记录总的歌曲数
    albumUrls=get_album(pushu_url)
    for i in albumUrls:  
        Allsongs=get_song(i['href'])
        for j in Allsongs:
            lyric=get_song_lyric(j['href'])
            tokenize(lyric)
            count+=1            
    order_words=sorted(words.items(),key=lambda x:x[1],reverse=True)
    
    # 将前200个2个字的词输出
    for i in order_words[0:200]:
        if(len(i[0])==2):
            print(i)
    
    for i in order_words[0:200]:
        if(len(i[0])==3):
            print(i)

    for i in order_words[0:200]:
        if(len(i[0])==4):
            print(i)

    # 将所有分词的结果输出到文件
    fs=open('pushu_word.txt','w')
    for i in order_words:
        fs.writelines(str(i)) 
    fs.close
