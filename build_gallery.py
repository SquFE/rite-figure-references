from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from html import escape
import json

ROOT=Path(__file__).parent
items=[
 dict(id='01_asap',name='ASAP',year=2025,p='066',title='ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills',box=(96,400,1130,1239),kind='动作序列',note='把不同技能排成横向时间序列，以连续姿态突出动态表现；不同服装和场景帮助区分技能。',borrow='借鉴起始、关键动作、结束的完整序列。你们应把恢复任务的一帧保留下来。',source='RSS 正式版'),
 dict(id='02_amo',name='AMO',year=2025,p='061',title='AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control',box=(96,348,1125,1039),kind='实景 + 物理标注',note='以真实操作场景为主体，用红色箭头、厘米数和关节方向线直接解释动作难度。',borrow='可标出威胁运动方向、避让方向与安全间隙；数字必须来自真实测量。',source='作者 arXiv 版本',arxiv='https://arxiv.org/abs/2505.03738'),
 dict(id='03_beamdojo',name='BeamDojo',year=2025,p='068',title='BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds',box=(96,426,1128,921),kind='同场景多帧叠影',note='在同一背景叠放多个时刻的机器人，用橙色箭头表现方向；下方小图补充窄梁和外力扰动。',borrow='非常适合呈现避障轨迹：保持相机固定，叠加运动阶段，并用单独颜色标示来袭物。',source='RSS 正式版'),
 dict(id='04_homie',name='HOMIE',year=2025,p='070',title='HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit',box=(98,386,1130,934),kind='多任务矩阵',note='九个子场景展示操作任务，每个子场景内部再用少量连续帧表现过程，传达能力覆盖面。',borrow='用行走、搬运、取放三种任务展示同一应急模块；每格给出可辨识的任务语境。',source='RSS 正式版'),
 dict(id='05_hugwbc',name='HugWBC',year=2025,p='067',title='A Unified and General Humanoid Whole-Body Controller for Versatile Locomotion',box=(151,355,1068,824),kind='按能力维度分组',note='按步态、上身任务和动态组合分行组织，通过行的结构体现不同能力维度。',borrow='可分为任务连续性、避让类型、控制器适配三组；避免把不同层次的证据混成一排。',source='RSS 正式版；标题按 PDF（目录使用 Fine-Grained Locomotion）'),
 dict(id='06_langwbc',name='LangWBC',year=2025,p='065',title='LangWBC: Language-directed Humanoid Whole-Body Control via End-to-end Learning',box=(111,347,1143,673),kind='简图 + 动作序列',note='左侧用极简模块解释输入和策略，右侧同场景连续动作；底部括号标出命令阶段，横向箭头强调切换。',borrow='最适合你们的横幅：左侧画参考中断与冻结跟踪器，右侧画执行任务 → 威胁出现 → 避让 → 恢复。',source='RSS 正式版'),
 dict(id='07_gettingup',name='HUMANUP',year=2025,p='063',title='Learning Getting-Up Policies for Real-World Humanoid Robots',box=(101,357,1127,981),kind='完整恢复过程',note='前两行用六帧展示仰卧起身与俯卧翻身，第三行展示不同地形；行标签明确说明能力。',borrow='用连续帧证明中断后的恢复过程，起始与结束状态都应完整可见。',source='作者 arXiv 版本',arxiv='https://arxiv.org/abs/2502.12152'),
 dict(id='08_standingup',name='HoST',year=2025,p='064',title='Learning Humanoid Standing-up Control across Diverse Postures',box=(98,403,1129,1044),kind='多姿态 + 鲁棒性',note='按 Diverse Postures 和 Robustness 分组，用场景中的连续姿态展示起身，并加入推扰、负载等条件。',borrow='把“不同任务起点”和“不同突发威胁”分开展示，让泛化对象清楚。',source='RSS 正式版'),
 dict(id='09_exbody',name='ExBody',year=2024,p='107',title='Expressive Whole-Body Control for Humanoid Robots',box=(96,381,1129,1008),kind='真实交互拼图',note='以户外、人机互动和表达性动作组成三行照片墙；不靠复杂架构图，靠真实语境建立直觉。',borrow='选择有明确人物、物体和任务关系的画面；不要让机器人姿态成为唯一信息。',source='作者 arXiv 版本',arxiv='https://arxiv.org/abs/2402.16796'),
 dict(id='10_humanoidbench',name='HumanoidBench',year=2024,p='061',title='HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation',box=(103,342,1123,598),kind='四场景横幅',note='四个大小一致的仿真场景并列，展示操作、搬运、导航和厨房任务，信息少而明确。',borrow='适合宽而矮的版式，借鉴等宽模块与统一相机尺度；你们还需加上应急发生的时间关系。',source='作者 arXiv 版本',arxiv='https://arxiv.org/abs/2403.10506'),
]
items += json.loads((ROOT/'additional_references.json').read_text())
for i in items:
    if 'p' in i:
        volume=21 if i['year']==2025 else 20
        i['url']=f"https://www.roboticsproceedings.org/rss{volume}/p{i['p']}.html"
        i['pdf']=i['url'].replace('.html','.pdf')
        i['venue']=f"RSS {i['year']}"
    i.setdefault('page_image',i['id'])
    im=Image.open(ROOT/'pages'/f"{i['page_image']}.png").convert('RGB')
    im.crop(i['box']).save(ROOT/'figures'/f"{i['id']}.jpg",quality=95)
    if i.get('method_image'):
        im=Image.open(ROOT/'pages'/f"{i['method_image']}.png").convert('RGB')
        im.crop(i['method_box']).save(ROOT/'figures'/f"{i['id']}-method.jpg",quality=95)
(ROOT/'references.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))

cards=[]
for n,i in enumerate(items,1):
    author=f' · <a href="{i["arxiv"]}" target="_blank" rel="noopener">截图版本</a>' if i.get('arxiv') else ''
    method=''
    if i.get('method_image'):
        method=f'''<details><summary>展开 Figure 2 · 模块画法参考</summary><button class="figure" aria-label="放大 {i['name']} 方法图" data-src="figures/{i['id']}-method.jpg" data-name="{i['name']} · Figure 2"><img src="figures/{i['id']}-method.jpg" alt="{i['name']} Figure 2"></button><p>{i['method_note']}</p><small>同一 PDF 的 Figure 2 / 第 {i['method_page']} 页。</small></details>'''
    paper_label='RSS 论文页' if 'p' in i else 'arXiv 论文页'
    pdf_label='正式 PDF' if 'p' in i else '指定 PDF'
    cards.append(f'''<article id="{i['id']}"><div class="card-head"><span class="number">{n:02}</span><div><h2>{i['name']}</h2><span class="venue">{i['venue']} · {i['kind']}</span></div></div>
    <button class="figure" aria-label="放大 {i['name']} 首图" data-src="figures/{i['id']}.jpg" data-name="{escape(i['title'],quote=True)}"><img src="figures/{i['id']}.jpg" alt="{i['name']} 论文 Figure 1" loading="lazy"></button>
    <div class="body"><p class="paper-title">{i['title']}</p><p><b>怎么画：</b>{i['note']}</p><p class="borrow"><b>RITE 可借鉴：</b>{i['borrow']}</p><div class="links"><a href="{i['url']}" target="_blank" rel="noopener">{paper_label} ↗</a><a href="{i['pdf']}" target="_blank" rel="noopener">{pdf_label} ↗</a><a href="pages/{i['page_image']}.png" target="_blank">完整第一页 ↗</a>{author}</div><small>图源：{i['source']}，Figure 1 / 第 1 页。原图版权归原作者所有。</small>{method}</div></article>''')
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>13 篇人形机器人论文 · Figure 1 构图参考</title><style>
:root{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;color:#202b38;background:#f3f5f7}*{box-sizing:border-box}body{margin:0}header,main,footer{max-width:1440px;margin:auto;padding:32px}header{padding-top:48px;padding-bottom:24px}.eyebrow{font-size:12px;font-weight:700;letter-spacing:.16em;color:#386662}h1{font-size:clamp(27px,3.2vw,44px);letter-spacing:-.04em;margin:14px 0}header p{font-size:16px;line-height:1.85;color:#536171;max-width:1040px}.suggestion{border-left:4px solid #2e7971;padding:14px 20px;background:#e6efec;border-radius:0 8px 8px 0;line-height:1.8}.suggestion a{font-weight:700}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px}article{background:white;border:1px solid #dee3e9;border-radius:12px;overflow:hidden;box-shadow:0 3px 12px #13283905}.card-head{display:flex;gap:16px;align-items:center;padding:22px 24px 18px}.number{font-size:26px;font-weight:700;color:#a5b7b3;font-variant-numeric:tabular-nums}h2{font-size:23px;margin:0 0 5px}.venue{font-size:13px;color:#6d7b8a}.figure{display:block;width:100%;padding:12px 18px;background:#fff;border:0;cursor:zoom-in}.figure img{display:block;width:100%;height:390px;object-fit:contain}.body{padding:0 24px 24px}.body p{font-size:14px;line-height:1.8;margin:10px 0}.paper-title{font-size:13px!important;color:#657383;min-height:43px}.borrow{background:#f0f5f3;padding:10px 12px;border-radius:6px}.links{display:flex;gap:16px;flex-wrap:wrap;margin:18px 0 10px;font-size:13px}a{color:#226e65;text-underline-offset:3px}small{display:block;color:#87919e;font-size:11px;line-height:1.6}footer{font-size:13px;color:#71808d;line-height:1.8}dialog{border:0;border-radius:12px;padding:14px;max-width:96vw;max-height:96vh;box-shadow:0 20px 80px #0006}dialog::backdrop{background:#152029d9}dialog img{display:block;max-width:92vw;max-height:80vh;object-fit:contain}details{margin-top:20px;border-top:1px solid #dfe7e4;padding-top:14px}summary{cursor:pointer;color:#226e65;font-size:14px;font-weight:600}details .figure{padding:14px 0}details .figure img{height:auto} .layout-plan{margin-top:26px;padding:24px;background:#fff;border:1px solid #dce5e1;border-radius:10px}.layout-plan h2{font-size:20px}.layout-plan>p{font-size:14px;margin:12px 0}.layout-main{padding:20px;border:1px solid #b7c9cf;background:#f1f6f8;border-radius:8px;text-align:center}.phase-row{display:flex;gap:12px;justify-content:space-between;margin:20px 0}.phase-row span{padding:14px 10px;background:white;border-radius:5px;flex:1;font-size:14px}.phase-row .key-phase{background:#ffe3c0;color:#8e4a03}.layout-scenes{display:flex;gap:12px;margin:12px 0}.layout-scenes>div{flex:1;background:#f5f7f7;padding:16px;text-align:center;border:1px solid #d8e1dd;border-radius:7px}.layout-scenes p{font-size:13px;margin:8px 0;line-height:1.7}.module-band{display:flex;align-items:center;justify-content:center;gap:12px;padding:18px 10px;border:1px solid #d9e2df;border-radius:7px}.module-band>span{font-size:14px;background:#e8eef1;padding:12px 18px;border-radius:6px;text-align:center}.module-band>span.reflex{background:#fde4be}.module-band i{font-style:normal}.module-band small{color:#665947}.layout-tip{font-size:13px!important} @media(max-width:600px){.layout-plan{padding:14px}.phase-row{gap:4px}.phase-row span{font-size:12px;padding:10px 4px}.module-band{gap:4px}.module-band>span{font-size:11px;padding:9px 5px}.module-band small{font-size:9px}} dialog .bar{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:4px 4px 12px;font-size:14px}#close{border:0;background:#e9edef;border-radius:6px;padding:8px 15px;cursor:pointer} @media(max-width:800px){header,main,footer{padding:22px}.grid{grid-template-columns:1fr}.figure img{height:auto;max-height:550px}.paper-title{min-height:0}}
</style><header><div class="eyebrow">PAPER FIGURE STUDY · HUMANOID ROBOTICS</div><h1>13 篇人形机器人论文，怎么画 Figure 1？</h1><p>原有 10 篇 RSS 论文，加上 Humanoid Dodgeball、SafeFall、PAC-MAN 三篇相关工作。首图均可点击放大；新增三篇还附有可展开的方法图。新增论文按指定 arXiv 版本标注，不将其归为已核实的 RSS 论文。</p><div class="suggestion"><b>按你的构图设想优先看：</b><a href="#12_safefall">SafeFall</a> 的主次场景布局、<a href="#11_dodgeball">Humanoid Dodgeball</a> 的连续帧叠影、<a href="#13_pacman">PAC-MAN</a> 的感知小窗，再结合 <a href="#06_langwbc">LangWBC</a> 的极简模块解释。</div>
<section class="layout-plan"><h2>RITE 排版草案：主场景 + 辅场景 + 模块带</h2><p>以下是拍摄与排版建议；任务名称仅作候选，不表示已完成实验。</p><div class="layout-main"><b>(a) 主场景 · 行走过程中的紧急避让</b><div class="phase-row"><span>t₀ 正常任务</span><span>t₁ 威胁出现</span><span class="key-phase">t₂ 关键避让</span><span>t₃ 恢复任务</span></div><small>同一固定机位 · 保留一次背景 · 叠加 3–4 个关键时刻</small></div><div class="layout-scenes"><div><b>(b) 辅场景 · 例如搬运</b><p>在同一场景内叠加动作<br>短标签解释任务连续性</p></div><div><b>(c) 辅场景 · 例如取放</b><p>在另一真实场景内叠加动作<br>短标签解释不同任务语境</p></div></div><div class="module-band"><span>Task reference</span><i>→</i><span class="reflex">RITE<br><small>Perception-triggered<br>interrupt / resume</small></span><i>→</i><span>Frozen tracker</span><i>→</i><span>Robot</span></div><p class="layout-tip"><b>画面规则：</b>关键避让姿态实色，其余时刻适度透明；威胁用红色轨迹，机器人运动用另一颜色；各场景独立叠帧，统一阶段标签。照片约占 80%，模块带约占 20%，不填未测得的时间或性能数字。</p></section></header><main class="grid">'''+''.join(cards)+'''</main><footer>来源：<a href="https://www.roboticsproceedings.org/rss21/">RSS 2025 正式论文集</a> · <a href="https://www.roboticsproceedings.org/rss20/">RSS 2024 正式论文集</a>。构图评论是针对图片的设计分析，不代表这些论文采用了 RITE 的方法。页面用于本地研究参考，论文图片未重新绘制或修改内容，仅裁切图区域；上方 RITE 排版草案为原创示意。</footer><dialog id="viewer"><div class="bar"><span id="caption"></span><button id="close">关闭 ×</button></div><img id="full" alt="放大的论文首图"></dialog><script>const viewer=document.querySelector('#viewer');document.querySelectorAll('.figure').forEach(b=>b.onclick=()=>{document.querySelector('#full').src=b.dataset.src;document.querySelector('#caption').textContent=b.dataset.name;viewer.showModal()});document.querySelector('#close').onclick=()=>viewer.close();viewer.onclick=e=>{if(e.target===viewer)viewer.close()};</script></html>'''
(ROOT/'index.html').write_text(html)

# Overview uses the original figures without changing their aspect ratios.
font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
bold_path='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
font=ImageFont.truetype(font_path,22)
bold=ImageFont.truetype(bold_path,29)
W=1800;cell_w=846;cell_h=690;gap=36;margin=36
rows=(len(items)+1)//2
sheet=Image.new('RGB',(W,rows*cell_h+(rows+1)*gap+80),'#f3f5f7');draw=ImageDraw.Draw(sheet)
draw.text((36,26),'13 Humanoid Papers | Figure 1 Reference Board',font=bold,fill='#243545')
for n,i in enumerate(items):
 x=margin+(n%2)*(cell_w+gap);y=100+(n//2)*(cell_h+gap)
 draw.rounded_rectangle((x,y,x+cell_w,y+cell_h),radius=12,fill='white',outline='#dbe2e7')
 draw.text((x+22,y+18),f"{n+1:02}  {i['name']}  |  {i['venue'].replace(' · ', ' / ')}",font=bold,fill='#263b48')
 im=Image.open(ROOT/'figures'/f"{i['id']}.jpg")
 im.thumbnail((cell_w-34,cell_h-90),Image.Resampling.LANCZOS)
 sheet.paste(im,(x+(cell_w-im.width)//2,y+70+(cell_h-90-im.height)//2))
sheet.save(ROOT/'figure1_overview.jpg',quality=93)
print('Gallery with 13 first figures and 3 method figures generated.')
