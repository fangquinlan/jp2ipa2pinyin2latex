import subprocess
import re
import os

def run_jumanpp(sentence):
    """
    运行 jumanpp 形态分析器，获取分析结果。
    """
    # 请根据您的环境设置 jumanpp 可执行文件和模型的路径
    jumanpp_exe = r"E:\jumanpp-2.0.0-rc4\build\src\jumandic\Release\jumanpp_v2.exe"
    model_path = r"E:\jumanpp-2.0.0-rc4\model\jumandic.jppmdl"
    command = [jumanpp_exe, '--model', model_path]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = process.communicate(sentence)
    if stderr:
        print("Error:", stderr)
    return stdout

def parse_jumanpp_output(output):
    """
    解析 jumanpp 的输出，提取每个单词的表层形式和假名读音。
    """
    words = []
    current_word = None
    for line in output.strip().split('\n'):
        if line.strip() == 'EOS':
            break
        if line.startswith('@'):
            # 处理有多个可能解析的情况，默认选择第一个
            continue
        else:
            fields = line.split()
            if len(fields) < 2:
                continue
            surface = fields[0]
            reading = fields[1]
            words.append({'surface': surface, 'reading': reading})
    return words

def kana_to_ipa(kana):
    """
    将假名读音转换为 IPA 表示，遵循特定的音韵规则。
    """
    # 使用您提供的新的 kana_to_ipa_map
    kana_to_ipa_map = {
        # 元音
        'あ': 'ä',  'い': 'i',   'う': 'ɯ̹',  'え': 'e̞',  'お': 'o̞',
        'ア': 'a',  'イ': 'i',   'ウ': 'ɯ̹',  'エ': 'e̞',  'オ': 'o̞',
        
        # 清音辅音行
        'か': 'kä', 'き': 'kʲi', 'く': 'kɯ̹', 'け': 'ke̞', 'こ': 'ko̞',
        'カ': 'kä', 'キ': 'kʲi', 'ク': 'kɯ̹', 'ケ': 'ke̞', 'コ': 'ko̞',
        
        'さ': 'sä', 'し': 'ɕi', 'す': 'sɯ̹̈', 'せ': 'se̞', 'そ': 'so̞',
        'サ': 'sä', 'シ': 'ɕi', 'ス': 'sɯ̹̈', 'セ': 'se̞', 'ソ': 'so̞',
        
        'た': 'tä', 'ち': 't͡ɕʲi̞', 'つ': 't͡sɯ̹̈', 'て': 'te̞', 'と': 'to̞',
        'タ': 'tä', 'チ': 't͡ɕʲi̞', 'ツ': 't͡sɯ̹̈', 'テ': 'te̞', 'ト': 'to̞',
        
        'な': 'nä', 'に': 'nʲi', 'ぬ': 'nɯ̹', 'ね': 'ne̞', 'の': 'no̞',
        'ナ': 'nä', 'ニ': 'nʲi', 'ヌ': 'nɯ̹', 'ネ': 'ne̞', 'ノ': 'no̞',
        
        'は': 'hä', 'ひ': 'çʲi', 'ふ': 'ɸɯ̹̽', 'へ': 'he̞', 'ほ': 'ho̞',
        'ハ': 'hä', 'ヒ': 'çʲi', 'フ': 'ɸɯ̹̽', 'ヘ': 'he̞', 'ホ': 'ho̞',
        
        'ま': 'mä', 'み': 'mʲi',  'む': 'mɯ̹', 'め': 'me̞', 'も': 'mo̞',
        'マ': 'mä', 'ミ': 'mʲi',  'ム': 'mɯ̹', 'メ': 'me̞', 'モ': 'mo̞',
        
        'や': 'jä', 'ゆ': 'jɯ̹', 'よ': 'jo̞', '𛀁': 'je̞',
        'ヤ': 'jä', 'ユ': 'jɯ̹', 'ヨ': 'jo̞',
        
        'ら': 'ɺä', 'り': 'ɺʲi',  'る': 'ɺɯ̹', 'れ': 'ɺe̞', 'ろ': 'ɺo̞',
        'ラ': 'ɺä', 'リ': 'ɺʲi',  'ル': 'ɺɯ̹', 'レ': 'ɺe̞', 'ロ': 'ɺo̞',
        
        'わ': 'β̞ä', 'ゐ': 'i', 'ゑ': 'e̞',  'を': 'o̞',
        'ワ': 'β̞ä', 'ヰ': 'i', 'ヱ': 'e̞',  'ヲ': 'o̞',
        
        'ん': 'ɴ',  'っ': '̚',
        'ン': 'ɴ',  'ッ': '̚',
        
        # 浊音辅音行
        'が': 'ɡä', 'ぎ': 'ɡʲi̞',  'ぐ': 'ɡɯ̹˕', 'げ': 'ɡe̞', 'ご': 'ɡo̜',
        'ガ': 'ɡä', 'ギ': 'ɡʲi̞',  'グ': 'ɡɯ̹˕', 'ゲ': 'ɡe̞', 'ゴ': 'ɡo̜',
        
        'ざ': 'zä', 'じ': 'd͡ʑi̞',  'ず': 'zɯ̹˕', 'ぜ': 'ze̞', 'ぞ': 'zo̜',
        'ザ': 'zä', 'ジ': 'd͡ʑi̞',  'ズ': 'zɯ̹˕', 'ゼ': 'ze̞', 'ゾ': 'zo̜',
        
        'だ': 'dä', 'ぢ': 'd͡ʑi̞',  'づ': 'd͡zɯᵝ', 'で': 'de̞', 'ど': 'do̜',
        'ダ': 'dä', 'ヂ': 'd͡ʑi̞',  'ヅ': 'd͡zɯᵝ', 'デ': 'de̞', 'ド': 'do̜',
        
        'ば': 'bä', 'び': 'bʲi̞',  'ぶ': 'bɯ̹˕', 'べ': 'be̞', 'ぼ': 'bo̜',
        'バ': 'bä', 'ビ': 'bʲi̞',  'ブ': 'bɯ̹˕', 'ベ': 'be̞', 'ボ': 'bo̜',
        
        'ぱ': 'pä', 'ぴ': 'pʲi̞',  'ぷ': 'pɯ̹˕', 'ぺ': 'pe̞', 'ぽ': 'po̜',
        'パ': 'pä', 'ピ': 'pʲi̞',  'プ': 'pɯ̹˕', 'ペ': 'pe̞', 'ポ': 'po̜',
        
        # 拗音
        'きゃ': 'kʲa̠', 'きゅ': 'kʲɨ', 'きょ': 'kʲo̞',
        'ぎゃ': 'ɡʲa̠', 'ぎゅ': 'ɡʲɨ', 'ぎょ': 'ɡʲo̞',
        'しゃ': 'ɕa̠', 'しゅ': 'ɕɯ̹', 'しょ': 'ɕo̞',
        'じゃ': 'd͡ʑa̠', 'じゅ': 'd͡ʑɨ', 'じょ': 'd͡ʑo̞',
        'ちゃ': 't͡ɕa̠', 'ちゅ': 't͡ɕɨ', 'ちょ': 't͡ɕo̞',
        'にゃ': 'ɲ̟a̠', 'にゅ': 'ɲ̟ɨ', 'にょ': 'ɲ̟o̞',
        'ひゃ': 'ça̠', 'ひゅ': 'çɨ', 'ひょ': 'ço̞',
        'みゃ': 'mʲa̠', 'みゅ': 'mʲɨ', 'みょ': 'mʲo̞',
        'りゃ': 'ɾʲa̠', 'りゅ': 'ɾʲɨ', 'りょ': 'ɾʲo̞',
        'びゃ': 'bʲa̠', 'びゅ': 'bʲɨ', 'びょ': 'bʲo̞',
        'ぴゃ': 'pʲa̠', 'ぴゅ': 'pʲɨ', 'ぴょ': 'pʲo̞',
        'ぢゃ': 'd͡ʑa̠', 'ぢゅ': 'd͡ʑɨ', 'ぢょ': 'd͡ʑo̞',
        'づゃ': 'd͡zʲa̠', 'づゅ': 'd͡zʲɨ', 'づょ': 'd͡zʲo̞',
        'キャ': 'kʲa̠', 'キュ': 'kʲɨ', 'キョ': 'kʲo̞',
        'ギャ': 'ɡʲa̠', 'ギュ': 'ɡʲɨ', 'ギョ': 'ɡʲo̞',
        'シャ': 'ɕa̠', 'シュ': 'ɕɨ', 'ショ': 'ɕo̞',
        'ジャ': 'd͡ʑa̠', 'ジュ': 'd͡ʑɨ', 'ジョ': 'd͡ʑo̞',
        'チャ': 't͡ɕa̠', 'チュ': 't͡ɕɨ', 'チョ': 't͡ɕo̞',
        'ニャ': 'ɲ̟a̠', 'ニュ': 'ɲ̟ɨ', 'ニョ': 'ɲ̟o̞',
        'ヒャ': 'ça̠', 'ヒュ': 'çɨ', 'ヒョ': 'ço̞',
        'ミャ': 'mʲa̠', 'ミュ': 'mʲɨ', 'ミョ': 'mʲo̞',
        'リャ': 'ɾʲa̠', 'リュ': 'ɾʲɨ', 'リョ': 'ɾʲo̞',
        'ビャ': 'bʲa̠', 'ビュ': 'bʲɨ', 'ビョ': 'bʲo̞',
        'ピャ': 'pʲa̠', 'ピュ': 'pʲɨ', 'ピョ': 'pʲo̞',
        'ヂャ': 'd͡ʑa̠', 'ヂュ': 'd͡ʑɨ', 'ヂョ': 'd͡ʑo̞',
        'ヅャ': 'd͡zʲa̠', 'ヅュ': 'd͡zʲɨ', 'ヅョ': 'd͡zʲo̞',
        
        # 外来语特殊拗音
        'ファ': 'ɸa̠', 'フィ': 'ɸʲi', 'フェ': 'ɸe̞', 'フォ': 'ɸo̞',
        'ティ': 'tʲi',  'ディ': 'dʲi',  'チェ': 't͡ɕe̞', 'シェ': 'ɕe̞',
        'ジェ': 'd͡ʑe̞', 'ツァ': 't͡sa̠', 'ツィ': 't͡sʲi', 'ツェ': 't͡se̞', 'ツォ': 't͡so̞',
        'ウィ': 'β̞i',  'ウェ': 'β̞e̞',  'ウォ': 'β̞o̞',
        'クァ': 'kᵝa̠', 'グァ': 'ɡᵝa̠',
        'きぇ': 'kʲe̞', 'しぇ': 'ɕe̞', 'ちぇ': 't͡ɕʲe̞',
        'にぇ': 'ɲ̟e̞', 'ひぇ': 'çe̞', 'みぇ': 'mʲe̞', 'りぇ': 'ɾʲe̞',
        'ぎぇ': 'ɡʲe̞', 'じぇ': 'd͡ʑe̞', 'びぇ': 'bʲe̞', 'ぴぇ': 'pʲe̞',
        'ふぁ': 'ɸa̠', 'ふぃ': 'ɸʲi', 'ふぇ': 'ɸe̞', 'ふぉ': 'ɸo̞',
        'てぃ': 'tʲi', 'でぃ': 'dʲi', 'とぅ': 'tɯ̟', 'どぅ': 'dɯ̟',
        'うぃ': 'β̞i', 'うぇ': 'β̞e̞', 'うぉ': 'β̞o̞',
        'ヴァ': 'va̠', 'ヴィ': 'vʲi', 'ヴ': 'vɯ̟ᵝ', 'ヴェ': 've̞', 'ヴォ': 'vo̞',
        'ヴャ': 'vʲa̠', 'ヴュ': 'vʲɨ', 'ヴョ': 'vʲo̞',
        
        # 长音
        'ー': 'ː',
        
        # 小写假名
        'ぁ': 'ä', 'ぃ': 'i', 'ぅ': 'ɯ̹', 'ぇ': 'e̞', 'ぉ': 'o̞',
        'ゃ': 'a̠', 'ゅ': 'ɨ', 'ょ': 'o̞', 'ゎ': 'wa̠',
        'ァ': 'ä', 'ィ': 'i', 'ゥ': 'ɯ̹', 'ェ': 'e̞', 'ォ': 'o̞',
        'ャ': 'a̠', 'ュ': 'ɨ', 'ョ': 'o̞', 'ヮ': 'wa̠',
        'ゕ': 'ka̠', 'ゖ': 'ke̞',
        'ヵ': 'ka̠', 'ヶ': 'ke̞',
    }

    # 为了处理拗音，需要先按长度排序键，以确保多字符的假名优先匹配
    kana_keys = sorted(kana_to_ipa_map.keys(), key=lambda x: -len(x))

    # 处理假名字符串，转换为 IPA
    ipa = ''
    i = 0
    while i < len(kana):
        matched = False
        for kana_char in kana_keys:
            if kana.startswith(kana_char, i):
                ipa += kana_to_ipa_map[kana_char]
                i += len(kana_char)
                matched = True
                break
        if not matched:
            # 未知字符，跳过或处理
            i += 1
    return ipa

def handle_vowel_lengthening(ipa):
    """
    处理元音长音
    """
    # 处理长音符号 'ː'
    # 将元音后接 'ː' 的情况合并为长元音
    ipa = re.sub(r'(ä|i|ɯ̹|e̞|o̞)ː', r'\1ː', ipa)
    return ipa

def apply_phonological_rules(ipa):
    """
    应用音韵规则，处理清音化、鼻音化等。
    """
    ipa = handle_vowel_lengthening(ipa)

    # 1. 处理促音（使用特殊符号 '̚' 表示）
    # 将促音符号 '̚' 替换为后续辅音的促音化
    # 破裂音前为内破音，破擦音前为 [t̚]，摩擦音前辅音延长
    ipa = re.sub(r'̚([ptk])', r'\1̚\1', ipa)  # 内破音加辅音重复
    ipa = re.sub(r'̚([tdz])', r't̚\1', ipa)    # 破擦音前为 [t̚]
    ipa = re.sub(r'̚([sʃɕçhɸ])', lambda m: m.group(1) * 2, ipa)  # 摩擦音前辅音延长

    # 2. 处理拨音 'ɴ' 的同化
    # 双唇音前的 'ɴ' 同化为 [m]
    ipa = re.sub(r'ɴ([pbmβ̞ɸ])', r'm\1', ipa)
    # 齿龈音前的 'ɴ' 同化为 [n]
    ipa = re.sub(r'ɴ([tdnɾszʑɕ])', r'n\1', ipa)
    # 软腭音前的 'ɴ' 同化为 [ŋ]
    ipa = re.sub(r'ɴ([kgɡɣ])', r'ŋ\1', ipa)
    # 鼻音前的元音鼻化
    ipa = re.sub(r'([äiɯ̹e̞o̞])([mnɲŋɴ])', r'\1̃\2', ipa)
    ipa = re.sub(r'([mnɲŋɴ])([äiɯ̹e̞o̞])', r'\1\2̃', ipa)
    # 在元音和半元音前，'ɴ' 使后续元音鼻化
    ipa = re.sub(r'ɴ([jäjɯ̹jo̞äɪ̟e̞o̞])', lambda m: m.group(1) + '̃', ipa)
    # 词尾的 'ɴ' 保持为 [ɴ]
    ipa = re.sub(r'ɴ$', r'ɴ', ipa)

    # 3. 处理元音的清音化（主要针对 [i] 和 [ɯ̹]）
    # 在无声辅音之间或在无声辅音后词尾的 [i] 和 [ɯ̹] 清音化
    ipa = re.sub(r'([ksthpɕçɸ])([iɯ̹])([ksthpɕçɸ])', lambda m: m.group(1) + m.group(2) + '̥' + m.group(3), ipa)
    ipa = re.sub(r'([ksthpɕçɸ])([iɯ̹])$', lambda m: m.group(1) + m.group(2) + '̥', ipa)
    # 增加对 [o̞] 的清化处理（当相邻两个以上的 [o̞] 时）
    ipa = re.sub(r'(o̞)(o̞)+', lambda m: ''.join([c + '̥' for c in m.group(0)]), ipa)

    # 4. 处理浊辅音的弱化
    # 在元音之间的 [ɡ] 弱化为 [ɣ]
    ipa = re.sub(r'([äiɯ̹e̞o̞])ɡ([äiɯ̹e̞o̞])', r'\1ɣ\2', ipa)
    # 在元音之间的 [b] 弱化为 [β]'
    ipa = re.sub(r'([äiɯ̹e̞o̞])b([äiɯ̹e̞o̞])', r'\1β\2', ipa)

    # 5. 处理辅音的颚化
    # 在 [i] 或 [j] 前的辅音强颚化，加上 ʲ
    ipa = re.sub(r'([tdn])([iɪ̟j])', lambda m: m.group(1) + 'ʲ' + m.group(2), ipa)
    ipa = re.sub(r'([sz])([iɪ̟j])', lambda m: 'ɕ' + m.group(2), ipa)  # s, z 在 i 前变为 ɕ

    # 6. 处理 /t/, /d/ 的破擦音化
    # /t/ 在 /i/ 前变为 [tɕ]
    ipa = re.sub(r'tʲi', 't͡ɕi', ipa)
    # /d/ 在 /i/ 前变为 [dʑ]
    ipa = re.sub(r'dʲi', 'd͡ʑi', ipa)
    # /t/ 在 /u/ 前变为 [ts]
    ipa = re.sub(r'tɯ̹', 't͡sɯ̹', ipa)
    # /d/ 在 /u/ 前变为 [dz]
    ipa = re.sub(r'dɯ̹', 'd͡zɯ̹', ipa)

    # 7. 处理 /h/ 的音变
    # /h/ 在 /i/ 前变为 [ç]
    ipa = re.sub(r'h([iɪ̟])', r'ç\1', ipa)
    # /h/ 在 /u/ 前变为 [ɸ]
    ipa = re.sub(r'hɯ̹', 'ɸɯ̹', ipa)

    # 8. 处理 /r/ 的变体
    # 在词首和 /N/ 后，/r/ 发为 [d̠ɺ̝̆]
    ipa = re.sub(r'(^|[ɴn])ɾ', r'\1d̠ɺ̝̆', ipa)
    # 其他位置保持 [ɾ]

    # 9. 处理声门塞音的插入
    # 在单词开头和结尾插入 [ʔ]
    # 根据需要，您可以选择是否插入声门塞音
    # 这里我们不插入声门塞音，以避免影响拼音转换
    # 如果需要插入，可以取消以下注释
    # ipa = 'ʔ' + ipa + 'ʔ'

    # 10. 处理 /w/ 的发音
    # /w/ 为 [β̞]，可视情况替换为 [ɰ]
    # 如果需要将 /w/ 表示为 [ɰ]，可取消以下注释
    # ipa = ipa.replace('β̞', 'ɰ')

    return ipa

def ipa_to_pinyin(ipa: str) -> str:
    """
    将 IPA 字符串转换为拼音。
    """
    ipa_to_pinyin_dict = {
        # Consonants
        'p': 'b', 'pʰ': 'p', 'm': 'm', 'f': 'f',
        't': 'd', 'tʰ': 't', 'n': 'n', 'l': 'l',
        'k': 'g', 'kʰ': 'k', 'x': 'h', 'h': 'h', 'ɣ': 'e', 'χ': 'h', 'ʁ': 'ʁ', 'ħ': 'haʰoʰ', 'ʕ': 'haʰo', 'ɦ': 'aʰ',
        'tɕ': 'j', 'tɕʰ': 'q', 'ɕ': 'x', 't͡ɕ': 'j', 't͡ɕʰ': 'q',
        'tʂ': 'zh', 'tʂʰ': 'ch', 'ʂ': 'sh', 'ɻ': 'r', 'ʐ': 'r', 't͡s': 'z', 't͡sʰ': 'c', 'ʈ͡ʂ': 'zh', 'ʈ͡ʂʰ': 'ch',
        'ts': 'z', 'tsʰ': 'c', 's': 's', 'd͡z': 'zi', 'dz': 'zi',
        'ŋ': 'ng', 'ɲ': 'ni', 'ɲ̟': 'ni',
        'ʔ': 'ʔ',
        'ɉ': 'i',
        'w': 'u', 'ɥ': 'ü',
        'j': 'i', 'ç': 'xi', 'd͡ʑ': 'ji', 'dʑ': 'ji',

        # Syllabic Consonants
        'm̩': 'm', 'm̥': 'hm',
        'n̩': 'n', 'ŋ̍': 'ng', 'ŋ̊': 'hng',
        'ɹ̩': 'i', 'ɻ̩': 'ri',

        # Vowels
        'i': 'i', 'u': 'u', 'y': 'ü', 'u˞': 'ur',
        'ai': 'a', 'ä': 'a', 'ɑ': 'ao', 'e̞': 'ie', 'ə': 'en', 'a̠': 'a',
        'o': 'o', 'ɔ': 'ao', 'o̞': 'o', 'o̞˞': 'or',
        'ɤ': 'e', 'ɛ': 'i', 'e': 'ie', 'œ': 'ue', 'o̜': 'o',
        'ɵ': 'ou', 'ʊ': 'ong', 'ʊ̃˞': 'ongr', 'ɤ˞': 'e', 'ɤ̞˞': 'eng', 'ɤ˞˞': 'er',
        'ɚ': 'r', 'ɐ': 'i', 'ɚ̃': 'ngr', 'ʌ̹': 'ao',
         'i̞': 'ie',

        # Diphthongs and Triphthongs
        'ja': 'ia', 'wa': 'ua',
        'jo': 'io', 'wo': 'uo',
        'jɛ': 'ie', 'ɥɛ': 'üe',
        'aɪ': 'ai', 'waɪ': 'uai', 'ai̯': 'ai',
        'eɪ': 'ei', 'weɪ': 'ui', 'ei̯': 'ei',
        'ɑʊ': 'ao', 'jɑʊ': 'iao', 'ɑu̯': 'ao', 'ɑu̯˞': 'aor',
        'oʊ': 'ou', 'joʊ': 'iu', 'ou̯': 'iu', 'ou̯˞': 'our',

        # R-colored vowels and combinations
        'äɚ̯': 'r', 'ä̃ɚ̯̃': 'angr', 'ɐɚ̯': 'yanr',

        'an': 'an', 'jɛn': 'ian', 'wan': 'uan', 'ɥæn': 'üan',
        'ən': 'en', 'in': 'in', 'wən': 'un', 'yn': 'ün',
        'ɑŋ': 'ang', 'jɑŋ': 'iang', 'wɑŋ': 'uang',
        'ɤŋ': 'eng', 'iŋ': 'ing', 'wɤŋ': 'ueng',
        'ʊŋ': 'ong', 'jʊŋ': 'iong',
        'ɚ̃': 'a',

        # Tones
        '˥˥': '55', '˧˥': '35', '˨˩˦': '214', '˨˩˩': '211',
        '˩˦': '14', '˥˩': '51', '˥˧': '53',
        '˨˩': '21', '˧˩': '31', '˦˩': '41', '˩˩': '11', '˨˥': '25',
        '˧': '33', '˩˧': '13', '˨˧': '23', '˨': '22',

        # Neutral Tone
        'k˥': '5', 'k˧': '3', 'k˨': '2', '˥': '55',
    }

    # 按照键的长度从长到短排序，确保最长的匹配优先
    ipa_keys = sorted(ipa_to_pinyin_dict.keys(), key=lambda x: -len(x))

    i = 0
    pinyin = ''
    while i < len(ipa):
        matched = False
        for key in ipa_keys:
            if ipa.startswith(key, i):
                pinyin += ipa_to_pinyin_dict[key]
                i += len(key)
                matched = True
                break
        if not matched:
            # 如果没有匹配到，保留原字符
            pinyin += ipa[i]
            i += 1
    return pinyin

def process_text(text, output_option):
    """
    处理输入的文本，返回转换后的结果。
    """
    result = ''
    # 分割文本，保留空格和标点符号
    tokens = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    for token in tokens:
        # 如果是空格或标点符号，直接保留
        if re.match(r'\s', token) or re.match(r'[^\w]', token):
            result += token
        else:
            # 使用 jumanpp 对单词进行解析
            jumanpp_output = run_jumanpp(token)
            words = parse_jumanpp_output(jumanpp_output)
            for word in words:
                surface = word['surface']
                reading = word['reading']
                # 处理助词的特殊读音
                if surface == 'は' and reading == 'は':
                    reading = 'わ'
                elif surface == 'へ' and reading == 'へ':
                    reading = 'え'
                elif surface == 'を' and reading == 'を':
                    reading = 'お'
                ipa = kana_to_ipa(reading)
                ipa = apply_phonological_rules(ipa)
                if output_option == '1':
                    result += f"\\anno{{{surface}}}{{{ipa}}}"
                elif output_option == '2':
                    pinyin = ipa_to_pinyin(ipa)
                    result += f"\\anno{{{surface}}}{{{pinyin}}}"
                else:
                    result += f"\\anno{{{surface}}}{{{ipa}}}"
    return result

def main():
    # 添加模式选择
    mode = input("请选择模式（1: 交互模式，2: 文件模式）：")
    if mode == '1':
        sentence = input("请输入日语句子：")
        output_option = input("请选择输出类型（1: IPA，2: 拼音）：")
        result = process_text(sentence, output_option)
        print(result.strip())
    elif mode == '2':
        # 文件模式
        if not os.path.exists('input.txt'):
            print("未找到 input.txt 文件。")
            return
        with open('input.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        output_option = input("请选择输出类型（1: IPA，2: 拼音）：")
        # 处理文本中的换行符，替换为 '\\'
        text = text.replace('\n', '\\\\')
        result = process_text(text, output_option)
        # 将结果写入 output.txt
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(result)
        print("转换完成，结果已写入 output.txt。")
    else:
        print("无效的模式选择。")

if __name__ == "__main__":
    main()