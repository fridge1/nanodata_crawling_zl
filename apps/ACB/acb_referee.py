import requests
from orm_connection.acb_basketball import BleagueAcbBasketballReferee
from apps.ACB.tools import tree_parse
from orm_connection.orm_session import MysqlSvr

session = MysqlSvr.get('spider_zl')
headers = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
url = 'http://www.acb.com/articulo/ver/150168'
res = requests.get(url,headers=headers)
tree = tree_parse(res)
name_list = tree.xpath('//tbody/tr')
id = 1
for name in name_list:
    name_en = name.xpath('./td/strong/text()|./td/text()')[0]
    data = {
        'id':id,
        'name_en':name_en
    }
    BleagueAcbBasketballReferee.upsert(
        session,
        'id',
        data
    )
    print(data)
    id += 1
session.close()