from bs4 import BeautifulSoup
import yaml


with open("ba-wiki.html", 'r', encoding='utf-8') as f:
    html_content = f.read()


# 使用 Beautiful Soup 解析 HTML 内容
soup = BeautifulSoup(html_content, 'html.parser')

character_div_elements = ''

# 提取包含 Character Name 的 div 元素
div_elements = div_element = soup.find('div', id='menu-23941')
for div in div_elements:
    character_div_elements = div.find_all('a', class_='item')

count = 0
data_list = []
data = {}

special_variants = []
special_variants_data = []

no_name_npc = ['行政官', '格黑娜学生', '温泉开发部部员', '风纪委员', '万魔殿学生', '急救医学部部员', '千年学生', '三一学生', '茶会学生',
               '正义实现委员会部员', '修女会成员', '玄龙门成员', '玄武商会成员', '魑魅一座', '亲卫队员', '工务部员', '女混混（HMG）',
               '女混混（SMG）', '女混混（SR）', '女混混（MG）', '钢盔团干部', '钢盔团成员', '阿里乌斯学生', '优斯提那信徒', '信徒泳装',
               ' 芭芭拉', '瓦尔基里学生', '瓦尔基里海警', '兔女郎卡牌']

# 打印提取的div元素内容
for div in character_div_elements:
    if div.text in no_name_npc:
        pass
    else:
        if '（' not in div.text or not [d for d in data_list if d.get('name') == div.text.split("（")[0]]:
            data = {
                'id': count,
                'name': div.text,
                'url': div.get('href'),
                'special': []
            }
            data_list.append(data)
            count += 1
        else:
            special = {
                'name': div.text,
                'url': div.get('href')
            }
            data = [d for d in data_list if d.get('name') == div.text.split("（")[0]][0]
            data['special'].append(special)
            data_list[data['id']] = data

            variant = div.text.split("（")[1][:-1]
            if variant not in special_variants:
                special_variants.append(variant)

count = 0

for variant in special_variants:
    special_variants_data.append({
        'id': count,
        'variant': variant,
        'character': []
    })
    count += 1

for data in data_list:
    name = data['name']
    if data['special']:
        for special in data['special']:
            variant_name = special['name'].split("（")[1][:-1]
            variant = [s for s in special_variants_data if s.get('variant') == variant_name][0]
            variant['character'].append(name)
            special_variants_data[variant['id']] = variant

with open("ba-character.yaml", 'w', encoding='utf-8') as f:
    f.writelines(yaml.dump(data_list, allow_unicode=True, sort_keys=False))

with open("ba-character-special-variants.yaml", 'w', encoding='utf-8') as f:
    f.writelines(yaml.dump(special_variants_data, allow_unicode=True, sort_keys=False))
