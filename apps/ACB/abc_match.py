import requests
from apps.ACB.tools import tree_parse, change_bjtime, get_venue_id, get_team_id, safe_get
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballMatch
from common.libs.log import LogMgr
import time
import traceback
from apps.send_error_msg import dingding_alter

logger = LogMgr.get('acb_match')


class GetMatchInfo(object):
    def __init__(self):
        self.sort_match_id = ['18638', '18639', '18640', '18641', '18642', '18643', '18644', '18645', '18646', '18647',
                              '18648', '18649', '18650', '18651', '18652', '18653', '18654', '18655', '18656', '18657',
                              '18658', '18659', '18660', '18661', '18662', '18663', '18664', '18665', '18666', '18667',
                              '18668', '18669', '18670', '18671', '18672', '18673', '18674', '18675', '18676', '18677',
                              '18678', '18679', '18680', '18681', '18682', '18683', '18684', '18685', '18686', '18687',
                              '18688', '18689', '18690', '18691', '18692', '18693', '18694', '18695', '18696', '18697',
                              '18698', '18699', '18700', '18701', '18702', '18703', '18704', '18705', '18706', '18707',
                              '18708', '18709', '18710', '18711', '18712', '18713', '18714', '18715', '18716', '18717',
                              '18718', '18719', '18720', '18721', '18722', '18723', '18724', '18725', '18726', '18727',
                              '18728', '18729', '18730', '18731', '18732', '18733', '18734', '18735', '18736', '18737',
                              '18738', '18739', '18740', '18741', '18742', '18743', '18744', '18745', '18746', '18747',
                              '18748', '18749', '18750', '18751', '18752', '18753', '18754', '18755', '18756', '18757',
                              '18758', '18759', '18760', '18761', '18762', '18763', '18764', '18765', '18766', '18767',
                              '18768', '18769', '18770', '18771', '18772', '18773', '18774', '18775', '18776', '18777',
                              '18778', '18779', '18780', '18781', '18782', '18783', '18784', '18785', '18786', '18787',
                              '18788', '18789', '18790', '18791', '18792', '18793', '18794', '18795', '18796', '18797',
                              '18798', '18799', '18800', '18801', '18802', '18803', '18804', '18805', '18806', '18807',
                              '18808', '18809', '18810', '18811', '18812', '18813', '18814', '18815', '18816', '18817',
                              '18818', '18819', '18820', '18821', '18822', '18823', '18824', '18825', '18826', '18827',
                              '18828', '18829', '18830', '18831', '18832', '18833', '18834', '18835', '18836', '18837',
                              '18838', '18839', '18840', '18841', '18842', '18843', '18844', '18845', '18846', '18847',
                              '18848', '18849', '18850', '18851', '18852', '18853', '18854', '18855', '18856', '18857',
                              '18858', '18859', '18860', '18861', '18862', '18863', '18864', '18865', '18866', '18867',
                              '18868', '18869', '18870', '18871', '18872', '18873', '18874', '18875', '18876', '18877',
                              '18878', '18879', '18880', '18881', '18882', '18883', '18884', '18885', '18886', '18887',
                              '18888', '18889', '18890', '18891', '18892', '18893', '18894', '18895', '18896', '18897',
                              '18898', '18899', '18900', '18901', '18902', '18903', '18904', '18905', '18906', '18907',
                              '18908', '18909', '18910', '18911', '18912', '18913', '18914', '18915', '18916', '18917',
                              '18918', '18919', '18920', '18921', '18922', '18923', '18924', '18925', '18926', '18927',
                              '18928', '18929', '18930', '18931', '18932', '18933', '18934', '18935', '18936', '18937',
                              '18938', '18939', '18940', '18941', '18942', '18943']
        self.sort_match_id_dict = {'18638': '/partido/estadisticas/id/18638', '18639': '/partido/estadisticas/id/18639',
                                   '18640': '/partido/estadisticas/id/18640', '18641': '/partido/estadisticas/id/18641',
                                   '18642': '/partido/estadisticas/id/18642', '18643': '/partido/estadisticas/id/18643',
                                   '18644': '/partido/estadisticas/id/18644', '18645': '/partido/estadisticas/id/18645',
                                   '18646': '/partido/estadisticas/id/18646', '18647': '/partido/estadisticas/id/18647',
                                   '18648': '/partido/estadisticas/id/18648', '18649': '/partido/estadisticas/id/18649',
                                   '18650': '/partido/estadisticas/id/18650', '18651': '/partido/estadisticas/id/18651',
                                   '18652': '/partido/estadisticas/id/18652', '18653': '/partido/estadisticas/id/18653',
                                   '18654': '/partido/estadisticas/id/18654', '18655': '/partido/estadisticas/id/18655',
                                   '18656': '/partido/estadisticas/id/18656', '18657': '/partido/estadisticas/id/18657',
                                   '18658': '/partido/estadisticas/id/18658', '18659': '/partido/estadisticas/id/18659',
                                   '18660': '/partido/estadisticas/id/18660', '18661': '/partido/estadisticas/id/18661',
                                   '18662': '/partido/estadisticas/id/18662', '18663': '/partido/estadisticas/id/18663',
                                   '18664': '/partido/estadisticas/id/18664', '18665': '/partido/estadisticas/id/18665',
                                   '18666': '/partido/estadisticas/id/18666', '18667': '/partido/estadisticas/id/18667',
                                   '18668': '/partido/estadisticas/id/18668', '18669': '/partido/estadisticas/id/18669',
                                   '18670': '/partido/estadisticas/id/18670', '18671': '/partido/estadisticas/id/18671',
                                   '18672': '/partido/estadisticas/id/18672', '18673': '/partido/estadisticas/id/18673',
                                   '18674': '/partido/estadisticas/id/18674', '18675': '/partido/estadisticas/id/18675',
                                   '18676': '/partido/estadisticas/id/18676', '18677': '/partido/estadisticas/id/18677',
                                   '18678': '/partido/estadisticas/id/18678', '18679': '/partido/estadisticas/id/18679',
                                   '18680': '/partido/estadisticas/id/18680', '18681': '/partido/estadisticas/id/18681',
                                   '18682': '/partido/estadisticas/id/18682', '18683': '/partido/estadisticas/id/18683',
                                   '18684': '/partido/estadisticas/id/18684', '18685': '/partido/estadisticas/id/18685',
                                   '18686': '/partido/estadisticas/id/18686', '18687': '/partido/estadisticas/id/18687',
                                   '18688': '/partido/estadisticas/id/18688', '18689': '/partido/estadisticas/id/18689',
                                   '18690': '/partido/estadisticas/id/18690', '18691': '/partido/estadisticas/id/18691',
                                   '18692': '/partido/estadisticas/id/18692', '18693': '/partido/estadisticas/id/18693',
                                   '18694': '/partido/estadisticas/id/18694', '18695': '/partido/estadisticas/id/18695',
                                   '18696': '/partido/estadisticas/id/18696', '18697': '/partido/estadisticas/id/18697',
                                   '18698': '/partido/estadisticas/id/18698', '18699': '/partido/estadisticas/id/18699',
                                   '18700': '/partido/estadisticas/id/18700', '18701': '/partido/estadisticas/id/18701',
                                   '18702': '/partido/estadisticas/id/18702', '18703': '/partido/estadisticas/id/18703',
                                   '18704': '/partido/estadisticas/id/18704', '18705': '/partido/estadisticas/id/18705',
                                   '18706': '/partido/estadisticas/id/18706', '18707': '/partido/estadisticas/id/18707',
                                   '18708': '/partido/estadisticas/id/18708', '18709': '/partido/estadisticas/id/18709',
                                   '18710': '/partido/estadisticas/id/18710', '18711': '/partido/estadisticas/id/18711',
                                   '18712': '/partido/estadisticas/id/18712', '18713': '/partido/estadisticas/id/18713',
                                   '18714': '/partido/estadisticas/id/18714', '18715': '/partido/estadisticas/id/18715',
                                   '18716': '/partido/estadisticas/id/18716', '18717': '/partido/estadisticas/id/18717',
                                   '18718': '/partido/estadisticas/id/18718', '18719': '/partido/estadisticas/id/18719',
                                   '18720': '/partido/estadisticas/id/18720', '18721': '/partido/estadisticas/id/18721',
                                   '18722': '/partido/estadisticas/id/18722', '18723': '/partido/estadisticas/id/18723',
                                   '18724': '/partido/estadisticas/id/18724', '18725': '/partido/estadisticas/id/18725',
                                   '18726': '/partido/estadisticas/id/18726', '18727': '/partido/estadisticas/id/18727',
                                   '18728': '/partido/estadisticas/id/18728', '18729': '/partido/estadisticas/id/18729',
                                   '18730': '/partido/estadisticas/id/18730', '18731': '/partido/estadisticas/id/18731',
                                   '18732': '/partido/estadisticas/id/18732', '18733': '/partido/estadisticas/id/18733',
                                   '18734': '/partido/estadisticas/id/18734', '18735': '/partido/estadisticas/id/18735',
                                   '18736': '/partido/estadisticas/id/18736', '18737': '/partido/estadisticas/id/18737',
                                   '18738': '/partido/estadisticas/id/18738', '18739': '/partido/estadisticas/id/18739',
                                   '18740': '/partido/estadisticas/id/18740', '18741': '/partido/estadisticas/id/18741',
                                   '18742': '/partido/estadisticas/id/18742', '18743': '/partido/estadisticas/id/18743',
                                   '18744': '/partido/estadisticas/id/18744', '18745': '/partido/estadisticas/id/18745',
                                   '18746': '/partido/estadisticas/id/18746', '18747': '/partido/estadisticas/id/18747',
                                   '18748': '/partido/estadisticas/id/18748', '18749': '/partido/estadisticas/id/18749',
                                   '18750': '/partido/estadisticas/id/18750', '18751': '/partido/estadisticas/id/18751',
                                   '18752': '/partido/estadisticas/id/18752', '18753': '/partido/estadisticas/id/18753',
                                   '18754': '/partido/estadisticas/id/18754', '18755': '/partido/estadisticas/id/18755',
                                   '18756': '/partido/estadisticas/id/18756', '18757': '/partido/estadisticas/id/18757',
                                   '18758': '/partido/estadisticas/id/18758', '18759': '/partido/estadisticas/id/18759',
                                   '18760': '/partido/estadisticas/id/18760', '18761': '/partido/estadisticas/id/18761',
                                   '18762': '/partido/estadisticas/id/18762', '18763': '/partido/estadisticas/id/18763',
                                   '18764': '/partido/previa/id/18764', '18765': '/partido/previa/id/18765',
                                   '18766': '/partido/previa/id/18766', '18767': '/partido/previa/id/18767',
                                   '18768': '/partido/previa/id/18768', '18769': '/partido/previa/id/18769',
                                   '18770': '/partido/previa/id/18770', '18771': '/partido/previa/id/18771',
                                   '18772': '/partido/previa/id/18772', '18773': '/partido/previa/id/18773',
                                   '18774': '/partido/previa/id/18774', '18775': '/partido/previa/id/18775',
                                   '18776': '/partido/previa/id/18776', '18777': '/partido/previa/id/18777',
                                   '18778': '/partido/previa/id/18778', '18779': '/partido/previa/id/18779',
                                   '18780': '/partido/previa/id/18780', '18781': '/partido/previa/id/18781',
                                   '18782': '/partido/previa/id/18782', '18783': '/partido/previa/id/18783',
                                   '18784': '/partido/previa/id/18784', '18785': '/partido/previa/id/18785',
                                   '18786': '/partido/previa/id/18786', '18787': '/partido/previa/id/18787',
                                   '18788': '/partido/previa/id/18788', '18789': '/partido/previa/id/18789',
                                   '18790': '/partido/previa/id/18790', '18791': '/partido/previa/id/18791',
                                   '18792': '/partido/previa/id/18792', '18793': '/partido/previa/id/18793',
                                   '18794': '/partido/previa/id/18794', '18795': '/partido/previa/id/18795',
                                   '18796': '/partido/previa/id/18796', '18797': '/partido/previa/id/18797',
                                   '18798': '/partido/previa/id/18798', '18799': '/partido/previa/id/18799',
                                   '18800': '/partido/previa/id/18800', '18801': '/partido/previa/id/18801',
                                   '18802': '/partido/previa/id/18802', '18803': '/partido/previa/id/18803',
                                   '18804': '/partido/previa/id/18804', '18805': '/partido/previa/id/18805',
                                   '18806': '/partido/previa/id/18806', '18807': '/partido/previa/id/18807',
                                   '18808': '/partido/previa/id/18808', '18809': '/partido/previa/id/18809',
                                   '18810': '/partido/previa/id/18810', '18811': '/partido/previa/id/18811',
                                   '18812': '/partido/previa/id/18812', '18813': '/partido/previa/id/18813',
                                   '18814': '/partido/previa/id/18814', '18815': '/partido/previa/id/18815',
                                   '18816': '/partido/previa/id/18816', '18817': '/partido/previa/id/18817',
                                   '18818': '/partido/previa/id/18818', '18819': '/partido/previa/id/18819',
                                   '18820': '/partido/previa/id/18820', '18821': '/partido/previa/id/18821',
                                   '18822': '/partido/previa/id/18822', '18823': '/partido/previa/id/18823',
                                   '18824': '/partido/previa/id/18824', '18825': '/partido/previa/id/18825',
                                   '18826': '/partido/previa/id/18826', '18827': '/partido/previa/id/18827',
                                   '18828': '/partido/previa/id/18828', '18829': '/partido/previa/id/18829',
                                   '18830': '/partido/previa/id/18830', '18831': '/partido/previa/id/18831',
                                   '18832': '/partido/previa/id/18832', '18833': '/partido/previa/id/18833',
                                   '18834': '/partido/previa/id/18834', '18835': '/partido/previa/id/18835',
                                   '18836': '/partido/previa/id/18836', '18837': '/partido/previa/id/18837',
                                   '18838': '/partido/previa/id/18838', '18839': '/partido/previa/id/18839',
                                   '18840': '/partido/previa/id/18840', '18841': '/partido/previa/id/18841',
                                   '18842': '/partido/previa/id/18842', '18843': '/partido/previa/id/18843',
                                   '18844': '/partido/previa/id/18844', '18845': '/partido/previa/id/18845',
                                   '18846': '/partido/previa/id/18846', '18847': '/partido/previa/id/18847',
                                   '18848': '/partido/previa/id/18848', '18849': '/partido/previa/id/18849',
                                   '18850': '/partido/previa/id/18850', '18851': '/partido/previa/id/18851',
                                   '18852': '/partido/previa/id/18852', '18853': '/partido/previa/id/18853',
                                   '18854': '/partido/previa/id/18854', '18855': '/partido/previa/id/18855',
                                   '18856': '/partido/previa/id/18856', '18857': '/partido/previa/id/18857',
                                   '18858': '/partido/previa/id/18858', '18859': '/partido/previa/id/18859',
                                   '18860': '/partido/previa/id/18860', '18861': '/partido/previa/id/18861',
                                   '18862': '/partido/previa/id/18862', '18863': '/partido/previa/id/18863',
                                   '18864': '/partido/previa/id/18864', '18865': '/partido/previa/id/18865',
                                   '18866': '/partido/previa/id/18866', '18867': '/partido/previa/id/18867',
                                   '18868': '/partido/previa/id/18868', '18869': '/partido/previa/id/18869',
                                   '18870': '/partido/previa/id/18870', '18871': '/partido/previa/id/18871',
                                   '18872': '/partido/previa/id/18872', '18873': '/partido/previa/id/18873',
                                   '18874': '/partido/previa/id/18874', '18875': '/partido/previa/id/18875',
                                   '18876': '/partido/previa/id/18876', '18877': '/partido/previa/id/18877',
                                   '18878': '/partido/previa/id/18878', '18879': '/partido/previa/id/18879',
                                   '18880': '/partido/previa/id/18880', '18881': '/partido/previa/id/18881',
                                   '18882': '/partido/previa/id/18882', '18883': '/partido/previa/id/18883',
                                   '18884': '/partido/previa/id/18884', '18885': '/partido/previa/id/18885',
                                   '18886': '/partido/previa/id/18886', '18887': '/partido/previa/id/18887',
                                   '18888': '/partido/previa/id/18888', '18889': '/partido/previa/id/18889',
                                   '18890': '/partido/previa/id/18890', '18891': '/partido/previa/id/18891',
                                   '18892': '/partido/previa/id/18892', '18893': '/partido/previa/id/18893',
                                   '18894': '/partido/previa/id/18894', '18895': '/partido/previa/id/18895',
                                   '18896': '/partido/previa/id/18896', '18897': '/partido/previa/id/18897',
                                   '18898': '/partido/previa/id/18898', '18899': '/partido/previa/id/18899',
                                   '18900': '/partido/previa/id/18900', '18901': '/partido/previa/id/18901',
                                   '18902': '/partido/previa/id/18902', '18903': '/partido/previa/id/18903',
                                   '18904': '/partido/previa/id/18904', '18905': '/partido/previa/id/18905',
                                   '18906': '/partido/previa/id/18906', '18907': '/partido/previa/id/18907',
                                   '18908': '/partido/previa/id/18908', '18909': '/partido/previa/id/18909',
                                   '18910': '/partido/previa/id/18910', '18911': '/partido/previa/id/18911',
                                   '18912': '/partido/previa/id/18912', '18913': '/partido/previa/id/18913',
                                   '18914': '/partido/previa/id/18914', '18915': '/partido/previa/id/18915',
                                   '18916': '/partido/previa/id/18916', '18917': '/partido/previa/id/18917',
                                   '18918': '/partido/previa/id/18918', '18919': '/partido/previa/id/18919',
                                   '18920': '/partido/previa/id/18920', '18921': '/partido/previa/id/18921',
                                   '18922': '/partido/previa/id/18922', '18923': '/partido/previa/id/18923',
                                   '18924': '/partido/previa/id/18924', '18925': '/partido/previa/id/18925',
                                   '18926': '/partido/previa/id/18926', '18927': '/partido/previa/id/18927',
                                   '18928': '/partido/previa/id/18928', '18929': '/partido/previa/id/18929',
                                   '18930': '/partido/previa/id/18930', '18931': '/partido/previa/id/18931',
                                   '18932': '/partido/previa/id/18932', '18933': '/partido/previa/id/18933',
                                   '18934': '/partido/previa/id/18934', '18935': '/partido/previa/id/18935',
                                   '18936': '/partido/previa/id/18936', '18937': '/partido/previa/id/18937',
                                   '18938': '/partido/previa/id/18938', '18939': '/partido/previa/id/18939',
                                   '18940': '/partido/previa/id/18940', '18941': '/partido/previa/id/18941',
                                   '18942': '/partido/previa/id/18942', '18943': '/partido/previa/id/18943'}
        self.get_venue_id = get_venue_id()
        self.get_team_id = get_team_id()
        self.session = MysqlSvr.get('spider_zl')

    def get_match_info(self):
        match_api_id_list = []
        match_api_id_team_dict = {}
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        match_url = 'http://jv.acb.com/historico.php?jornada=%s'
        for jornada in range(1, 26):
            match_res = requests.get(match_url % jornada, headers=headers)
            logger.info(match_url % jornada)
            match_tree = tree_parse(match_res)
            par_ids = match_tree.xpath('//div[@class="partidos"]/div/@id')
            home_names = match_tree.xpath(
                '//div[@class="partidos"]/div[@class="partido borde_azul"]/div[@class="fila_superior borde_azul_inferior"]/div[@class="nombre_equipo borde_azul_derecha clase_solo_ocultar_960 ellipsis mayuscula"]/text()|./div[@class="partido borde_gris"]/div[@class="fila_superior borde_gris_inferior"]/div[@class="nombre_equipo borde_gris_derecha clase_solo_ocultar_960 ellipsis mayuscula"]/text()')
            away_names = match_tree.xpath(
                '//div[@class="partidos"]/div[@class="partido borde_azul"]/div[@class="fila_superior borde_azul_inferior"]/div[@class="nombre_equipo clase_solo_ocultar_960 ellipsis mayuscula"]/text()|./div[@class="partido borde_gris"]/div[@class="fila_superior borde_gris_inferior"]/div[@class="nombre_equipo clase_solo_ocultar_960 ellipsis mayuscula"]/text()')
            for index in range(len(par_ids)):
                par_id = par_ids[index]
                id = par_id.split('-')[-1]
                if id:
                    try:
                        home_name = home_names[index]
                    except:
                        logger.info('没有信息')
                    try:
                        away_name = away_names[index]
                    except:
                        logger.info('没有信息')
                    home_team_id = self.get_team_id[home_name.lower().strip()]
                    away_team_id = self.get_team_id[away_name.lower().strip()]
                    match_api_id_team_dict[id] = (home_team_id, away_team_id)
                    match_api_id_list.append(id)
        match_api_id_list.sort()
        print(match_api_id_list)
        for index in range(len(match_api_id_list)):
            match_info_dict = {}
            url = self.sort_match_id_dict[self.sort_match_id[index]]
            res = requests.get('http://www.acb.com' + url, headers=headers)
            tree = tree_parse(res)
            time_info = tree.xpath('//div[@class="datos_evento roboto texto-centrado colorweb_4 bg_azul_medio"]')
            date = time_info[0].xpath('string(.)').split('-')[0]
            time = time_info[0].xpath('string(.)').split('-')[1]
            match_info_dict['match_time'] = change_bjtime(date.strip() + ' ' + time.strip())
            print(match_info_dict['match_time'])
            match_info_dict['id'] = match_api_id_list[index]
            match_info_dict['sport_id'] = 2
            venue_city = time_info[0].xpath('string(.)').split('-')[-1].strip()
            match_info_dict['venue_id'] = self.get_venue_id[venue_city]
            match_info_url = 'https://www.fibalivestats.com/data/%s/data.json' % match_api_id_list[index]
            match_res = requests.get(match_info_url, headers=headers)
            logger.info(match_info_url)
            if match_res.status_code == 200:
                match_info = match_res.json()
                match_info_dict['status_id'] = 10
                home_name = match_info['tm']['1']['name']
                away_name = match_info['tm']['2']['name']
                match_info_dict['home_team_id'] = self.get_team_id[home_name.lower().strip()]
                match_info_dict['away_team_id'] = self.get_team_id[away_name.lower().strip()]
                match_info_dict['home_score'] = safe_get(match_info, 'tm.1.tot_sPoints')
                match_info_dict['away_score'] = safe_get(match_info, 'tm.2.tot_sPoints')
                match_info_dict['home_half_score'] = safe_get(match_info, 'tm.1.p1_score') + safe_get(match_info,
                                                                                                      'tm.1.p2_score')
                match_info_dict['away_half_score'] = safe_get(match_info, 'tm.2.p1_score') + safe_get(match_info,
                                                                                                      'tm.2.p2_score')
                home_p1_score = safe_get(match_info, 'tm.1.p1_score')
                home_p2_score = safe_get(match_info, 'tm.1.p2_score')
                home_p3_score = safe_get(match_info, 'tm.1.p3_score')
                home_p4_score = safe_get(match_info, 'tm.1.p4_score')
                if match_info_dict['home_score'] != home_p1_score + home_p2_score + home_p3_score + home_p4_score:
                    home_p5_score = safe_get(match_info, 'tm.1.ot_score')
                    match_info_dict['home_scores'] = str([home_p1_score, home_p2_score, home_p3_score, home_p4_score,
                                                      home_p5_score,
                                                      match_info_dict['home_score']])
                else:
                    match_info_dict['home_scores'] = str([home_p1_score, home_p2_score, home_p3_score, home_p4_score,
                                                      match_info_dict['home_score']])
                away_p1_score = safe_get(match_info, 'tm.2.p1_score')
                away_p2_score = safe_get(match_info, 'tm.2.p2_score')
                away_p3_score = safe_get(match_info, 'tm.2.p3_score')
                away_p4_score = safe_get(match_info, 'tm.2.p4_score')
                if match_info_dict['away_score'] != away_p1_score + away_p2_score + away_p3_score + away_p4_score:
                    away_p5_score = safe_get(match_info, 'tm.2.ot_score')
                    match_info_dict['away_scores'] = str([away_p1_score, away_p2_score, away_p3_score, away_p4_score,
                                                      away_p5_score,
                                                      match_info_dict['away_score']])
                else:
                    match_info_dict['away_scores'] = str([away_p1_score, away_p2_score, away_p3_score, away_p4_score,
                                                      match_info_dict['away_score']])
            else:
                match_info_dict['home_team_id'] = match_api_id_team_dict[match_api_id_list[index]][0]
                match_info_dict['away_team_id'] = match_api_id_team_dict[match_api_id_list[index]][1]
                match_info_dict['home_score'] = 0
                match_info_dict['away_score'] = 0
                match_info_dict['home_scores'] = 0
                match_info_dict['away_scores'] = 0
                match_info_dict['home_half_score'] = 0
                match_info_dict['away_half_score'] = 0
                match_info_dict['status_id'] = 1
            BleagueAcbBasketballMatch.upsert(
                self.session,
                'id',
                match_info_dict
            )
            logger.info(match_info_dict)



    def run(self):
        try:
            while True:
                self.get_match_info()
                time.sleep(43200)
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())


