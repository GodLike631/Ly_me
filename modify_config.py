import os
import re
import random
import string
import glob
import datetime
import json

cnb_path = 'datas/cnb.json'
haitun_path = 'datas/haitun.json'
lz_path = 'datas/lz.json'

lock_file_path = 'datas/控制开关.txt'
tracker_path = 'datas/最新接口文件名.txt'

# ====================================================================
# ✍️ 【通道一：老杨专属点播手工加线区】
# ====================================================================
MY_CUSTOM_SITES = [
    {
        "key": "山楂影视",
        "name": "山楂影视.py",  
        "type": 3,
        "api": "https://ghfast.top/https://raw.githubusercontent.com/GodLike631/test/refs/heads/main/datas/%E5%B1%B1%E6%A5%82%E5%BD%B1%E8%A7%86.py",
        "searchable": 1,
        "quickSearch": 1
    },
    {
        "key": "红果短剧",
        "name": "红果短剧.py",  
        "type": 3,
        "api": "https://ghfast.top/https://raw.githubusercontent.com/GodLike631/test/refs/heads/main/datas/%E7%BA%A2%E6%9E%9C%E7%9F%AD%E5%89%A7.py",
        "searchable": 1,
        "quickSearch": 1
    }
]

# ====================================================================
# 📺 【通道二：老杨专属直播手工加线区】
# ====================================================================
MY_CUSTOM_LIVES = [
    {
        "name": "乡村电视 ｜Tg：@huliys9",
        "type": 0,
        "playerType": 2,
        "ua": "okhttp/5.3.2",
        "url": "https://gh-proxy.com/https://raw.githubusercontent.com/GodLike631/test/refs/heads/main/datas/%E4%B9%A1%E6%9D%91%E7%94%B5%E8%A7%86.txt"
    },
    {
        "name": "最新电影｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/GodLike631/Ly_18/refs/heads/main/datas/%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1.m3u"
    },
    {
        "name": "Kimentanm",
        "type": 0,
        "url": "https://ghfast.top/https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u",
        "playerType": 2
    },
    {
      "name": "综合直播",
      "type": 0,
      "playerType": 2,
      "url": "https://ghfast.top/https://raw.githubusercontent.com/develop202/migu_video/refs/heads/main/interface.txt",
      "ua": "bingcha/1.1 (mianfeifenxiang) "
    },
    {
        "name": "央卫TV｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "http://47.120.41.246:8025/vip/jar/zb.php"
    },
    {
        "name": "超稳定流畅｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/GodLike631/test/refs/heads/main/datas/%E8%B6%85%E7%A8%B3%E5%AE%9A%E6%B5%81%E7%95%85.txt"
    },
    {
        "name": "国产直播🔞｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/Ameria22/TV/refs/heads/main/data/01%E5%9B%BD%E4%BA%A7%E7%9B%B4%E6%92%AD_20260417_024507.m3u"
    },
    {
        "name": "国产精品🔞｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/Ameria22/TV/refs/heads/main/data/01%E5%9B%BD%E4%BA%A7%E7%B2%BE%E5%93%81_20260417_024507.m3u"
    },
    {
        "name": "4K福利🔞｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/Ameria22/TV/refs/heads/main/data/4k%E7%A6%8F%E5%88%A9.m3u"
    },
    {
        "name": "探花🔞｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://raw.githubusercontent.com/Ameria22/TV/refs/heads/main/data/01%E6%8E%A2%E8%8A%B1%E7%BA%A6%E7%82%AE_20260417_024507.m3u"
    },
    {
        "name": "欧美🔞｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://ghfast.top/https://raw.githubusercontent.com/Ameria22/TV/refs/heads/main/data/%E6%AC%A7%E7%BE%8E%E9%A2%91%E9%81%93.m3u"
    },
    {
        "name": "咪咕｜Tg：@huliys9",
        "type": 0,
        "ua": "okhttp/5.3.2",
        "url": "https://develop202.github.io/migu_video/interface.txt"
    },
    {
      "name": "Gather「IPTV」",
      "type": 3,
      "url": "https://iptv.yang-1989.xyz/playlist.m3u",
      "epg":"https://material.yang-1989.xyz/epg.xml.gz",
      "ua": "okhttp/3.8.1",
      "timeout": 10,
      "playerType": 2
    },
    {
      "name": "Live「直播」",
      "type": 3,
      "url": "https://live.yang-1989.eu.org/Live.m3u",
      "ua": "okhttp/3.8.1",
      "timeout": 10,
      "playerType": 2
    },
    {
      "name": "myTV「香港」",
      "type": 3,
      "url": "https://iptv.yang-1989.xyz/myTV/playlist.m3u",
      "epg":"https://material.yang-1989.xyz/epg.xml.gz",
      "ua": "okhttp/3.8.1",
      "timeout": 10,
      "playerType": 2
    },
    {
      "name": "Sport「体育」",
      "type": 3,
      "url": "https://cdn-1.yang-1989.xyz/sprt/playlist.m3u",
      "epg":"https://material.yang-1989.xyz/epg.xml.gz",
      "ua": "okhttp/3.8.1",
      "timeout": 10,
      "playerType": 2
    }
]

# ====================================================================
# ⏰ 洗牌与暗号逻辑
# ====================================================================
today = datetime.datetime.now()
current_month = str(today.month) 
is_reset_day = (today.day == 1)

saved_month, saved_code = "", ""
if os.path.exists(lock_file_path):
    with open(lock_file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if "-" in content:
            saved_month, saved_code = content.split("-", 1)
        else:
            saved_code = content

if is_reset_day and saved_month != current_month:
    current_token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    with open(lock_file_path, 'w', encoding='utf-8') as f:
        f.write(f"{current_month}-{current_token}")
else:
    if not saved_code or len(saved_code) != 3:
        current_token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
        with open(lock_file_path, 'w', encoding='utf-8') as f:
            f.write(f"{current_month}-{current_token}")
    else:
        current_token = saved_code

if current_token in ["全量版", "纯净版"]:
    output_filename = "老杨TV全量版.json"
else:
    output_filename = f"老杨TV全量版{current_token}.json"

output_path = f"datas/{output_filename}"

# ====================================================================
# 🧠 安全加载与对象级规范缝合
# ====================================================================
def load_json_safe(path):
    if not os.path.exists(path): return {}
    with open(path, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return {}

json_cnb = load_json_safe(cnb_path)
json_haitun = load_json_safe(haitun_path)
json_lz = load_json_safe(lz_path)

haitun_sites = json_haitun.get("sites", [])
haitun_lives = json_haitun.get("lives", [])
lz_sites = json_lz.get("sites", [])
cnb_sites = json_cnb.get("sites", [])
cnb_lives = json_cnb.get("lives", [])

# 传统站点洗白与去除非法路径
upstream_sites = haitun_sites + lz_sites + cnb_sites
clean_upstream_sites = []
custom_keys = {site.get("key") for site in MY_CUSTOM_SITES if site.get("key")}

for item in upstream_sites:
    if not item or not isinstance(item, dict): continue
    if item.get("key") in custom_keys: continue  # 被老杨手工特权覆盖
    
    # 清洗名字
    name = item.get("name", "")
    name = name.replace('🐬', '').replace('海豚影视', '').replace('海豚', '')
    name = name.replace('完全免费，如有收费的都是骗子', '').replace('交流群 TG：@hshsjk9', '').strip()
    item["name"] = name
    
    # 路径安全化远程替换
    s_api = item.get("api", "")
    if isinstance(s_api, str):
        if "PanWebShare" in s_api:
            item["api"] = "csp_PanWebShare"
            if "jar" in item: item.pop("jar")
        else:
            path_replacements = {
                './spider.jar': 'https://cnb.cool/fish2018/xs/-/git/raw/main/spider.jar',
                './XBPQ/': 'https://cnb.cool/fish2018/xs/-/git/raw/main/XBPQ/',
                './XYQHiker': 'https://cnb.cool/fish2018/xs/-/git/raw/main/XYQHiker/',
                './js/': 'https://cnb.cool/fish2018/xs/-/git/raw/main/js/',
                './json/': 'https://cnb.cool/fish2018/xs/-/git/raw/main/json/',
                './py/': 'https://cnb.cool/fish2018/xs/-/git/raw/main/py/'
            }
            for src, dst in path_replacements.items():
                if item["api"].startswith(src):
                    item["api"] = item["api"].replace(src, dst)
                    
    # 🎯 特殊处理：针对 New Video 依赖本地 Jar 的特殊站点做结构级属性注入（杜绝 replace 毁文件）
    if item.get("key") in ["hajim-腾讯备", "茫茫"]:
        item["spider"] = "./tvbox.jar"
        
    clean_upstream_sites.append(item)

# 直播流合并清洗
base_lives = haitun_lives + cnb_lives
clean_base_lives = []
custom_live_names = {live.get("name") for live in MY_CUSTOM_LIVES if live.get("name")}

for live in base_lives:
    if not live or not isinstance(live, dict): continue
    l_name = live.get("name", "")
    if l_name in custom_live_names or "日本女优" in l_name or "日本女友" in l_name: continue
    if not live.get("ua") or live.get("ua") == "okhttp":
        live["ua"] = "okhttp/5.3.2"
    clean_base_lives.append(live)

# 手工直播按排位算法归流
inserted_count = 0
for custom_live in MY_CUSTOM_LIVES:
    if "🔞" in custom_live.get("name", ""):
        clean_base_lives.append(custom_live)
    else:
        insert_idx = 5 + inserted_count
        if len(clean_base_lives) >= insert_idx:
            clean_base_lives.insert(insert_idx, custom_live)
        else:
            clean_base_lives.append(custom_live)
        inserted_count += 1

# 拼装全新底图结构
ordered_obj = {
    "spider": json_cnb.get("spider", "https://cnb.cool/fish2018/xs/-/git/raw/main/spider.jar"),
    "wallpaper": "https://img.naixiai.cn/2026/06/18/IMG_6638.jpeg",
    "notice": "👑 欢迎使用【老杨TV粉丝专属缝合专线】！纯净无广告！密码不定期自动更换！失效请回群获取最新链接！",
    "sites": [],
    "lives": clean_base_lives
}

# 九大方阵智能清洗分类落盘
block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8, block_9 = [], [], [], [], [], [], [], [], []
for site in (clean_upstream_sites + MY_CUSTOM_SITES):
    raw_name = site.get("name", "")
    s_key = site.get("key", "")
    
    # 过滤脏字符
    for char in ['丨', '┃', ' ']: raw_name = raw_name.strip(char)
    
    is_guazi = "瓜子" in raw_name or "GZ" == s_key
    is_nsfw = False if is_guazi else ("🔞" in raw_name or "色播" in raw_name or "av" in s_key.lower() or "爆料" in raw_name or "video" in raw_name.lower() or "md" in s_key.lower())
    
    if s_key == "热播影视":
        site["name"] = "热播 • APP｜合并自海豚佬 and 鱼佬接口，感谢付出｜@huliys9"
        site["category"] = "综合"
        block_1.append(site)
    elif "豆瓣" in raw_name and "首页" in raw_name:
        site["name"] = "🦋 豆瓣 • 首页"
        site["category"] = "综合"
        site["searchable"] = 0
        block_2.append(site)
    elif is_nsfw:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "福利"
        block_9.append(site)
    elif "短剧" in raw_name or "剧场" in raw_name:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "短剧"
        block_3.append(site)
    elif "动漫" in raw_name or "新番" in raw_name:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "动漫"
        block_4.append(site)
    elif "磁力" in raw_name or "云盘" in raw_name or "4k" in raw_name.lower():
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "网盘/磁力"
        block_5.append(site)
    elif "体育" in raw_name or "直播" in raw_name:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "体育/直播"
        block_6.append(site)
    elif "少儿" in raw_name or "课堂" in raw_name:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "少儿"
        site["searchable"] = 0
        block_7.append(site)
    else:
        site["name"] = f"🦋 {raw_name.replace('🦋','')}"
        site["category"] = "综合"
        block_2.append(site)

    if site.get("category") not in ["少儿", "音乐"] and "searchable" not in site:
        site["searchable"] = 1

# 爱奇艺官方对齐
for site in block_2:
    if site.get("key") == "AQY": site["name"] = "🦋 爱奇艺 ｜Tg：@huliys9"

ordered_obj["sites"] = block_1 + block_2 + block_3 + block_4 + block_6 + block_7 + block_8 + block_5 + block_9

# 解析与DOH安全归类
combined_parses = json_haitun.get("parses", []) + json_lz.get("parses", []) + json_cnb.get("parses", [])
unique_parses = []
seen_names = set()
for p in combined_parses:
    if p.get("name") and p["name"] not in seen_names:
        unique_parses.append(p)
        seen_names.add(p["name"])
ordered_obj["parses"] = unique_parses

# 规则与高级WebView广告过滤安全注入
ordered_obj["rules"] = [
    {
        "name": "老楊TV·雲端高級去广告JS注入",
        "hosts": ["vip.wwgz.cn", "lziplayer.com", "m3u8.apibdzy.com", "cj.ffzyapi.com"],
        "script": ["console.log('WebView AdBlock Active');"]
    }
]

# 安全落盘
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(ordered_obj, f, ensure_ascii=False, indent=4)
    
with open(tracker_path, 'w', encoding='utf-8') as f:
    f.write(output_filename)

print(f"🎉 修复版全量版更新成功！已杜绝文本割裂风险。配置输出至: {output_path}")

# ====================================================================
# 🛡️ 过期旧线调包轰炸安全沙箱化（防止误杀当天新线）
# ====================================================================
old_configs = glob.glob('datas/老杨TV全量版*.json')
for old_file in old_configs:
    if os.path.basename(old_file) != output_filename:
        try:
            trap_json = {
                "notice": "⚠️ 当前专线已过期断流！老链接已彻底作废！请重新加群获取暗号密码！",
                "sites": [{"key": "trap", "name": "🚨 专线密码已过期断流！请前往群获取最新密码", "type": 3, "api": "csp_JuDou"}]
            }
            with open(old_file, 'w', encoding='utf-8') as f:
                json.dump(trap_json, f, ensure_ascii=False, indent=4)
        except: pass
