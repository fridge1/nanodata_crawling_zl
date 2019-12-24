import requests
from apps.ACB.tools import tree_parse, change_bjtime



def get_match_id():
    match_id_list = []
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    for jornada in range(1,48):
        url = 'http://jv.acb.com/historico.php?jornada=%s'
        res = requests.get(url % jornada,headers=headers)
        tree = tree_parse(res)
        match_jornada_list = tree.xpath('//div[@id="partidos_jv"]/div/@id')
        for match_id in match_jornada_list:
            if match_id.split('-')[-1]:
                match_id_list.append(match_id.split('-')[-1])
                print(match_id)
    return match_id_list



def get_match_info():
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    year_list = [2019]
    match_urls = 'http://www.acb.com/resultados-clasificacion/ver/temporada_id/%s/competicion_id/1/jornada_numero/1'
    for year in year_list:
        match_url_res = requests.get(match_urls % year, headers=headers)
        match_tree = tree_parse(match_url_res)
        jornada_list = match_tree.xpath('//div[@id="listado_resultados_jornada"]/div/@data-t2v-id')
        for jornada in jornada_list:
            map_url = 'http://www.acb.com/resultados-clasificacion/ver/temporada_id/%s/competicion_id/1/jornada_numero/%s'
            headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            }
            match_info_res = requests.get(map_url % (str(year), jornada), headers=headers)
            match_info_tree = tree_parse(match_info_res)
            match_info_urls = list(set(match_info_tree.xpath(
                '//div[@id="listado_partidos"]/article/section/div[@class="info roboto_condensed_bold"]/div/a/@href|//div[@id="listado_partidos"]/article/section/div[@class="info roboto_condensed_bold"]/span[@class="fecha"]/a/@href')))
            for url in match_info_urls:
                res = requests.get('http://www.acb.com' + url, headers=headers)
                id = url.split('/')[-1]
                tree = tree_parse(res)
                time_info = tree.xpath('//div[@class="datos_evento roboto texto-centrado colorweb_4 bg_azul_medio"]')
                date = time_info[0].xpath('string(.)').split('-')[0]
                time = time_info[0].xpath('string(.)').split('-')[1]
                match_time = change_bjtime(date.strip() + ' ' + time.strip())
                venue_city = time_info[0].xpath('string(.)').split('-')[-1].strip()


print(get_match_id())