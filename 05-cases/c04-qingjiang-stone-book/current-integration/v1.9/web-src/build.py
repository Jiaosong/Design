from pathlib import Path
import html
import re

root = Path(__file__).resolve().parent

CHAPTERS = {
    "CH00": "项目定义",
    "CH01": "项目问题与机会",
    "CH02": "场地与山水分析",
    "CH03": "地域文化与内容分析",
    "CH04": "人群与使用状态分析",
    "CH05": "游程与行为分析",
    "CH06": "设计原理",
    "CH07": "设计方法",
    "CH08": "总体策略与体验系统",
    "CH09": "路线、交通与服务设计",
    "CH10": "十三印内容与互动系统",
    "CH11": "数字陪伴系统 / App",
    "CH12": "关键场景设计",
    "CH13": "实体、身体与感官设计",
    "CH14": "记忆、IP与文化产品",
    "CH15": "设计深化与细节",
    "CH16": "技术、模型与工程证明",
    "CH17": "方案演化与专业判断",
    "CH18": "开放项、回程与结尾",
}

PAGES = [
("001","CH00","项目封面 / Hero"),("002","CH00","清江石书是什么"),
("003","CH01","为什么需要重新设计清江游程"),("004","CH01","十三站问题 → 多分支网络问题"),("005","CH01","项目核心矛盾总图"),
("006","CH02","区域与清江山水格局"),("007","CH02","南北岸与跨江关系"),("008","CH02","真实游步网络分析"),("009","CH02","空间收放分析"),("010","CH02","观看尺度分析"),
("011","CH03","清江内容来源谱系"),("012","CH03","内容不是百科：什么适合进入什么场景"),("013","CH03","R07 地名阅读：仓禀峰 / 仓廪峰"),("014","CH03","文化如何进入旅程"),
("015","CH04","人群分析变量总图"),("016","CH04","儿童 / 亲子"),("017","CH04","青年 / 探索者"),("018","CH04","成年 / 深度阅读者"),("019","CH04","长者 / 低体力 / 低数字熟悉度"),("020","CH04","R06 同一场景四种使用深度"),
("021","CH05","完整游客旅程"),("022","CH05","身体状态随游程变化"),("023","CH05","注意力密度变化"),("024","CH05","互动动作语法"),
("025","CH06","原理01：真实清江优先"),("026","CH06","原理02：路线、服务与回程优先"),("027","CH06","原理03：三种观看尺度"),("028","CH06","原理04：内容可选 + 注意力随场景改变"),("029","CH06","原理05：数字退场 + 最小必要实体介入 + 记忆闭环"),
("030","CH07","方法01：证据 → 空间发现 → 设计后果"),("031","CH07","方法02：场景 × 注意力 × 人群"),("032","CH07","方法03：Landscape First → Relation Reveal"),("033","CH07","方法04：介入强度比较法"),
("034","CH08","清江石书总体系统图"),("035","CH08","景观 / 路线 / 内容 / 数字 / 实体 / 记忆六层关系"),("036","CH08","游程 × 系统矩阵"),
("037","CH09","ROUTE-03 总路线图"),("038","CH09","游船：水上看清江"),("039","CH09","索道：空中看清江"),("040","CH09","步行：山中探索网络"),("041","CH09","Return / Service / No-phone 路径"),
("042","CH10","十三印完整 R01–R13 总索引"),("043","CH10","十三印不是十三站：内容结构图"),("044","CH10","R05 / R06：景观与科学观察示例"),("045","CH10","R07 / R09 / R12：地名与地方故事示例"),("046","CH10","R13：内容退场示例"),
("047","CH11","App 项目定义 + 信息架构"),("048","CH11","TODAY / 今日清江"),("049","CH11","ROUTE / 探索地图"),("050","CH11","READ / 十三印阅读"),("051","CH11","R06 / Landscape First Reveal"),("052","CH11","R13 / PLAY OFF"),("053","CH11","MY BOOK / 我的石书"),("054","CH11","SERVICE / RETURN + Offline / No-phone"),
("055","CH12","R01：索道 / 移动观看"),("056","CH12","R05：景观发现"),("057","CH12","R06：Landscape First"),("058","CH12","R06：Relation Reveal"),("059","CH12","R06：身体恢复 + 人群深度"),("060","CH12","R13：进入 / 收束 / 通过"),("061","CH12","R13：退出 / 回望 / Return"),
("062","CH13","Physical 总体策略：什么时候值得加一个物"),("063","CH13","P02 倚靠恢复 / 当前 KEEP SUPPORT"),("064","CH13","P02 人体与使用动作"),("065","CH13","步步生光 / HOLD PROCESS"),("066","CH13","Fluid Rest / HOLD COMPETITION"),("067","CH13","Fluid Rest 人体 / 剖面 / 构造研究"),("068","CH13","清风吟 / Sensory HOLD"),
("069","CH14","清江旅记 / 实体记忆 Hero"),("070","CH14","我的石书 / 数字记忆 Hero"),("071","CH14","纸本 × 数字：一次旅程的双重记录"),("072","CH14","清江一线 / 清江雾气 / 红花峰崽等延展"),
("073","CH15","人体工学 / 使用尺度"),("074","CH15","平面 + 定位关系"),("075","CH15","立面 + 剖面"),("076","CH15","材料 / CMF / 触感 / 耐候"),("077","CH15","连接 / 拆换 / 排水 / 防滑 / 维护"),
("078","CH16","C22 / C23 空间关系总图"),("079","CH16","SEC-A 主技术剖面"),("080","CH16","R06 General Assembly"),("081","CH16","R06 Detail Atlas / D1–D4"),
("082","CH17","实体介入方案比较"),("083","CH17","数字设计演化"),("084","CH17","KEEP / HOLD / DROP 为什么"),
("085","CH18","哪些已经设计，哪些仍待现场验证"),("086","CH18","Return：怎么回来"),("087","CH18","最终页：第二次看见同一条江"),
]

# Current authority contract: CHAPTER != PAGE.
# 19 chapter containers contain 87 independent PAGE/article surfaces.
if len(CHAPTERS) != 19:
    raise RuntimeError(f"CHAPTER CONTRACT VIOLATION: {len(CHAPTERS)} != 19")
if len(PAGES) != 87:
    raise RuntimeError(f"PAGE CONTRACT VIOLATION: {len(PAGES)} != 87")
expected = [f"{i:03d}" for i in range(1,88)]
if [p[0] for p in PAGES] != expected:
    raise RuntimeError("PAGE-ID CONTRACT VIOLATION: expected continuous 001–087")

LEGACY_PAGE_FLOOR = 52
if len(PAGES) < LEGACY_PAGE_FLOOR:
    raise RuntimeError("NO-COMPRESSION VIOLATION")

nav = "".join(f'<a href="#p{pid}">{pid}</a>' for pid,_,_ in PAGES)
chapter_html=[]
for ch, ch_title in CHAPTERS.items():
    articles=[]
    for pid, pch, title in PAGES:
        if pch != ch:
            continue
        articles.append(
            f'<article class="page" id="p{pid}" data-page="{pid}" data-chapter="{ch}">'
            f'<div class="page-number">{pid}</div>'
            f'<div class="chapter-tag">{ch} · {html.escape(ch_title)}</div>'
            f'<h2>{html.escape(title)}</h2>'
            f'<div class="page-source-slot" data-page-source="{pid}"></div>'
            f'</article>'
        )
    chapter_html.append(
        f'<section class="chapter" id="{ch.lower()}" data-chapter-container="{ch}">'+"".join(articles)+"</section>"
    )

index = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>清江石书｜87页 Current Framework</title><link rel="stylesheet" href="styles.css"></head><body><nav class="page-index">{nav}</nav><main>{"".join(chapter_html)}</main><script src="app.js"></script></body></html>'''
(root/"index.html").write_text(index, encoding="utf-8")

# Preserve the existing visual style-parts pipeline. Finished-pixel runtime is persisted in
# C04_WEB_v1_9_87_PAGE_FRAMEWORK_FULL.zip; this build establishes the authoritative page structure.
styles=sorted((root/"style_parts").glob("*.css"))
(root/"styles.css").write_text("".join(p.read_text(encoding="utf-8") for p in styles), encoding="utf-8")

# Read back the generated structural contract.
rendered=(root/"index.html").read_text(encoding="utf-8")
chapter_count=len(re.findall(r'<section\b[^>]*class="[^"]*\bchapter\b', rendered, flags=re.I))
page_count=len(re.findall(r'<article\b[^>]*class="[^"]*\bpage\b', rendered, flags=re.I))
if chapter_count != 19 or page_count != 87:
    raise RuntimeError(f"POST-BUILD CONTRACT VIOLATION: chapters={chapter_count}, pages={page_count}")

print(root/"index.html")
print(root/"styles.css")
print(f"chapter_count={chapter_count}")
print(f"page_count={page_count}")
print(f"legacy_page_floor={LEGACY_PAGE_FLOOR}")
print("page_id_range=001-087")
