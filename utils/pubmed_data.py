from threading import Lock
from xml.dom import minidom
import os.path
import sys
import threading
import urllib2


ARTICLE_PATH="article"
ABSTRACT_PATH="abstract"
PROVIDER_PRIORITY=["PMC","Hindawi"]
lock=Lock()
ids=[]
i=0
abstract_url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=text&id="
link_url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?db=pubmed&cmd=llinks&id="

class ArticleCollectorThread ( threading.Thread ):

    def run ( self ):
        while(True):
            articleId,index=get_article_id()
            if articleId==None:
                break;
            sys.stdout.write("("+str(index)+"/"+str(len(ids2))+") "+articleId+".")
            if (not is_abstract_exist(articleId)):
                doc=get_url_as_xmldoc(abstract_url+articleId)
                sys.stdout.write(".")
                abstractList = doc.getElementsByTagName("AbstractText")
                if (len(abstractList)>0):
                    abstract=abstractList[0].childNodes[0].data.encode('ascii', 'ignore');
                    sys.stdout.write(".")
                    save_abstract(articleId, abstract)
            doc=get_url_as_xmldoc(link_url+articleId)
            sys.stdout.write(".")
            objUrls=doc.getElementsByTagName("ObjUrl")
            providers={}
            for objUrl in objUrls:
                provider=objUrl.getElementsByTagName("NameAbbr")[0].childNodes[0].data.encode('ascii', 'ignore');
                url=objUrl.getElementsByTagName("Url")[0].childNodes[0].data.encode('ascii', 'ignore');
                providers[provider]=url
                sys.stdout.write(".")
            url_list=[providers[provider] for provider in PROVIDER_PRIORITY if provider in providers.keys()]
            all_urls=url_list+providers.values()
            i=0
            for url in all_urls:
                try:
                    if (not is_article_exist(articleId,i)):
                        data=get_data_from_url(url)
                        sys.stdout.write(".")
                        save_article(articleId, i,data)
                    i+=1
                except Exception:
                    pass
                
            print "done."

    

def get_data_from_url(url):
    website = urllib2.urlopen(url)
    return website.read()     


def get_url_as_xmldoc(url):
    data = get_data_from_url(url)
    xmldoc = minidom.parseString(data)
    return xmldoc

def get_article_ids(search_term):
    
    term=search_term.replace(" ","+")
    
    url="http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+term+"+AND+free+full+text[filter]"

    xmldoc = get_url_as_xmldoc(url)
    count=xmldoc.getElementsByTagName('Count')[0].childNodes[0].data.encode('ascii', 'ignore')
    
    url=url+"&RetMax="+count
    xmldoc = get_url_as_xmldoc(url)
    
    ids = xmldoc.getElementsByTagName('Id')
    
    id_list=[articleId.childNodes[0].data.encode('ascii', 'ignore') for articleId in ids]
    
    return id_list

def write_to_file(filename,data):
    f = open(filename, 'w');
    f.write(data);
    f.close();

def create_valid_filename(articleId, ARTICLE_PATH, index=-1):
    if (index==-1):
        article_path=ARTICLE_PATH
    else:
        article_path=ARTICLE_PATH + "/" + articleId
        
    if (not os.path.exists(article_path)):
        os.makedirs(article_path)
    if (index==-1):
        filename = article_path+"/" + articleId+".html"
    else:
        filename = article_path+"/" + articleId+"."+str(index)+".html"
    return filename

def save_article(articleId, index, data):
    filename = create_valid_filename(articleId, ARTICLE_PATH, index)
    write_to_file(filename, data)
    return filename;

def save_abstract(articleId, abstract_data):
    filename = create_valid_filename(articleId, ABSTRACT_PATH)
    write_to_file(filename, abstract_data)
    return filename;

def is_abstract_exist(articleId):
    return os.path.exists(create_valid_filename(articleId, ABSTRACT_PATH))

def is_article_exist(articleId,index):
    return os.path.exists(create_valid_filename(articleId, ARTICLE_PATH,index))

def get_article_id():
    articleId=None
    index=-1
    lock.acquire()
    if (len(ids)>0):
        articleId=ids[0]
        del ids[0]
        index=len(ids2)-len(ids)
    lock.release()
    return articleId,index

ids=get_article_ids("heart")
ids2=list(ids)
no_of_threads=50
for index in range(no_of_threads):
    ArticleCollectorThread().start()
    
