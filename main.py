from __patch__ import patch_all
from actions.eur_basketball import eur_basketball_actions
from actions.nbl_basketball import nbl_basketball_actions
from actions.kbl_basketball import kbl_basketball_actions
from actions.acb_basketball import acb_basketball_actions
from actions.wta_tennis import wta_tennis_actions
from apps.app import AppCtx

patch_all()
from common.libs.log import LogMgr
from common.utils import parse_options


logger = LogMgr.get()

group_actions = {
    'eur_basketball_actions': eur_basketball_actions,
    'nbl_basketball_actions' : nbl_basketball_actions,
    'kbl_basketball_actions' : kbl_basketball_actions,
    'acb_basketball_actions' : acb_basketball_actions,
    'wta_tennis_actions' : wta_tennis_actions,
}

if __name__ == '__main__':
    actions = dict()
    for k, v in group_actions.items():
        actions.update(v)
    options = parse_options()
    action = options.get('action') or options.get('a')
    env = options.get('env') or options.get('e')
    echo = options.get('echo') and True

    if action:
        AppCtx.set_env(env)
        AppCtx.set_echo(echo)
        if action in actions:
            logger.info('当前环境:%s 动作:%s' % (AppCtx.get_env(), action))
            actions[action](options)
