from orm_connection.eur_basketball import BleagueBasketballGameText
from orm_connection.orm_session import MysqlSvr
MysqlSvr.set_env('development')



def test_upsert():
     # 插入数据
    data = {
        'id'     : 123,
        'key'    : '123',
        # 'name_en': 'test',
        # 'name_zh': 'test_zh'
    }
    spx_dev_session = MysqlSvr.get('spider_zl')
    BleagueBasketballGameText.upsert(
        spx_dev_session,
        'id',
        data
    )
    spx_dev_session.close()




#
# def test_upsert():
#     pass
    # for num in range(50, 60):
    #     data = {
    #         'sport_id': 2,
    #         'key': 'test_zh%d' % num,
    #         'city': 'test_zh%d' % num
    #     }
    #     print(data)
    #     spx_dev_session = MysqlSvr.get('local')
    #     _, row = BleaguejpBasketballVenue.upsert(
    #         spx_dev_session,
    #         'key',
    #         data
    #     )
    #     print(row.id)
    # data = {
    #     'sport_id': 2,
    #     # 'key': 'test_zh52',
    #     'city': 'test_zhwww'
    # }
    #
    # print(data)
    # spx_dev_session = MysqlSvr.get('local')
    # _, row = BleaguejpBasketballVenue.set_attr(
    #     spx_dev_session,
    #     155,
    #     data
    # )
    # print(row.id)
    #查询表内数据总量
    # dd = BleaguejpBasketballPlayer.count_all(
    #     spx_dev_session,
    #     # 'id',
    #     # data
    # )
    # pp = BleaguejpBasketballTeam.get_all(spx_dev_session,'name_en')
    # print(dd)
    # print(pp)
    # spx_dev_session.close()

if __name__ == '__main__':
    test_upsert()

