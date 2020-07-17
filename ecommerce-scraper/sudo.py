import re,sys,bs4,requests,subprocess,os

amz_result={}
flip_result={}
snap_result={}
amazon = 'http://www.amazon.in/s/?url=search-alias%3Daps&field-keywords='
snapdeal = 'http://www.snapdeal.com/search?keyword='
flipkart = 'http://www.flipkart.com/search?q='

def openweb(url):
    DEVNULL = open(os.devnull,'w')
    subprocess.call(['xdg-open',url],stdout=DEVNULL,stderr=subprocess.STDOUT)

def get_src(site,args):
  #webbrowser.open(site+args)
    req = requests.get(site+args)
    if not req:
        print ('Connection Failed for '+site)
        return None
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    return soup
    
def show_amz(args):
    res = 5
    amz_title = '.a-link-normal > .a-text-normal'
    soup = get_src(amazon,args)
    if not soup:
        return None
    title = []
    ctr = 5
    for name in soup.findAll(True,{'class':['a-size-base', 'a-color-null','s-inline' , 's-access-title', 'a-text-normal']}):
        val = name.get('data-attribute') 
        if val != None:
            title.append(val)
            ctr -= 1
        if ctr == 0:
            break

    prices = []
    ctr = 0
    for pr in  soup.select('a.a-link-normal.a-text-normal > span.a-size-base.a-color-price.s-price.a-text-bold'):
        x = re.findall(r'([\d\,\.]+)',str(pr.get_text))
        print ('Amazon ->',title[ctr]+': ',x[3])
        ctr += 1
        if ctr==5:
            break
                 
def show_flip(args):
    flip_title = '.fk-display-block'
    soup = get_src(flipkart,args)
    if not soup:
        return None  
    title_link = soup.select(flip_title)
    price_link = soup.select('.pu-final')
    product=[]
    price = []
    res = 5
    for title in title_link:
        if res == 0:
            break
        prd=str(title.get('title')).strip()
        if prd != 'None':
            res -=1
            product.append(prd)
        
    res = 5
    for val in price_link:
        if res == 0:
            break 
        pr = str(val.get_text()).strip()
        if pr !='None':
            res -=1  
            price.append(pr)
    
    flip_result=dict(zip(price,product,))
    for price,prd in flip_result.items():
        print ('FlipKart'+'-> '+prd+':'+price)

def show_snap(args):
    res = 5
    snapdeal = 'http://www.snapdeal.com/search?keyword='
    snap_title = '.product-tuple-description > .product-desc-rating a > .product-title'
    soup = get_src(snapdeal,args)
    if not soup:
        return None  
    title_link = soup.select(snap_title)
    price_link = soup.select('.product-price') 
    price = []
    product=[]
    for title,val in zip(title_link,price_link):
        if res == 0:
            break
        res -=1
        product.append(str(title.get_text())[:-1])
        price.append(str(val.get_text()))
        
    snap_result = dict(zip(price,product))
    for price,prd in snap_result.items():
        print ('SnapDeal'+'-> '+prd+':'+price)
        
def main(args):
    print ('Pulling Request from Web.......\n')
    show_flip(args)
    print ('                        ----------------------------------------------------------------------------------------------------------------------------')
    show_snap(args) 
    
    print ('                        ----------------------------------------------------------------------------------------------------------------------------')
    show_amz(args)

    print ('                        ----------------------------------------------------------------------------------------------------------------------------')
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print ("Usage:- [search query] => will give results of search query from amazon,flipkart,snapdeal, no args it will give result from main page  of these shopping site")
    args = ' '.join(args)
    main(args)
    query=input('>> q(quit), open web page with : az(amazon),fk(flipkart),sd(snapdeal) :')
    if query == 'az':
        openweb(amazon+args)
    elif query == 'fk':
        openweb(flipkart+args)
    elif query == 'sd':
        openweb(snapdeal+args)
else:
        sys.exit(1)    
