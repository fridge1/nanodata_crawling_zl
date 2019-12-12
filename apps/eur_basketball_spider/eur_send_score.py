from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_match_live')





data = {
    'sport_id': 2,
    'site': 'bt',
    'matches': {
        match_id: {
            'score': {
                'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': match_time},
                'status_id': status_id,
                'home_scores': home_scores,
                'away_scores': away_scores,
            }
        }
    }
}



