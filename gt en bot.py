import discord
from discord import app_commands
from discord.ui import Select, View
import schedule
import random
import asyncio
import json
from datetime import datetime
import pytz
import os
import asyncpg

# 设置 Bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# 单词表（此处省略，实际使用时需保留完整的 word_list）
word_list = [
    {"word": "bide", "pronunciation": "[əˈbaɪd]", "part_of_speech": "vt.vi", "meaning": "遵守"},
    {"word": "abolish", "pronunciation": "[əˈbɑlɪʃ]", "part_of_speech": "vt", "meaning": "廢止"},
    {"word": "abortion", "pronunciation": "[əˈbɔrʃən]", "part_of_speech": "n", "meaning": "墮胎"},
    {"word": "abrupt", "pronunciation": "[əˈbrʌpt]", "part_of_speech": "adj", "meaning": "突然的"},
    {"word": "absurd", "pronunciation": "[əbˈsɝd]", "part_of_speech": "adj", "meaning": "荒謬的"},
    {"word": "abundant", "pronunciation": "[əˈbʌndənt]", "part_of_speech": "adj", "meaning": "豐富的"},
    {"word": "academy", "pronunciation": "[əˈkædəmɪ]", "part_of_speech": "n", "meaning": "學院"},
    {"word": "accustom", "pronunciation": "[əˈkʌstəm]", "part_of_speech": "vt", "meaning": "使…習慣"},
    {"word": "ace", "pronunciation": "[es]", "part_of_speech": "n", "meaning": "么點；王牌"},
    {"word": "acknowledge", "pronunciation": "[əkˈnɑlɪdʒ]", "part_of_speech": "vt", "meaning": "承認"},
    {"word": "acknowledgement", "pronunciation": "[əkˈnɑlɪdʒmənt]", "part_of_speech": "n", "meaning": "承認"},
    {"word": "acne", "pronunciation": "[ˈæknɪ]", "part_of_speech": "n", "meaning": "粉刺"},
    {"word": "admiral", "pronunciation": "[ˈædmərəl]", "part_of_speech": "n", "meaning": "海軍上將"},
    {"word": "adolescence", "pronunciation": "[ˌædəˈlɛsns]", "part_of_speech": "n", "meaning": "青春期"},
    {"word": "adolescent", "pronunciation": "[ˌædəˈlɛsnt]", "part_of_speech": "adj", "meaning": "青春期的"},
    {"word": "adore", "pronunciation": "[əˈdor]", "part_of_speech": "vt", "meaning": "珍愛"},
    {"word": "adulthood", "pronunciation": "[əˈdʌlthʊd]", "part_of_speech": "n", "meaning": "成年時期"},
    {"word": "advertiser", "pronunciation": "[ˈædvɚˌtaɪzɚ]", "part_of_speech": "n", "meaning": "登廣告者"},
    {"word": "affection", "pronunciation": "[əˈfɛkʃən]", "part_of_speech": "n", "meaning": "情愛"},
    {"word": "agenda", "pronunciation": "[əˈdʒɛndə]", "part_of_speech": "n", "meaning": "議程"},
    {"word": "agony", "pronunciation": "[ˈægənɪ]", "part_of_speech": "n", "meaning": "痛苦"},
    {"word": "agricultural", "pronunciation": "[ˌægrɪˈkʌltʃərəl]", "part_of_speech": "adj", "meaning": "農業的"},
    {"word": "AI/artificial intelligence", "pronunciation": "[ˌɑrtəˈfɪʃəl] [ɪnˈtɛlədʒəns]", "part_of_speech": "n", "meaning": "人工智慧"},
    {"word": "airtight", "pronunciation": "[ˈɛrˌtaɪt]", "part_of_speech": "adj", "meaning": "密閉的"},
    {"word": "airway", "pronunciation": "[ˈɛrˌwe]", "part_of_speech": "n", "meaning": "呼吸道；(礦井的)風道"},
    {"word": "aisle", "pronunciation": "[aɪl]", "part_of_speech": "n", "meaning": "走道；通道"},
    {"word": "algebra", "pronunciation": "[ˈældʒəbrə]", "part_of_speech": "n", "meaning": "代數"},
    {"word": "alien", "pronunciation": "[ˈelɪən]", "part_of_speech": "n/adj", "meaning": "外國人；外星人；外星的；外國的"},
    {"word": "allergic", "pronunciation": "[əˈlɝdʒɪk]", "part_of_speech": "adj", "meaning": "過敏的"},
    {"word": "allergy", "pronunciation": "[ˈælɚdʒɪ]", "part_of_speech": "n", "meaning": "過敏"},
    {"word": "alligator", "pronunciation": "[ˈæləˌgetɚ]", "part_of_speech": "n", "meaning": "鱷魚"},
    {"word": "ally", "pronunciation": "[əˈlaɪ]", "part_of_speech": "n", "meaning": "同盟者"},
    {"word": "alter", "pronunciation": "[ˈɔltɚ]", "part_of_speech": "vt.vi", "meaning": "改變"},
    {"word": "alternate", "pronunciation": "[ˈɔltɚnɪt]", "part_of_speech": "vt.vi.adj.n", "meaning": "替換(者)"},
    {"word": "altitude", "pronunciation": "[ˈæltəˌtjud]", "part_of_speech": "n", "meaning": "海拔"},
    {"word": "ample", "pronunciation": "[ˈæmpəl]", "part_of_speech": "adj", "meaning": "足夠的"},
    {"word": "anchor", "pronunciation": "[ˈæŋkɚ]", "part_of_speech": "n", "meaning": "錨"},
    {"word": "anthem", "pronunciation": "[ˈænθəm]", "part_of_speech": "n", "meaning": "讚美詩；聖歌；國歌"},
    {"word": "antique", "pronunciation": "[ænˈtik]", "part_of_speech": "n", "meaning": "骨董"},
    {"word": "applaud", "pronunciation": "[əˈplɔd]", "part_of_speech": "vt.vi", "meaning": "鼓掌"},
    {"word": "applause", "pronunciation": "[əˈplɔz]", "part_of_speech": "n", "meaning": "掌聲"},
    {"word": "apt", "pronunciation": "[æpt]", "part_of_speech": "adj", "meaning": "有…傾向的；聰明的"},
    {"word": "architect", "pronunciation": "[ˈɑrkəˌtɛkt]", "part_of_speech": "n", "meaning": "建築師"},
    {"word": "architecture", "pronunciation": "[ˈɑrkəˌtɛktʃɚ]", "part_of_speech": "n", "meaning": "建築"},
    {"word": "arena", "pronunciation": "[əˈrinə]", "part_of_speech": "n", "meaning": "競技場"},
    {"word": "armor", "pronunciation": "[ˈɑrmɚ]", "part_of_speech": "n", "meaning": "盔甲"},
    {"word": "ascend", "pronunciation": "[əˈsɛnd]", "part_of_speech": "vt.vi", "meaning": "上升"},
    {"word": "ass", "pronunciation": "[æs]", "part_of_speech": "n", "meaning": "驢子；笨蛋；屁股"},
    {"word": "assault", "pronunciation": "[əˈsɔlt]", "part_of_speech": "vt.n/vi", "meaning": "攻擊/動武"},
    {"word": "asset", "pronunciation": "[ˈæsɛt]", "part_of_speech": "n", "meaning": "資產"},
    {"word": "astonish", "pronunciation": "[əˈstɑnɪʃ]", "part_of_speech": "vt", "meaning": "震驚"},
    {"word": "astonishment", "pronunciation": "[əˈstɑnɪʃmənt]", "part_of_speech": "n", "meaning": "震驚"},
    {"word": "astray", "pronunciation": "[əˈstre]", "part_of_speech": "adv", "meaning": "迷路地"},
    {"word": "astronaut", "pronunciation": "[ˈæstrəˌnɔt]", "part_of_speech": "n", "meaning": "太空人"},
    {"word": "astronomer", "pronunciation": "[əˈstrɑnəmɚ]", "part_of_speech": "n", "meaning": "天文學家"},
    {"word": "astronomy", "pronunciation": "[əsˈtrɑnəmɪ]", "part_of_speech": "n", "meaning": "天文學"},
    {"word": "attendance", "pronunciation": "[əˈtɛndəns]", "part_of_speech": "n", "meaning": "出席"},
    {"word": "auditorium", "pronunciation": "[ˌɔdəˈtorɪəm]", "part_of_speech": "n", "meaning": "禮堂"},
    {"word": "auxiliary", "pronunciation": "[ɔgˈzɪljərɪ]", "part_of_speech": "adj/n", "meaning": "輔助的/輔助者；助手；助動詞"},
    {"word": "awe", "pronunciation": "[ɔ]", "part_of_speech": "n/vt", "meaning": "敬畏/使...敬畏"},
    {"word": "awhile", "pronunciation": "[əˈhwaɪl]", "part_of_speech": "adv", "meaning": "片刻"},
    {"word": "bachelor", "pronunciation": "[ˈbætʃəlɚ]", "part_of_speech": "n", "meaning": "單身漢"},
    {"word": "backbone", "pronunciation": "[ˈbækˌbon]", "part_of_speech": "n", "meaning": "脊椎"},
    {"word": "badge", "pronunciation": "[bædʒ]", "part_of_speech": "n", "meaning": "徽章"},
    {"word": "ballot", "pronunciation": "[ˈbælət]", "part_of_speech": "n", "meaning": "選票"},
    {"word": "ban", "pronunciation": "[bæn]", "part_of_speech": "n/vt", "meaning": "禁止"},
    {"word": "bandit", "pronunciation": "[ˈbændɪt]", "part_of_speech": "n", "meaning": "土匪"},
    {"word": "banner", "pronunciation": "[ˈbænɚ]", "part_of_speech": "n", "meaning": "旗幟"},
    {"word": "banquet", "pronunciation": "[ˈbæŋkwɪt]", "part_of_speech": "n", "meaning": "宴會"},
    {"word": "barbarian", "pronunciation": "[bɑrˈbɛrɪən]", "part_of_speech": "n/adj", "meaning": "野蠻人/野蠻人的"},
    {"word": "barbershop", "pronunciation": "[ˈbɑrbɚˌʃɑp]", "part_of_speech": "n", "meaning": "(男)理髮廳"},
    {"word": "barefoot", "pronunciation": "[ˈbɛrˌfʊt]", "part_of_speech": "adj", "meaning": "赤腳的"},
    {"word": "barren", "pronunciation": "[ˈbærən]", "part_of_speech": "adj", "meaning": "貧瘠的；不孕的"},
    {"word": "bass", "pronunciation": "[bes]", "part_of_speech": "n", "meaning": "低音樂器；男低音；鱸魚"},
    {"word": "batch", "pronunciation": "[bætʃ]", "part_of_speech": "n", "meaning": "一批"},
    {"word": "batter", "pronunciation": "[ˈbætɚ]", "part_of_speech": "vt.vi", "meaning": "猛擊"},
    {"word": "bazaar", "pronunciation": "[bəˈzɑr]", "part_of_speech": "n", "meaning": "市場"},
    {"word": "beautify", "pronunciation": "[ˈbjutəˌfaɪ]", "part_of_speech": "vt.vi", "meaning": "美化"},
    {"word": "beforehand", "pronunciation": "[bɪˈforˌhænd]", "part_of_speech": "adv", "meaning": "預先地"},
    {"word": "behalf", "pronunciation": "[bɪˈhæf]", "part_of_speech": "n", "meaning": "代表"},
    {"word": "belongings", "pronunciation": "[bəˈlɔŋɪŋz]", "part_of_speech": "n", "meaning": "財產"},
    {"word": "beloved", "pronunciation": "[bɪˈlʌvɪd]", "part_of_speech": "adj", "meaning": "心愛的"},
    {"word": "beneficial", "pronunciation": "[ˌbɛnəˈfɪʃəl]", "part_of_speech": "adj", "meaning": "有益(利)的"},
    {"word": "beware", "pronunciation": "[bɪˈwɛr]", "part_of_speech": "v", "meaning": "當心"},
    {"word": "bid", "pronunciation": "[bɪd]", "part_of_speech": "vt/n", "meaning": "命令；吩咐；向…表示；出價/出價；努力"},
    {"word": "blacksmith", "pronunciation": "[ˈblækˌsmɪθ]", "part_of_speech": "n", "meaning": "鐵匠"},
    {"word": "blast", "pronunciation": "[blæst]", "part_of_speech": "n/v", "meaning": "強風；爆炸/爆炸"},
    {"word": "blaze", "pronunciation": "[blez]", "part_of_speech": "n/v", "meaning": "火焰/燃燒"},
    {"word": "bleach", "pronunciation": "[blitʃ]", "part_of_speech": "vt.vi.n", "meaning": "漂白(劑)"},
    {"word": "blizzard", "pronunciation": "[ˈblɪzɚd]", "part_of_speech": "n", "meaning": "暴風雪"},
    {"word": "blond/blonde", "pronunciation": "[blɑnd]", "part_of_speech": "adj/n", "meaning": "金髮的/金髮人"},
    {"word": "blot", "pronunciation": "[blɑt]", "part_of_speech": "n", "meaning": "汙漬"},
    {"word": "blues", "pronunciation": "[bluz]", "part_of_speech": "n", "meaning": "憂鬱"},
    {"word": "blur", "pronunciation": "[blɝ]", "part_of_speech": "n/v", "meaning": "模糊/使…模糊"},
    {"word": "bodily", "pronunciation": "[ˈbɑdɪlɪ]", "part_of_speech": "adj", "meaning": "身體的"},
    {"word": "bodyguard", "pronunciation": "[ˈbɑdɪˌgɑrd]", "part_of_speech": "n", "meaning": "保鑣"},
    {"word": "bog", "pronunciation": "[bɑg]", "part_of_speech": "n/vt.vi", "meaning": "沼澤/(使)陷入泥淖"},
    {"word": "bolt", "pronunciation": "[bolt]", "part_of_speech": "n/vt.vi", "meaning": "門閂；閃電/閂住"},
    {"word": "bonus", "pronunciation": "[ˈbonəs]", "part_of_speech": "n", "meaning": "紅利"},
    {"word": "boom", "pronunciation": "[bum]", "part_of_speech": "n/vi/vt", "meaning": "(發出)隆隆聲；(使)興旺"},
    {"word": "booth", "pronunciation": "[buθ]", "part_of_speech": "n", "meaning": "小亭"},
    {"word": "boredom", "pronunciation": "[ˈbordəm]", "part_of_speech": "n", "meaning": "無聊"},
    {"word": "bosom", "pronunciation": "[ˈbʊzəm]", "part_of_speech": "n", "meaning": "胸；乳房"},
    {"word": "botany", "pronunciation": "[ˈbɑtənɪ]", "part_of_speech": "n", "meaning": "植物學"},
    {"word": "boulevard", "pronunciation": "[ˈbuləˌvɑrd]", "part_of_speech": "n", "meaning": "林蔭大道"},
    {"word": "bound", "pronunciation": "[baʊnd]", "part_of_speech": "vi/vt", "meaning": "(使)跳躍"},
    {"word": "boundary", "pronunciation": "[ˈbaʊndrɪ]", "part_of_speech": "n", "meaning": "邊界"},
    {"word": "bowel", "pronunciation": "[ˈbaʊəl]", "part_of_speech": "n", "meaning": "腸"},
    {"word": "boxer", "pronunciation": "[ˈbɑksɚ]", "part_of_speech": "n", "meaning": "拳擊手"},
    {"word": "boxing", "pronunciation": "[ˈbɑksɪŋ]", "part_of_speech": "n", "meaning": "拳擊"},
    {"word": "boyhood", "pronunciation": "[ˈbɔɪhʊd]", "part_of_speech": "n", "meaning": "少年時期"},
    {"word": "brace", "pronunciation": "[bres]", "part_of_speech": "n", "meaning": "支撐物；矯正器；大括號"},
    {"word": "braid", "pronunciation": "[bred]", "part_of_speech": "n", "meaning": "辮子"},
    {"word": "breadth", "pronunciation": "[brɛdθ]", "part_of_speech": "n", "meaning": "寬度"},
    {"word": "bribe", "pronunciation": "[braɪb]", "part_of_speech": "n/vt/vi", "meaning": "賄賂"},
    {"word": "briefcase", "pronunciation": "[ˈbrifˌkes]", "part_of_speech": "n", "meaning": "公事包"},
    {"word": "broaden", "pronunciation": "[ˈbrɔdn]", "part_of_speech": "vi/vt", "meaning": "拓寬"},
    {"word": "bronze", "pronunciation": "[brɑnz]", "part_of_speech": "n", "meaning": "青銅"},
    {"word": "brooch", "pronunciation": "[brotʃ]", "part_of_speech": "n", "meaning": "胸針"},
    {"word": "brood", "pronunciation": "[brud]", "part_of_speech": "n/vt/vi", "meaning": "一窩(卵、蟲、鳥)/孵出"},
    {"word": "broth", "pronunciation": "[brɔθ]", "part_of_speech": "n", "meaning": "湯"},
    {"word": "brotherhood", "pronunciation": "[ˈbrʌðɚˌhʊd]", "part_of_speech": "n", "meaning": "兄弟情誼"},
    {"word": "browse", "pronunciation": "[braʊz]", "part_of_speech": "vi/vt/n", "meaning": "瀏覽；吃草"},
    {"word": "bruise", "pronunciation": "[bruz]", "part_of_speech": "n", "meaning": "瘀青"},
    {"word": "bulge", "pronunciation": "[bʌldʒ]", "part_of_speech": "n", "meaning": "腫脹；凸塊"},
    {"word": "bulk", "pronunciation": "[bʌlk]", "part_of_speech": "n", "meaning": "體積；容積；大量"},
    {"word": "bully", "pronunciation": "[ˈbʊlɪ]", "part_of_speech": "n/vt/vi", "meaning": "霸凌；威嚇"},
    {"word": "bureau", "pronunciation": "[ˈbjʊro]", "part_of_speech": "n", "meaning": "局(處)"},
    {"word": "butcher", "pronunciation": "[ˈbʊtʃɚ]", "part_of_speech": "n", "meaning": "肉販"},
    {"word": "cactus", "pronunciation": "[ˈkæktəs]", "part_of_speech": "n", "meaning": "仙人掌"},
    {"word": "calf", "pronunciation": "[kæf]", "part_of_speech": "n", "meaning": "小牛"},
    {"word": "calligraphy", "pronunciation": "[kəˈlɪgrəfɪ]", "part_of_speech": "n", "meaning": "書法"},
    {"word": "canal", "pronunciation": "[kəˈnæl]", "part_of_speech": "n", "meaning": "運河"},
    {"word": "cannon", "pronunciation": "[ˈkænən]", "part_of_speech": "n", "meaning": "大砲"},
    {"word": "carbon", "pronunciation": "[ˈkɑrbən]", "part_of_speech": "n", "meaning": "炭"},
    {"word": "cardboard", "pronunciation": "[ˈkɑrdˌbord]", "part_of_speech": "n", "meaning": "硬紙板"},
    {"word": "carefree", "pronunciation": "[ˈkɛrˌfri]", "part_of_speech": "adj", "meaning": "無憂無慮的"},
    {"word": "caretaker", "pronunciation": "[ˈkɛrˌtekɚ]", "part_of_speech": "n", "meaning": "照顧者"},
    {"word": "carnation", "pronunciation": "[kɑrˈneʃən]", "part_of_speech": "n", "meaning": "康乃馨"},
    {"word": "carnival", "pronunciation": "[ˈkɑrnəvəl]", "part_of_speech": "n", "meaning": "嘉年華會"},
    {"word": "carp", "pronunciation": "[kɑrp]", "part_of_speech": "n", "meaning": "鯉魚"},
    {"word": "carton", "pronunciation": "[ˈkɑrtn]", "part_of_speech": "n", "meaning": "紙盒；紙箱"},
    {"word": "category", "pronunciation": "[ˈkætəˌgorɪ]", "part_of_speech": "n", "meaning": "種類；分類"},
    {"word": "cathedral", "pronunciation": "[kəˈθidrəl]", "part_of_speech": "n", "meaning": "大教堂"},
    {"word": "caution", "pronunciation": "[ˈkɔʃən]", "part_of_speech": "n", "meaning": "小心；謹慎"},
    {"word": "cautious", "pronunciation": "[ˈkɔʃəs]", "part_of_speech": "adj", "meaning": "小心的；謹慎的"},
    {"word": "celebrity", "pronunciation": "[sɪˈlɛbrətɪ]", "part_of_speech": "n", "meaning": "名人；名流；名聲"},
    {"word": "celery", "pronunciation": "[ˈsɛlərɪ]", "part_of_speech": "n", "meaning": "芹菜"},
    {"word": "cellar", "pronunciation": "[ˈsɛlɚ]", "part_of_speech": "n", "meaning": "地窖；地下室；酒窖"},
    {"word": "cell-phone", "pronunciation": "[ˈsɛlfon]", "part_of_speech": "n", "meaning": "手機"},
    {"word": "cello", "pronunciation": "[ˈtʃɛlo]", "part_of_speech": "n", "meaning": "大提琴"},
    {"word": "Celsius", "pronunciation": "[ˈsɛlsɪəs]", "part_of_speech": "n/adj", "meaning": "攝氏/攝氏的"},
    {"word": "ceremony", "pronunciation": "[ˈsɛrəˌmonɪ]", "part_of_speech": "n", "meaning": "典禮；儀式"},
    {"word": "certificate", "pronunciation": "[sɚˈtɪfəkɪt]", "part_of_speech": "n", "meaning": "證書"},
    {"word": "chairperson", "pronunciation": "[ˈtʃɛrˌpɝsn]", "part_of_speech": "n", "meaning": "議長；主席(無性別歧視)"},
    {"word": "chair", "pronunciation": "[ˈtʃɛrmən]", "part_of_speech": "n", "meaning": "主席"},
    {"word": "chairwoman", "pronunciation": "[ˈtʃɛrˌwʊmən]", "part_of_speech": "n", "meaning": "女主席"},
    {"word": "chant", "pronunciation": "[tʃænt]", "part_of_speech": "n/vt/vi", "meaning": "反覆地唱；吟誦"},
    {"word": "chatter", "pronunciation": "[ˈtʃætɚ]", "part_of_speech": "vt.vi.n", "meaning": "喋喋不休地說"},
    {"word": "checkbook", "pronunciation": "[ˈtʃɛkˌbʊk]", "part_of_speech": "n", "meaning": "支票簿"},
    {"word": "check-in", "pronunciation": "[ˈtʃɛkˌɪn]", "part_of_speech": "n", "meaning": "到達登記；報到"},
    {"word": "check-out", "pronunciation": "[ˈtʃɛkˌaʊt]", "part_of_speech": "n", "meaning": "檢查；結帳離開；退房"},
    {"word": "checkup", "pronunciation": "[ˈtʃɛkˌʌp]", "part_of_speech": "n", "meaning": "檢查；體檢"},
    {"word": "chef", "pronunciation": "[ʃɛf]", "part_of_speech": "n", "meaning": "主廚；大師傅"},
    {"word": "chemist", "pronunciation": "[ˈkɛmɪst]", "part_of_speech": "n", "meaning": "化學家"},
    {"word": "chestnut", "pronunciation": "[ˈtʃɛsˌnʌt]", "part_of_speech": "n", "meaning": "栗子"},
    {"word": "chili", "pronunciation": "[ˈtʃɪlɪ]", "part_of_speech": "n", "meaning": "胡椒"},
    {"word": "chimpanzee", "pronunciation": "[ˌtʃɪmpænˈzi]", "part_of_speech": "n", "meaning": "黑猩猩"},
    {"word": "choir", "pronunciation": "[kwaɪr]", "part_of_speech": "n", "meaning": "唱詩班"},
    {"word": "chord", "pronunciation": "[kɔrd]", "part_of_speech": "n", "meaning": "和弦；和音"},
    {"word": "chubby", "pronunciation": "[ˈtʃʌbɪ]", "part_of_speech": "adj", "meaning": "圓胖的；豐滿的"},
    {"word": "circuit", "pronunciation": "[ˈsɝkɪt]", "part_of_speech": "n", "meaning": "電路"},
    {"word": "cite", "pronunciation": "[saɪt]", "part_of_speech": "vt", "meaning": "引用；引…為證"},
    {"word": "civic", "pronunciation": "[ˈsɪvɪk]", "part_of_speech": "adj", "meaning": "公民的；市民的"},
    {"word": "clam", "pronunciation": "[klæm]", "part_of_speech": "n", "meaning": "蛤；鉗子"},
    {"word": "clan", "pronunciation": "[klæn]", "part_of_speech": "n", "meaning": "氏族；部落"},
    {"word": "clasp", "pronunciation": "[klæsp]", "part_of_speech": "vt.vi.n", "meaning": "緊握；緊抱；擁抱"},
    {"word": "clause", "pronunciation": "[klɔz]", "part_of_speech": "n", "meaning": "子句；條款"},
    {"word": "cling", "pronunciation": "[klɪŋ]", "part_of_speech": "vi", "meaning": "黏著；纏著；緊抓"},
    {"word": "clockwise", "pronunciation": "[ˈklɑkˌwaɪz]", "part_of_speech": "adj.adv", "meaning": "順時針的(地)"},
    {"word": "clover", "pronunciation": "[ˈklovɚ]", "part_of_speech": "n", "meaning": "苜蓿；三葉草"},
    {"word": "cluster", "pronunciation": "[ˈklʌstɚ]", "part_of_speech": "n", "meaning": "群；串；束"},
    {"word": "clutch", "pronunciation": "[klʌtʃ]", "part_of_speech": "vt.vi.n", "meaning": "抓住/離合器"},
    {"word": "coastline", "pronunciation": "[ˈkostˌlaɪn]", "part_of_speech": "n", "meaning": "海岸線"},
    {"word": "cocoon", "pronunciation": "[kəˈkun]", "part_of_speech": "n", "meaning": "繭"},
    {"word": "coil", "pronunciation": "[kɔɪl]", "part_of_speech": "n/vt.vi", "meaning": "線圈；捲/捲；盤繞"},
    {"word": "colleague", "pronunciation": "[ˈkɑlig]", "part_of_speech": "n", "meaning": "同事"},
    {"word": "colonel", "pronunciation": "[ˈkɝnəl]", "part_of_speech": "n", "meaning": "陸軍上校"},
    {"word": "colonial", "pronunciation": "[kəˈlonjəl]", "part_of_speech": "adj", "meaning": "殖民(地)的"},
    {"word": "combat", "pronunciation": "[ˈkɑmbæt]", "part_of_speech": "n/vt/vi", "meaning": "戰鬥"},
    {"word": "comedian", "pronunciation": "[kəˈmidɪən]", "part_of_speech": "n", "meaning": "喜劇演員"},
    {"word": "comet", "pronunciation": "[ˈkɑmɪt]", "part_of_speech": "n", "meaning": "彗星"},
    {"word": "commentator", "pronunciation": "[ˈkɑmənˌtetɚ]", "part_of_speech": "n", "meaning": "評論家"},
    {"word": "commission", "pronunciation": "[kəˈmɪʃən]", "part_of_speech": "n/vt", "meaning": "傭金/委任"},
    {"word": "commodity", "pronunciation": "[kəˈmɑdətɪ]", "part_of_speech": "n", "meaning": "商品；日用品"},
    {"word": "commonplace", "pronunciation": "[ˈkɑmənˌples]", "part_of_speech": "adj", "meaning": "平凡的"},
    {"word": "communism", "pronunciation": "[ˈkɑmjʊˌnɪzəm]", "part_of_speech": "n", "meaning": "共產主義"},
    {"word": "communist", "pronunciation": "[ˈkɑmjʊˌnɪst]", "part_of_speech": "n/adj", "meaning": "共產主義者/共產主義的"},
    {"word": "commute", "pronunciation": "[kəˈmjut]", "part_of_speech": "vi/n", "meaning": "通勤"},
    {"word": "commuter", "pronunciation": "[kəˈmjutɚ]", "part_of_speech": "n", "meaning": "通勤者"},
    {"word": "compact", "pronunciation": "[kəmˈpækt]", "part_of_speech": "adj", "meaning": "緊密的；小巧的"},
    {"word": "compass", "pronunciation": "[ˈkʌmpəs]", "part_of_speech": "n", "meaning": "指南針"},
    {"word": "compassion", "pronunciation": "[kəmˈpæʃən]", "part_of_speech": "n", "meaning": "同情"},
    {"word": "compassionate", "pronunciation": "[kəmˈpæʃənət]", "part_of_speech": "adj", "meaning": "有同情心的"},
    {"word": "compel", "pronunciation": "[kəmˈpɛl]", "part_of_speech": "vt", "meaning": "強迫"},
    {"word": "compliment", "pronunciation": "[ˈkɑmpləmənt]", "part_of_speech": "n/vt", "meaning": "恭維；稱讚"},
    {"word": "compound", "pronunciation": "[ˈkɑmpaʊnd]/[kəmˈpaʊnd]", "part_of_speech": "n/vt", "meaning": "混合物/合成"},
    {"word": "comprehend", "pronunciation": "[ˌkɑmprɪˈhɛnd]", "part_of_speech": "vt", "meaning": "理解"},
    {"word": "comprehension", "pronunciation": "[ˌkɑmprɪˈhɛnʃən]", "part_of_speech": "n", "meaning": "理解力"},
    {"word": "compromise", "pronunciation": "[ˈkɑmprəˌmaɪz]", "part_of_speech": "n/vt/vi", "meaning": "妥協；讓步"},
    {"word": "compute", "pronunciation": "[kəmˈpjut]", "part_of_speech": "vt.vi.n", "meaning": "計算"},
    {"word": "computerize", "pronunciation": "[kəmˈpjutəˌraɪz]", "part_of_speech": "vt", "meaning": "使電腦化"},
    {"word": "comrade", "pronunciation": "[ˈkɑmræd]", "part_of_speech": "n", "meaning": "夥伴"},
    {"word": "conceal", "pronunciation": "[kənˈsil]", "part_of_speech": "vt", "meaning": "隱藏"},
    {"word": "conceive", "pronunciation": "[kənˈsiv]", "part_of_speech": "vt/vi", "meaning": "想像"},
    {"word": "condemn", "pronunciation": "[kənˈdɛm]", "part_of_speech": "vt", "meaning": "譴責"},
    {"word": "conduct", "pronunciation": "[kənˈdʌkt]/[ˈkɑndʌkt]", "part_of_speech": "vt.vi/n", "meaning": "指揮；行為/行為；指導"},
    {"word": "confession", "pronunciation": "[kənˈfɛʃən]", "part_of_speech": "n", "meaning": "坦白；懺悔"},
    {"word": "confront", "pronunciation": "[kənˈfrʌnt]", "part_of_speech": "vt", "meaning": "面臨；遭遇"},
    {"word": "consent", "pronunciation": "[kənˈsɛnt]", "part_of_speech": "vi/n", "meaning": "同意"},
    {"word": "conserve", "pronunciation": "[kənˈsɝv]", "part_of_speech": "vt", "meaning": "保存；節省"},
    {"word": "considerate", "pronunciation": "[kənˈsɪdərɪt]", "part_of_speech": "adj", "meaning": "體諒的"},
    {"word": "console", "pronunciation": "[kənˈsol]", "part_of_speech": "vt", "meaning": "安慰"},
    {"word": "constitutional", "pronunciation": "[ˌkɑnstəˈtjuʃənəl]", "part_of_speech": "adj", "meaning": "憲法的"},
    {"word": "contagious", "pronunciation": "[kənˈtedʒəs]", "part_of_speech": "adj", "meaning": "有傳染性的"},
    {"word": "contaminate", "pronunciation": "[kənˈtæməˌnet]", "part_of_speech": "vt", "meaning": "汙染"},
    {"word": "contemplate", "pronunciation": "[ˈkɑntɛmˌplet]", "part_of_speech": "vt/vi", "meaning": "深思"},
    {"word": "contemporary", "pronunciation": "[kənˈtɛmpəˌrɛrɪ]", "part_of_speech": "adj", "meaning": "當代的"},
    {"word": "contempt", "pronunciation": "[kənˈtɛmpt]", "part_of_speech": "n", "meaning": "輕視"},
    {"word": "contend", "pronunciation": "[kənˈtɛnd]", "part_of_speech": "vt/vi", "meaning": "爭論；競爭"},
    {"word": "continental", "pronunciation": "[ˌkɑntəˈnɛntəl]", "part_of_speech": "adj", "meaning": "洲的；大陸的"},
    {"word": "continuity", "pronunciation": "[ˌkɑntəˈnjuətɪ]", "part_of_speech": "n", "meaning": "連貫性；持續性"},
    {"word": "convert", "pronunciation": "[kənˈvɝt]", "part_of_speech": "vt/vi", "meaning": "轉換；變成"},
    {"word": "convict", "pronunciation": "[kənˈvɪkt]", "part_of_speech": "vt", "meaning": "判...有罪；判決"},
    {"word": "coral", "pronunciation": "[ˈkɔrəl]", "part_of_speech": "n", "meaning": "珊瑚"},
    {"word": "corporation", "pronunciation": "[ˌkɔrpəˈreʃən]", "part_of_speech": "n", "meaning": "股份有限公司"},
    {"word": "copyright", "pronunciation": "[ˈkɑpɪˌraɪt]", "part_of_speech": "n", "meaning": "版權；著作權"},
    {"word": "correspondence", "pronunciation": "[ˌkɔrəˈspɑndəns]", "part_of_speech": "n", "meaning": "通信"},
    {"word": "corridor", "pronunciation": "[ˈkɔrɪdɚ]", "part_of_speech": "n", "meaning": "走廊；通道"},
    {"word": "corrupt", "pronunciation": "[kəˈrʌpt]", "part_of_speech": "vt/vi/adj", "meaning": "腐敗(的)"},
    {"word": "counsel", "pronunciation": "[ˈkaʊnsəl]", "part_of_speech": "n/vt/vi", "meaning": "忠告；商議"},
    {"word": "counselor", "pronunciation": "[ˈkaʊnsəlɚ]", "part_of_speech": "n", "meaning": "顧問；輔導員"},
    {"word": "cozy", "pronunciation": "[ˈkozɪ]", "part_of_speech": "adj", "meaning": "舒適的"},
    {"word": "counterclockwise", "pronunciation": "[ˌkaʊntɚˈklɑkˌwaɪz]", "part_of_speech": "adj.adv", "meaning": "逆時針的(地)"},
    {"word": "coupon", "pronunciation": "[ˈkupɑn]", "part_of_speech": "n", "meaning": "折價券；優待券"},
    {"word": "courtyard", "pronunciation": "[ˈkortˌjɑrd]", "part_of_speech": "n", "meaning": "庭院"},
    {"word": "cowardly", "pronunciation": "[ˈkaʊɚdlɪ]", "part_of_speech": "adj.adv", "meaning": "膽小的(地)"},
    {"word": "cracker", "pronunciation": "[ˈkrækɚ]", "part_of_speech": "n", "meaning": "脆餅；爆竹"},
    {"word": "crater", "pronunciation": "[ˈkretɚ]", "part_of_speech": "n", "meaning": "火山口"},
    {"word": "creak", "pronunciation": "[krik]", "part_of_speech": "vt.vi", "meaning": "發出喀吱聲"},
    {"word": "creek", "pronunciation": "[krik]", "part_of_speech": "n", "meaning": "小河"},
    {"word": "crib", "pronunciation": "[krɪb]", "part_of_speech": "n", "meaning": "嬰兒床"},
    {"word": "crocodile", "pronunciation": "[ˈkrɑkəˌdaɪl]", "part_of_speech": "n", "meaning": "鱷魚"},
    {"word": "crossing", "pronunciation": "[ˈkrɔsɪŋ]", "part_of_speech": "n", "meaning": "交叉點；十字路口"},
    {"word": "crouch", "pronunciation": "[kraʊtʃ]", "part_of_speech": "n/vt/vi", "meaning": "蹲伏"},
    {"word": "crunch", "pronunciation": "[krʌntʃ]", "part_of_speech": "v/n", "meaning": "(發出)嘎吱吱的聲音"},
    {"word": "crystal", "pronunciation": "[ˈkrɪstəl]", "part_of_speech": "n", "meaning": "水晶"},
    {"word": "cuisine", "pronunciation": "[kwɪˈzin]", "part_of_speech": "n", "meaning": "菜餚；烹飪"},
    {"word": "curb", "pronunciation": "[kɝb]", "part_of_speech": "n/vt", "meaning": "路邊；邊欄/抑制"},
    {"word": "currency", "pronunciation": "[ˈkɝənsɪ]", "part_of_speech": "n", "meaning": "貨幣；流通"},
    {"word": "curriculum", "pronunciation": "[kəˈrɪkjələm]", "part_of_speech": "n", "meaning": "課程"},
    {"word": "curry", "pronunciation": "[ˈkɝɪ]", "part_of_speech": "n", "meaning": "咖哩"},
    {"word": "customs", "pronunciation": "[ˈkʌstəmz]", "part_of_speech": "n", "meaning": "海關；關稅"},
    {"word": "dart", "pronunciation": "[dɑrt]", "part_of_speech": "n/vt/vi", "meaning": "鏢/投擲/急衝"},
    {"word": "dazzle", "pronunciation": "[ˈdæzəl]", "part_of_speech": "vt", "meaning": "使…目眩；耀眼"},
    {"word": "decay", "pronunciation": "[dɪˈke]", "part_of_speech": "n/vt/vi", "meaning": "腐朽；衰敗"},
    {"word": "deceive", "pronunciation": "[dɪˈsiv]", "part_of_speech": "vt/vi", "meaning": "欺騙；蒙蔽"},
    {"word": "declaration", "pronunciation": "[ˌdɛkləˈreʃən]", "part_of_speech": "n", "meaning": "宣言"},
    {"word": "delegate", "pronunciation": "[ˈdɛləˌget]", "part_of_speech": "n/vt", "meaning": "代表團團員/派...為代表"},
    {"word": "delegation", "pronunciation": "[ˌdɛləˈgeʃən]", "part_of_speech": "n", "meaning": "代表團；委任"},
    {"word": "democrat", "pronunciation": "[ˈdɛməˌkræt]", "part_of_speech": "n", "meaning": "民主主義者"},
    {"word": "denial", "pronunciation": "[dɪˈnaɪəl]", "part_of_speech": "n", "meaning": "否認；拒絕"},
    {"word": "descriptive", "pronunciation": "[dɪˈskrɪptɪv]", "part_of_speech": "adj", "meaning": "描述的"},
    {"word": "despair", "pronunciation": "[dɪˈspɛr]", "part_of_speech": "n/vi", "meaning": "絕望"},
    {"word": "despise", "pronunciation": "[dɪˈspaɪz]", "part_of_speech": "vt", "meaning": "輕視"},
    {"word": "destination", "pronunciation": "[ˌdɛstəˈneʃən]", "part_of_speech": "n", "meaning": "目的地"},
    {"word": "destiny", "pronunciation": "[ˈdɛstənɪ]", "part_of_speech": "n", "meaning": "命運"},
    {"word": "destructive", "pronunciation": "[dɪˈstrʌktɪv]", "part_of_speech": "adj", "meaning": "有破壞性的"},
    {"word": "devotion", "pronunciation": "[dɪˈvoʃən]", "part_of_speech": "n", "meaning": "奉獻；忠誠；熱愛"},
    {"word": "devour", "pronunciation": "[dɪˈvaʊr]", "part_of_speech": "vt", "meaning": "吞食"},
    {"word": "dialect", "pronunciation": "[ˈdaɪəlɛkt]", "part_of_speech": "n", "meaning": "方言"},
    {"word": "disbelief", "pronunciation": "[ˌdɪsbəˈlif]", "part_of_speech": "n", "meaning": "不信；懷疑"},
    {"word": "discard", "pronunciation": "[ˈdɪskɑrd]", "part_of_speech": "n", "meaning": "丟棄"},
    {"word": "disciple", "pronunciation": "[dɪˈsaɪpəl]", "part_of_speech": "n", "meaning": "信徒；門徒"},
    {"word": "discriminate", "pronunciation": "[dɪˈskrɪməˌnet]", "part_of_speech": "vt/vi", "meaning": "辨別；歧視"},
    {"word": "dispense", "pronunciation": "[dɪˈspɛns]", "part_of_speech": "vt", "meaning": "分配；分送；執行"},
    {"word": "dispose", "pronunciation": "[dɪˈspoz]", "part_of_speech": "vt/vi", "meaning": "處理；整理；配置"},
    {"word": "distinction", "pronunciation": "[dɪˈstɪŋkʃən]", "part_of_speech": "n", "meaning": "差別；卓越"},
    {"word": "distinctive", "pronunciation": "[dɪˈstɪŋktɪv]", "part_of_speech": "adj", "meaning": "有特色的"},
    {"word": "distress", "pronunciation": "[dɪˈstrɛs]", "part_of_speech": "n/vt", "meaning": "痛苦/使痛苦"},
    {"word": "document", "pronunciation": "[ˈdɑkjəmənt]", "part_of_speech": "n", "meaning": "文件"},
    {"word": "doorstep", "pronunciation": "[ˈdorˌstɛp]", "part_of_speech": "n", "meaning": "門階"},
    {"word": "doorway", "pronunciation": "[ˈdorˌwe]", "part_of_speech": "n", "meaning": "出入口"},
    {"word": "dormitory", "pronunciation": "[ˈdɔrməˌtorɪ]", "part_of_speech": "n", "meaning": "學生宿舍"},
    {"word": "dough", "pronunciation": "[do]", "part_of_speech": "n", "meaning": "生麵團"},
    {"word": "downward(s)", "pronunciation": "[ˈdaʊnwɚd(z)]", "part_of_speech": "adj.adv", "meaning": "向下"},
    {"word": "drape", "pronunciation": "[drep]", "part_of_speech": "n/vt/vi", "meaning": "簾/覆蓋"},
    {"word": "dreadful", "pronunciation": "[ˈdrɛdfəl]", "part_of_speech": "adj", "meaning": "畏懼的；可怕的"},
    {"word": "dresser", "pronunciation": "[ˈdrɛsɚ]", "part_of_speech": "n", "meaning": "梳妝台；(劇場)服裝員"},
    {"word": "dressing", "pronunciation": "[ˈdrɛsɪŋ]", "part_of_speech": "n", "meaning": "沙拉醬；服飾"},
    {"word": "driveway", "pronunciation": "[ˈdraɪvˌwe]", "part_of_speech": "n", "meaning": "私人車道"},
    {"word": "duration", "pronunciation": "[djʊˈreʃən]", "part_of_speech": "n", "meaning": "持續期間"},
    {"word": "dusk", "pronunciation": "[dʌsk]", "part_of_speech": "n", "meaning": "黃昏"},
    {"word": "dwarf", "pronunciation": "[dwɔrf]", "part_of_speech": "n/adj", "meaning": "矮子/矮小的"},
    {"word": "dwell", "pronunciation": "[dwɛl]", "part_of_speech": "vi", "meaning": "居住"},
    {"word": "dwelling", "pronunciation": "[ˈdwɛlɪŋ]", "part_of_speech": "n", "meaning": "住處"},
    {"word": "eclipse", "pronunciation": "[ɪˈklɪps]", "part_of_speech": "n/vt", "meaning": "蝕"},
    {"word": "eel", "pronunciation": "[il]", "part_of_speech": "n", "meaning": "鰻；鱔魚"},
    {"word": "ego", "pronunciation": "[ˈigo]", "part_of_speech": "n", "meaning": "自我；自我意識"},
    {"word": "elaborate", "pronunciation": "[ɪˈlæbəˌret]", "part_of_speech": "adj/vi/vt", "meaning": "精巧的/詳述"},
    {"word": "elevate", "pronunciation": "[ˈɛləˌvet]", "part_of_speech": "vt", "meaning": "提升；抬高"},
    {"word": "embrace", "pronunciation": "[ɪmˈbres]", "part_of_speech": "vt/vi/n", "meaning": "擁抱"},
    {"word": "endeavor", "pronunciation": "[ɪnˈdɛvɚ]", "part_of_speech": "vi/n", "meaning": "努力；盡力"},
    {"word": "enroll", "pronunciation": "[ɪnˈrol]", "part_of_speech": "vt/vi", "meaning": "(使…)註冊"},
    {"word": "enrollment", "pronunciation": "[ɪnˈrolmənt]", "part_of_speech": "n", "meaning": "註冊"},
    {"word": "ensure", "pronunciation": "[ɪnˈʃʊr]", "part_of_speech": "vt", "meaning": "確保"},
    {"word": "enterprise", "pronunciation": "[ˈɛntɚˌpraɪz]", "part_of_speech": "n", "meaning": "企業；事業心"},
    {"word": "enthusiastic", "pronunciation": "[ɪnˌθjuzɪˈæstɪk]", "part_of_speech": "adj", "meaning": "熱心的"},
    {"word": "entitle", "pronunciation": "[ɪnˈtaɪtəl]", "part_of_speech": "vt", "meaning": "取名為…；始有資格"},
    {"word": "equate", "pronunciation": "[ɪˈkwet]", "part_of_speech": "vt", "meaning": "使相等；同等看待"},
    {"word": "erect", "pronunciation": "[ɪˈrɛkt]", "part_of_speech": "vt", "meaning": "豎立；使直立"},
    {"word": "erupt", "pronunciation": "[ɪˈrʌpt]", "part_of_speech": "vt/vi", "meaning": "爆發"},
    {"word": "escort", "pronunciation": "[ˈɛskɔrt]", "part_of_speech": "n/vt", "meaning": "護送者/護送"},
    {"word": "estate", "pronunciation": "[ɪsˈtet]", "part_of_speech": "n", "meaning": "財產"},
    {"word": "esteem", "pronunciation": "[ɪsˈtim]", "part_of_speech": "n/vt", "meaning": "尊重"},
    {"word": "eternal", "pronunciation": "[ɪˈtɝnəl]", "part_of_speech": "adj", "meaning": "不朽的；無休止的"},
    {"word": "ethic(s)", "pronunciation": "[ˈɛθɪk]", "part_of_speech": "n", "meaning": "倫理標準"},
    {"word": "evergreen", "pronunciation": "[ˈɛvɚˌgrin]", "part_of_speech": "n/adj", "meaning": "長青樹/常綠的"},
    {"word": "exaggeration", "pronunciation": "[ɪgˌzædʒəˈreʃən]", "part_of_speech": "n", "meaning": "誇大；誇張"},
    {"word": "exceed", "pronunciation": "[ɪkˈsid]", "part_of_speech": "vt/vi", "meaning": "超過；勝過"},
    {"word": "excel", "pronunciation": "[ɪkˈsɛl]", "part_of_speech": "vt/vi", "meaning": "勝過；擅長"},
]

sent_words = {}  # 每个伺服器的已发送单词列表，键为 guild_id

# 初始化資料庫
async def init_db():
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS guild_configs (
                guild_id TEXT PRIMARY KEY,
                channel_id BIGINT,
                reminder_time TEXT
            )
        ''')
        await conn.close()
        print("資料庫初始化成功")
    except Exception as e:
        print(f"資料庫初始化失敗: {e}")

# 載入配置（從資料庫）
async def load_config():
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        try:
            result = await conn.fetch('SELECT * FROM guild_configs')
            config = {"guilds": {row["guild_id"]: {
                "channel_id": row["channel_id"],
                "reminder_time": row["reminder_time"]
            } for row in result}}
            print(f"載入配置: {config}")
            return config
        finally:
            await conn.close()
    except Exception as e:
        print(f"載入配置失敗: {e}")
        return {"guilds": {}}

# 儲存配置（到資料庫）
async def save_config(config):
    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        try:
            for guild_id, settings in config["guilds"].items():
                await conn.execute(
                    '''
                    INSERT INTO guild_configs (guild_id, channel_id, reminder_time)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (guild_id) DO UPDATE
                    SET channel_id = $2, reminder_time = $3
                    ''',
                    guild_id, settings.get("channel_id"), settings.get("reminder_time")
                )
            print(f"成功保存配置: {config}")
        finally:
            await conn.close()
    except Exception as e:
        print(f"保存配置失敗: {e}")
        raise

# 获取随机未发送单词
def get_random_words(guild_id, num=5):
    if guild_id not in sent_words:
        sent_words[guild_id] = []
    available_words = [w for w in word_list if w["word"] not in sent_words[guild_id]]
    if len(available_words) < num:
        sent_words[guild_id].clear()
        available_words = word_list.copy()
        random.shuffle(available_words)
    return random.sample(available_words, min(num, len(available_words)))

# 发送单词提醒
async def send_word_reminder(guild_id, channel_id):
    print(f"執行每日單字提醒，伺服器 ID: {guild_id}, 頻道 ID: {channel_id}")
    channel = bot.get_channel(int(channel_id))
    if channel is None:
        print(f"未找到頻道！頻道 ID: {channel_id}, 伺服器: {[guild.name for guild in bot.guilds]}")
        return
    if not channel.permissions_for(channel.guild.me).send_messages:
        print(f"機器人無權在頻道 {channel.name} (ID: {channel_id}) 發送訊息")
        return
    try:
        words = get_random_words(guild_id, 5)
        message = "📚 **每日單字提醒 (Level 5)** 📚\n\n"
        for word in words:
            message += (
                f"**單字**: {word['word']} {word['pronunciation']}\n"
                f"**詞性**: {word['part_of_speech']}\n"
                f"**釋義**: {word['meaning']}\n\n"
            )
            sent_words[guild_id].append(word["word"])
        await channel.send(message)
        print(f"成功發送單字提醒至頻道 {channel.name} (ID: {channel_id})，單字: {[word['word'] for word in words]}")
    except Exception as e:
        print(f"發送單字提醒失敗: {e}, 伺服器 ID: {guild_id}, 頻道 ID: {channel_id}")

# 设置排程
def setup_schedule(config):
    schedule.clear()
    if "guilds" not in config:
        print("配置中缺少 'guilds' 鍵，跳過排程設定")
        return
    for guild_id, settings in config["guilds"].items():
        channel_id = settings.get("channel_id")
        reminder_time = settings.get("reminder_time", "09:00")
        if channel_id is None:
            print(f"伺服器 {guild_id} 未設定頻道 ID，跳過排程設定")
            continue
        print(f"設定每日提醒時間: {reminder_time}, 伺服器 ID: {guild_id}, 頻道 ID: {channel_id}")
        schedule.every().day.at(reminder_time, "Asia/Shanghai").do(
            lambda gid=guild_id, cid=channel_id: bot.loop.create_task(send_word_reminder(gid, cid))
        )
    print(f"目前排程任務: {schedule.get_jobs()}")

# 异步排程循环
async def schedule_reminder():
    print("開始執行排程檢查...")
    while True:
        try:
            schedule.run_pending()
            print(f"檢查排程任務: {schedule.get_jobs()}")
        except Exception as e:
            print(f"排程執行錯誤: {e}")
        await asyncio.sleep(60)

# Bot 启动事件
@bot.event
async def on_ready():
    await init_db()  # 初始化資料庫
    config = await load_config()
    print(f'已登入為 {bot.user}')
    print(f"目前伺服器時間: {datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%H:%M:%S %Z')}")
    await asyncio.sleep(5)
    print(f"伺服器列表: {[guild.name for guild in bot.guilds]}")
    try:
        synced = await tree.sync()
        print(f"已同步 {len(synced)} 個斜線指令: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"指令同步失敗: {e}")
    setup_schedule(config)
    bot.loop.create_task(schedule_reminder())

# /word 指令
@tree.command(name="word", description="獲取隨機 Level 5 單字")
async def word(interaction: discord.Interaction):
    select = Select(
        placeholder="選擇要獲取的單字數量",
        options=[discord.SelectOption(label=f"{i} 個單字", value=str(i)) for i in range(1, 11)]
    )
    async def select_callback(interaction: discord.Interaction):
        num_words = int(select.values[0])
        guild_id = str(interaction.guild_id)
        words = get_random_words(guild_id, num_words)
        message = f"📚 **單字查詢 (Level 5, {num_words} 個)** 📚\n\n"
        for word in words:
            message += (
                f"**單字**: {word['word']} {word['pronunciation']}\n"
                f"**詞性**: {word['part_of_speech']}\n"
                f"**釋義**: {word['meaning']}\n\n"
            )
            if guild_id not in sent_words:
                sent_words[guild_id] = []
            sent_words[guild_id].append(word["word"])
        await interaction.response.edit_message(content=message, view=None)
    select.callback = select_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message("請選擇要獲取的單字數量：", view=view)

# /set_time 指令
@tree.command(name="set_time", description="設定每日單字提醒時間（格式：HH:MM，24小時制）")
@app_commands.describe(time="時間格式，例如 14:30")
async def set_time(interaction: discord.Interaction, time: str):
    config = await load_config()
    guild_id = str(interaction.guild_id)
    try:
        if not (len(time) == 5 and time[2] == ':' and time[:2].isdigit() and time[3:].isdigit()):
            raise ValueError("時間格式錯誤")
        hour = int(time[:2])
        minute = int(time[3:])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("時間範圍錯誤")
        if guild_id not in config["guilds"]:
            config["guilds"][guild_id] = {}
        config["guilds"][guild_id]["reminder_time"] = time
        await save_config(config)
        setup_schedule(config)  # 即時更新排程
        await interaction.response.send_message(f"每日單字提醒時間已設定為 {time} (CST)。")
        print(f"伺服器 {guild_id} 成功設定提醒時間: {time}")
    except ValueError as e:
        await interaction.response.send_message(f"請輸入有效的時間格式，例如 `/set_time 14:30`（24小時制）。錯誤：{str(e)}")
        print(f"伺服器 {guild_id} 時間格式錯誤: {str(e)}")
    except Exception as e:
        await interaction.response.send_message(f"設定時間時發生錯誤，請檢查日誌！錯誤：{str(e)}")
        print(f"伺服器 {guild_id} 設定提醒時間失敗: {str(e)}")

# /set_channel 指令
@tree.command(name="set_channel", description="設定每日單字提醒的頻道")
async def set_channel(interaction: discord.Interaction):
    config = await load_config()
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("此指令只能在伺服器中使用！")
        return
    text_channels = [channel for channel in guild.text_channels
                     if channel.permissions_for(guild.me).send_messages and
                     channel.permissions_for(guild.me).view_channel]
    if not text_channels:
        await interaction.response.send_message("目前伺服器沒有機器人可訪問的文字頻道！")
        return
    select = Select(
        placeholder="選擇每日提醒的頻道",
        options=[
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in text_channels[:25]
        ]
    )
    async def select_callback(interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        channel_id = int(select.values[0])
        channel = bot.get_channel(channel_id)
        if channel:
            if guild_id not in config["guilds"]:
                config["guilds"][guild_id] = {}
            config["guilds"][guild_id]["channel_id"] = channel_id
            await save_config(config)
            setup_schedule(config)  # 即時更新排程
            await interaction.response.edit_message(
                content=f"每日單字提醒頻道已設定為 {channel.name} (ID: {channel_id})。",
                view=None
            )
            print(f"伺服器 {guild_id} 成功設定頻道: {channel_id}")
        else:
            await interaction.response.edit_message(
                content=f"無法訪問選擇的頻道 (ID: {channel_id})，請確認機器人有權限！",
                view=None
            )
            print(f"伺服器 {guild_id} 無法訪問頻道: {channel_id}")
    select.callback = select_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message("請選擇每日單字提醒的頻道：", view=view)

# /help 指令
@tree.command(name="help", description="顯示所有可用指令的說明資訊")
async def help_command(interaction: discord.Interaction):
    config = await load_config()
    guild_id = str(interaction.guild_id)
    channel_info = "未設定（請使用 /set_channel 設定）"
    reminder_time = "未設定"
    if guild_id in config["guilds"]:
        channel_id = config["guilds"][guild_id].get("channel_id")
        reminder_time = config["guilds"][guild_id].get("reminder_time", "09:00")
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            channel_info = f"{channel.name} (ID: {channel_id})" if channel else f"ID: {channel_id} (無效)"
    message = (
        "📚 **單字學習機器人指令列表** 📚\n\n"
        "**/word** - 獲取隨機的 Level 5 單字（可選擇 1-10 個），包含發音、詞性與釋義。\n"
        "**/set_time <HH:MM>** - 設定每日單字提醒時間（24小時制，例如 14:30）。\n"
        "**/set_channel** - 設定每日單字提醒的頻道。\n"
        "**/help** - 顯示本說明資訊。\n"
        "**/test_channel** - 測試機器人是否能訪問指定頻道。\n"
        "**/test_reminder** - 手動觸發每日單字提醒。\n"
        "**/show_config** - 顯示當前配置檔案內容。\n\n"
        f"每日單字提醒將於每日 {reminder_time} 自動發送至指定頻道 ({channel_info})。\n"
        "⚠️ **注意**：請先使用 `/set_channel` 設定提醒頻道，否則每日提醒不會發送！"
    )
    await interaction.response.send_message(message)

# /test_channel 指令
@tree.command(name="test_channel", description="測試機器人是否能訪問指定頻道")
async def test_channel(interaction: discord.Interaction):
    config = await load_config()
    guild_id = str(interaction.guild_id)
    if guild_id not in config["guilds"] or not config["guilds"][guild_id].get("channel_id"):
        await interaction.response.send_message("尚未設定提醒頻道，請使用 `/set_channel` 設定！")
        return
    channel_id = config["guilds"][guild_id]["channel_id"]
    channel = bot.get_channel(int(channel_id))
    if channel:
        await channel.send("測試訊息：頻道訪問成功！")
        await interaction.response.send_message("成功發送訊息至目標頻道！")
    else:
        await interaction.response.send_message(f"無法訪問頻道 ID: {channel_id}, 伺服器: {[guild.name for guild in bot.guilds]}")

# /test_reminder 指令
@tree.command(name="test_reminder", description="手動觸發每日單字提醒")
async def test_reminder(interaction: discord.Interaction):
    config = await load_config()
    guild_id = str(interaction.guild_id)
    if guild_id not in config["guilds"] or not config["guilds"][guild_id].get("channel_id"):
        await interaction.response.send_message("尚未設定提醒頻道，請使用 `/set_channel` 設定！")
        return
    channel_id = config["guilds"][guild_id]["channel_id"]
    await send_word_reminder(guild_id, channel_id)
    await interaction.response.send_message("已手動觸發每日單字提醒！")

# /show_config 指令
@tree.command(name="show_config", description="顯示當前配置檔案內容")
async def show_config(interaction: discord.Interaction):
    config = await load_config()
    await interaction.response.send_message(f"當前配置：\n```json\n{json.dumps(config, indent=4, ensure_ascii=False)}\n```")

# 運行 Bot
try:
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        raise ValueError("未找到 DISCORD_BOT_TOKEN 環境變數，請在 Render Dashboard 設置！")
    bot.run(bot_token)
finally:
    asyncio.get_event_loop().close()