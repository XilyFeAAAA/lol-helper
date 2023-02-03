
from enum import Enum

class LobbyVaria(str, Enum):
    Update = 'Update'
    Create = 'Create'
    Delete = 'Delete'

class Gamemode(int, Enum):
    PRACTICE_GAME = -1
    RANKED_SOLO_5x5 = 420
    RANKED_FLIX_SR = 440
    NORMAL = 430
    ARAM = 450
    URF = 1090
    TFT = 900


class StateEvent(str, Enum):
    Lobby = 'Lobby'
    none = 'None'
    Matchmaking = 'Matchmaking'
    Champselect = 'ChampSelect'
    ReadyCheck = 'ReadyCheck'
    Reconnect = 'Reconnect:'
    GameStart = 'GameStart'
    TerminatedInError = 'TerminatedInError'
    InProgress = 'InProgress'
    PreEndOfGame = 'PreEndOfGame'
    EndOfGame = 'EndOfGame'
    WaitingForStats = 'WaitingForStats'

class LootType(str, Enum):
    champion_rental = 'CHAMPION_RENTAL'
    skin_rental = 'SKIN_RENTAL'
    stone = 'STATSTONE'
    emote = 'EMOTE'
    token = 'CHAMPION_TOKEN'  # 成就代币
    chest = 'CHEST'  # 宝箱
    currency = 'CURRENCY'  # 神话精萃

class Redeem(str, Enum):
    isOwned = 'ALREADY_OWNED'
    notOwned = 'REDEEMABLE_RENTAL'


ClientStatus = {
    "在线": "chat",
    "离开": "away",
    "游戏中": "dnd",
    "离线": "offline",
    "手机在线": "mobile"
}

Environment = {
    'HN1': '艾欧尼亚',
    'HN2': '祖安',
    'HN3': '诺克萨斯',
    'HN4': '班德尔城',
    'HN5': '皮尔特沃夫',
    'HN6': '战争学院',
    'HN7': '巨神峰 ',
    'HN8': '雷瑟守备',
    'HN9': '裁决之地',
    'HN10': '黑色玫瑰',
    'HN11': '暗影岛',
    'HN12': '钢铁烈阳 ',
    'HN13': '水晶之痕',
    'HN14': '均衡教派',
    'HN15': '影流',
    'HN16': '守望之海',
    'HN17': '征服之海',
    'HN18': '卡拉曼达',
    'HN19': '皮城警备',
    'WT1': '比尔吉沃特',
    'WT2': '德玛西亚',
    'WT3': '弗雷尔卓德',
    'WT4': '无畏先锋',
    'WT5': '恕瑞玛',
    'WT6': '扭曲丛林',
    'WT7': '巨龙之巢',
    'HN1_NEW': '艾欧尼亚',
    'HN2_NEW': '祖安',
    'HN3_NEW': '诺克萨斯',
    'HN4_NEW': '班德尔城',
    'HN5_NEW': '皮尔特沃夫',
    'HN6_NEW': '战争学院',
    'HN7_NEW': '巨神峰 ',
    'HN8_NEW': '雷瑟守备',
    'HN9_NEW': '裁决之地',
    'HN10_NEW': '黑色玫瑰',
    'HN11_NEW': '暗影岛',
    'HN12_NEW': '钢铁烈阳 ',
    'HN13_NEW': '水晶之痕',
    'HN14_NEW': '均衡教派',
    'HN15_NEW': '影流',
    'HN16_NEW': '守望之海',
    'HN17_NEW': '征服之海',
    'HN18_NEW': '卡拉曼达',
    'HN19_NEW': '皮城警备',
    'WT1_NEW': '比尔吉沃特',
    'WT2_NEW': '德玛西亚',
    'WT3_NEW': '弗雷尔卓德',
    'WT4_NEW': '无畏先锋',
    'WT5_NEW': '恕瑞玛',
    'WT6_NEW': '扭曲丛林',
    'WT7_NEW': '巨龙之巢',
    'BGP1': '男爵领域'
  }

RankLevel = {
    '4': 'IV',
    '3': 'III',
    '2': 'II',
    '1': 'I'
}

Position = {
    "补位": 'FILL',
    "上单": 'TOP',
    "打野": 'JUNGLE',
    "中单": 'MIDDLE',
    "射手": 'BOTTOM',
    "辅助": 'UTILITY'
}

Rank = {
    '坚韧黑铁': 'IRON',
    '英勇黄铜': 'BRONZE',
    '不屈白银': 'SILVER',
    '荣耀黄金': 'GOLD',
    '华贵铂金': 'PLATINUM',
    '璀璨钻石': 'DIAMOND',
    '超凡大师': 'MASTER',
    '傲世宗师': 'GRANDMASTER',
    '最强王者': 'CHALLENGER',
    '没有段位': 'UNRANKKED'
}

Rankmode = {
    '单排 / 双排': 'RANKED_SOLO_5x5',
    '灵活组排5v5': 'RANKED_FLEX_SR',
    '云顶之弈': 'RANKED_TFT'
}


class ROUTE(str, Enum):
    state = '/riot-messaging-service/v1/state'
    GameFlow = '/lol-gameflow/v1/gameflow-phase'
    ChampionBench = '/lol-lobby-team-builder/champ-select/v1/session'
    # 选人信息
    BpSession = '/lol-champ-select/v1/session'
    add_friend = '/lol-chat/v1/friend-requests'  # POST
    accept_game = '/lol-matchmaking/v1/ready-check/accept'  # post
    decline_game = '/lol-matchmaking/v1/ready-check/decline'
    reconnect_game = '/lol-gameflow/v1/reconnec'
    play_again = '/lol-lobby/v2/play-again'
    blue_essence = '/lol-inventory/v1/wallet/lol_blue_essence'
    bp_champion = '/lol-champ-select/v1/session/actions/{}'  # patch
    swap_champion = '/lol-champ-select/v1/session/bench/swap/{}'
    cancel_add_friend = '/lol-chat/v1/friend-requests/{}'  # Delete
    # 个人信息
    me = '/lol-chat/v1/me'
    environment = '/riotclient/v1/crash-reporting/environment'
    # 英雄信息
    champions = '/lol-game-data/assets/v1/champions/{id}.json'
    all_champions = '/lol-champions/v1/owned-champions-minimal'
    current_champion = '/lol-champ-select/v1/current-champion'
    # 房间信息
    session = '/lol-gameflow/v1/session'
    friend_list = '/lol-game-client-chat/v1/buddies'
    chat_info = '/lol-chat/v1/conversations/{}/messages'
    # 当前所有好友对话 id= conversation-id以及最后回复内容
    conversations = '/lol-chat/v1/conversations'
    chat_frient = "/lol-game-client-chat/v1/instant-messages?summonerName={}&message={}"
    # 指定聊天的所有内容    post= {body= message type= chat}
    conversation_msg = '/lol-chat/v1/conversations/{}/messages'
    current_environment = '/riotclient/v1/crash-reporting/environment'
    current_summoner = '/lol-summoner/v1/current-summoner'
    game_flow = '/lol-gameflow/v1/gameflow-phase'
    match_detail = '/lol-match-history/v1/games/{}'
    match_list_by_id = '/lol-match-history/v3/matchlist/account/{}?begIndex={}&endIndex={}'
    match_list_by_puuid = '/lol-match-history/v1/products/lol/{}/matches?begIndex={}&endIndex={}'
    summoner = '/lol-summoner/v1/summoners/{}'
    summoner_by_name = '/lol-summoner/v1/summoners?name={}'
    summoner_by_puuid = '/lol-summoner/v2/summoners/puuid/{}'
    rank = '/lol-ranked/v1/ranked-stats/{}'
    profile_icon = '/lol-game-data/assets/v1/profile-icons/{}.jpg'
    summoner_profile = '/lol-summoner/v1/current-summoner/summoner-profile'
    ranked_stats = '/lol-ranked/v1/ranked-stats/{summonerId}'
    # ids = ''.join(summonerIds)
    summoners = '/lol-summoner/v2/summoners?ids={ids}'
    lobby = '/lol-lobby/v2/lobby'
    gamemode = '/lol-lobby/v1/parties/gamemode'
    lobby_bot = '/lol-lobby/v1/lobby/custom/bots'
    promote = '/lol-lobby/v2/lobby/members/{}/promote'
    search = '/lol-lobby/v2/lobby/matchmaking/search'
    invite = '/lol-lobby/v2/lobby/invitations'
    revoke_invite = '/lol-lobby/v2/lobby/members/{}/revoke-invite'
    kick = '/lol-lobby/v2/lobby/members/{}/kick'
    switch = '/lol-lobby/v1/lobby/custom/switch-teams'
    # 对局信息
    allgamedata = '/liveclientdata/allgamedata'
    position = '/lol-lobby/v2/lobby/members/localMember/position-preferences'
    notification = '/lol-champ-select/v1/pin-drop-notification'
    # 英雄
    pickable = '/lol-champ-select/v1/pickable-champion-ids'
    bannable = '/lol-champ-select/v1/bannable-champion-ids'
    reroll = '/lol-champ-select/v1/session/my-selection/reroll'
    champion_skin = '/lol-game-data/assets/v1/champions/{}.json'
    # 战利品
    collection = '/lol-collections/v1/inventories/{}/champion-mastery/top?limit={}'
    loot = '/lol-loot/v1/player-loot'
    loot_map = '/lol-loot/v1/player-loot-map'
    champion_rental = '/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={}'
    skin_rental = '/lol-loot/v1/recipes/SKIN_RENTAL_disenchant/craft?repeat={}'
    # 符文
    page = '/lol-perks/v1/pages'
    current_rune = '/lol-perks/v1/currentpage'
