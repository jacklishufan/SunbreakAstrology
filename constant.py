CONST_LST_SKILL = '''
1:攻击
2:挑战者
3:无伤
4:怨恨
5:死里逃生
6:看破
7:超会心
8:弱点特效
9:力量解放
10:精神抖擞
11:会心击【属性】
12:达人艺
13:火属性攻击强化
14:水属性攻击强化
15:冰属性攻击强化
16:雷属性攻击强化
17:龙属性攻击强化
18:毒属性强化
19:麻痹属性强化
20:睡眠属性强化
21:爆破属性强化
22:匠
23:利刃
24:弹丸节约
25:刚刃打磨
26:心眼
27:弹道强化
28:钝器能手
30:集中
31:强化持续
32:跑者
33:体术
34:耐力急速回复
35:防御性能
36:防御强化
37:攻击守势
38:拔刀术【技】
39:拔刀术【力】
40:纳刀术
41:击晕术
42:夺取耐力
43:滑走强化
44:吹笛名人
45:炮术
46:炮弹装填
47:特殊射击强化
48:通常弹・连射箭强化
49:贯穿弹・贯穿箭强化
50:散弹・扩散箭强化
51:装填扩充
52:装填速度
53:减轻后坐力
54:抑制偏移
55:速射强化
56:防御
57:精灵加护
58:体力回复量提升
59:回复速度
60:快吃
61:耳塞
62:风压耐性
63:耐震
64:泡沫之舞
65:回避性能
66:回避距离提升
67:火耐性
68:水耐性
69:冰耐性
70:雷耐性
71:龙耐性
72:属性异常状态的耐性
73:毒耐性
74:麻痹耐性
75:睡眠耐性
76:昏厥耐性
77:泥雪耐性
78:爆破异常状态的耐性
79:植生学
80:地质学
81:破坏王
84:幸运
85:砥石使用高速化
86:炸弹客
87:最爱蘑菇
88:道具使用强化
89:广域化
90:满足感
91:火场怪力
92:不屈
93:减轻胆怯
94:跳跃铁人
95:剥取铁人
96:饥饿耐性
97:飞身跃入
98:佯动
99:骑乘名人
103:龙气活性
104:翔虫使
105:墙面移动
106:逆袭
107:高速变形
108:鬼火缠
116:因祸得福
122:合气
123:提供
124:属性
125:攻势
126:零件改造
127:打磨术【锐】
128:刃鳞打磨
129:走壁移动【翔】
131:连击
121:嘲讽防御:
115:业铠
135:刚心
145:奋斗
139:粉尘绕
138:风绕:
143:狂龙翔
140:寒气炼成
141:龙气转换
137:狂化
'''

skills_mapping = [x.split(':') for x in CONST_LST_SKILL.split("\n") if x.strip()]
skills_mapping = {int(x[0]):x[1] for x in skills_mapping if len(x) == 2}

import pandas as pd
import numpy as np
all_slots = pd.read_csv("data/craft.txt",sep='\t',header=None)
all_slots = np.array(all_slots)

start = 0 
end = 6
tables = {}
for i in [1,2,3,4,5,6,13]:
    tables[i] = np.array(pd.DataFrame(all_slots[:,start:end]).dropna())
    start += 11
    end += 11

for i in [1,2,3,4,5,6,13]:
    tables[i] = {
        int(idx):dict(name=name,vals=[v1,v2,v3]) for (_,idx,name,v1,v2,v3) in tables[i]
    }

import json
def dump_json(data,path):
    with open(path,'w',encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))

REGISTRY = dict(
    skills_mapping=skills_mapping,
    crafts_mapping=tables,
)
dump_json(REGISTRY,'data/compiled.json')