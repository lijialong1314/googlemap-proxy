# -*- coding: utf-8 -*-
import hashlib
import requests
from urlextract import URLExtract

sourceurl = "https://maps.google.cn/maps/api/js"
maindomain = "api.googlemaps.world"
mainapidomain = "mapsapis.googlemaps.world"

def getmd5(txt):
    hl = hashlib.md5()
    hl.update(txt.encode(encoding='utf-8'))
    return hl.hexdigest()

def getAllLink(txt):
    extractor = URLExtract()
    urls = extractor.find_urls(txt)
    return urls

def save(filename,content):
    with open(filename,"w") as w:
        for row in content:
            w.write(row+"\n")
            
def main():
    source = requests.get(sourceurl)
    alllink = getAllLink(source.text)
    linkdata = []
    
    for link in alllink:
        if "https" in link and link not in linkdata and "www.google.cn" not in link and "maps.google.cn" not in link:
            linkdata.append(link)

    replacefilter = []
    location =[]
    alldomain = []
    for row in linkdata:
        if(len(row)>0):
            domain = row.replace("https://","").split("/")[0]
            if domain in alldomain:
                    continue
            alldomain.append(domain)
            
            if "maps.googleapis.com" in row:
                replacefilter.append("replace_filter %s %s ig;"%(domain,mainapidomain))
            elif "www.google.com" in row:
                replacefilter.append("replace_filter %s %s ig;"%(domain,"www.google.cn"))
            else:
                md5val = getmd5(domain.replace(".",""))
                replacefilter.append("replace_filter %s %s ig;"%(domain,maindomain+"/"+md5val))
                location.append("location /%s/ { proxy_pass %s; }"%(md5val,"https://"+domain+"/"));                
    
    #save nginx config
    save("replace.conf",replacefilter)
    save("location.conf",location)
    
if __name__ == "__main__":
    main()