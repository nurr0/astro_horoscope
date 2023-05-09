import requests
import json
from fastapi.responses import JSONResponse


def get_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').text
    result = {'data': json.loads(response)['content']['text'][0]['content']}
    return result


def get_full_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').json()
    return response


def get_name_meaning(name):
    try:
        with open('name_dict.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            name_info = data[name]
    except:
        name_info = JSONResponse(content={"detail": "Not found"}, status_code=404)
    return name_info


letter_values = {
    "А": 1, "И": 1, "С": 1, "Ъ": 1,
    "Б": 2, "Й": 2, "Т": 2, "Ы": 2,
    "В": 3, "К": 3, "У": 3, "Ь": 3,
    "Г": 4, "Л": 4, "Ф": 4, "Э": 4,
    "Д": 5, "М": 5, "Х": 5, "Ю": 5,
    "Е": 6, "Н": 6, "Ц": 6, "Я": 6,
    "Ё": 7, "О": 7, "Ч": 7,
    "Ж": 8, "П": 8, "Ш": 8,
    "З": 9, "Р": 9, "Щ": 9
}


def name_to_num(name, familyname, fathername):
    num_name = ''.join([str(letter_values[i]) for i in name.strip().upper().replace(' ', '').replace('-', '')])
    num_familyname = ''.join(
        [str(letter_values[i]) for i in familyname.strip().upper().replace(' ', '').replace('-', '')])
    num_fathername = ''.join(
        [str(letter_values[i]) for i in fathername.strip().upper().replace(' ', '').replace('-', '')])
    num_fullname = num_name + num_fathername + num_familyname
    num_name = int(num_fullname)
    while num_name >= 10:
        num_name = sum(int(digit) for digit in str(num_name))
        num_name = int(str(num_name).replace('0', ''))
        if num_name == 11 or num_name == 22:
            return num_name
    return num_name


def name_analys(name, familyname, fathername):
    num_explanation = {
        1: 'Означает личность, полную энергии и желания действовать. Большую пользу оно оказывает при действиях в сиюминутной, непосредственной обстановке, в ситуациях внезапных и неожиданных, меньшую – в запланированных ситуациях. Категорически противопоказаны рискованные мероприятия и вложения в малоперспективный бизнес. Лучше всего – исполнять порученные задания. С числом 1 ассоциируется уверенность в своих силах и возможностях, такие понятия, как смелость и храбрость. Но натура этих людей более подражающая, чем творческая. Деньги они умеют как зарабатывать, так и тратить. Следует избегать опрометчивых решений.',
        2: 'Символизирует изменчивый характер, эмоциональное и внутреннее беспокойство, которые могут довести человека до полной неуверенности или даже фатализма. Не беспокоиться по мелочам и всяким незначительным действиям, избегать споров и ссор. Наилучший успех принесет совместная работа с друзьями, коллегами.',
        3: 'Символизирует талант, разносторонность, веселость, указывает на науку, мир искусства, спортивную жизнь, на все, что служит отдушиной человеку, его хобби. Если данная личность примет полезные советы и поступит разумно при выборе профессии, планировании своей карьеры, то это окажется путь, ведущий к успеху и славе.',
        4: 'Означает успех в научных и технических областях, особенно в индустрии. Оно символизирует надежность и стабильность, добросовестность, приобретение друзей и достижение признания. Более того, такой человек полезен в экстремальных ситуациях, в трудных условиях, когда с наилучшей стороны раскрываются качества его характера и нравы. Это никогда не следует недооценивать.',
        5: 'Символизирует исполненную энтузиазма натуру, любящую приключения и рискованные мероприятия, склонную ко всему необычному. Эти люди подвижны, любят поездки и путешествия и везде чувствуют себя как дома. Они быстро и легко усваивают иностранные языки, традиции других народов. Часто их действия и поведение оказываются совершенно внезапными и неожиданными, с непредсказуемыми последствиями. При всех затруднениях они выходят сухими из воды. Во многом им в жизни помогает находчивость и остроумие, их жизнерадостность. Любовь к частым переменам мешает им оценить настоящее, увидеть реальные перспективы. Они всегда устремлены только вперед и не видят то, что под рукой.',
        6: 'Предвещает успех в предприятиях, если только удается завоевать доверие у окружающих, привлечь не только клиентов, но и последователей. Часто из них получаются или политические деятели, или высокие государственные чиновники. Они становятся известными в обществе своими научными или философскими взглядами, но при условии, что их слово совпадает с делами. Ведь общество ждет от них реализации сказанного. Они быстро усваивают ту истину, что честность плодотворнее честолюбия, что честные усилия не пропадают даром, что добрые, благие поступки помогут достигнуть цели, не прибегая к радикальным методам.',
        7: 'Таит в себе способность направлять талант в сферу науки, в мир искусства или философии, в религиозную деятельность. Но успех их деятельности во многом зависит от глубокого анализа результатов уже достигнутого и от реального планирования своего будущего. Понимая других людей, они нередко становятся лидерами и учителями самого высокого класса. Но если они решили заняться коммерческим или финансовыми делами, то здесь им самим потребуется помощь со стороны.',
        8: 'Благоприятствует деятельности в сфере значительных, крупных дел, предвещая и материальные блага. Заканчивая успешно одно дело, эти люди сразу же принимаются за следующее. Часто пользу и выгоду, как общественный и материальный успех, им приносит увлечение забытыми учениями, брошенные предприятия, отслужившие свое методы и т.д. и т.п. Но они должны отказаться от мелочей и деталей, передавая эту работу другим, а сами выступая только по большому счету.',
        9: 'Требует от своего подопечного преданности высокой цели, таланту и призванию, а также щедрой отдачи того, чем одарила его природа. Так как все они пользуются авторитетом, могут быть лидерами, то должны руководствоваться при этом справедливостью, не отступать от тех высоких идей, которые провозглашают. Им не следует мелочиться, прибегать к недостойным действиям или к несвойственному им поведению, чтобы не потерять ни преданности, ни уважения, которые они завоевали. Для себя они не должны требовать больше, чем им причитается, и не требовать от других то, на что они не способны. Они должны усмирять себя, отказаться от излишней гордости и эгоизма, самомнения и высокомерия. И признавать достоинство и права других людей.',
        11: 'Придает решительность, силу и жизненность здравому смыслу, обстоятельность, что помогает человеку подняться поистине до вдохновенных высот. Но затем опять все может измениться, чрезмерную предосторожность или самодовольство числа 2 снова нарушит активность числа 11 и все начнется сначала.',
        22: 'Может рождать сильные колебания между эксцентричностью и гениальностью. Обладая талантом изобретателя или исследователя, данный человек будет обращаться и к сфере тайного, неизведанного, к еще неисследованному и необъясненному.',
    }
    try:
        num_name = name_to_num(name, familyname, fathername)
        explanation = num_explanation[num_name]
        data = {'familyname': familyname,
                'name': name,
                'fathername': fathername,
                'name_number': num_name,
                'explanation': explanation
                }
    except:
        data = JSONResponse(content={"detail": "Not found"}, status_code=404)
    return data


def get_omens_by_letter(letter):
    try:
        response = requests.get(f'https://horoscopes.rambler.ru/api/front/v3/omens/letter/{letter}/').json()
        data = response['content']['inner_blocks'][0]['list_bubbles']['tabs'][0]['list']
        res_data = []
        for elem in data:
            res_data.append({'name': elem['name'],
                             'link': elem['link'].replace('/primety/word/',
                                                          'https://atoma-horoscope.onrender.com/omens_by_word/'),
                             'sign': elem['sign']})
    except:
        res_data = JSONResponse(content={"detail": "Not found"}, status_code=404)
    return res_data


def get_omens_by_word(word):
    try:
        response = requests.get(f'https://horoscopes.rambler.ru/api/front/v3/omens/word/{word}/').json()
        data = response['content']['inner_blocks'][0]['omens_list']['omens']
    except:
        data = JSONResponse(content={"detail": "Not found"}, status_code=404)
    return data
