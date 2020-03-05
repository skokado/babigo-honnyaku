from django.shortcuts import render
from django.views import generic
from django.template import loader
from django.http import HttpResponse

from . import forms

def babinize(string: str,
             use_only=None):
    """引数チェック"""
    if use_only and use_only not in ('hira', 'kata'):
        raise SyntaxError('Argument "use_only" must be "hira" or "kata".')
    chars = [c for c in string]

    """モードに応じた変換文字の定義"""
    babi_char = {'a_hira': 'ば', 'a_kata': 'バ',
                 'i_hira': 'び', 'i_kata': 'ビ',
                 'u_hira': 'ぶ', 'u_kata': 'ブ',
                 'e_hira': 'べ', 'e_kata': 'ベ',
                 'o_hira': 'ぼ', 'o_kata': 'ボ'}
    if use_only == 'hira':
        babi_char['a_kata'] = 'ば'
        babi_char['i_kata'] = 'び'
        babi_char['u_kata'] = 'ぶ'
        babi_char['e_kata'] = 'べ'
        babi_char['o_kata'] = 'ぼ'
    elif use_only == 'kata':
        babi_char['a_hira'] = 'バ'
        babi_char['i_hira'] = 'ビ'
        babi_char['u_hira'] = 'ブ'
        babi_char['e_hira'] = 'ベ'
        babi_char['o_hira'] = 'ボ'

    """次の文字が拗音の場合はバビ語化をスキップする必要がある
    ※拗音(ようおん)：「ゃ」や「ょ」など
    """
    relentless_sounds = 'ぁぃぅぇぉゃゅょ' + 'ァィゥェォャュョ'

    """はじめに「ば行」を置換"""
    trans_table_babibubebo = {}
    trans_table_babibubebo['ば'] = 'ば' + babi_char['a_hira']
    trans_table_babibubebo['び'] = 'び' + babi_char['i_hira']
    trans_table_babibubebo['ぶ'] = 'ぶ' + babi_char['u_hira']
    trans_table_babibubebo['べ'] = 'ぼ' + babi_char['e_hira']
    trans_table_babibubebo['ぼ'] = 'ぼ' + babi_char['o_hira']
    
    trans_table_babibubebo['バ'] = 'バ' + babi_char['a_kata']
    trans_table_babibubebo['ビ'] = 'ビ' + babi_char['i_kata']
    trans_table_babibubebo['ブ'] = 'ブ' + babi_char['u_kata']
    trans_table_babibubebo['ベ'] = 'ベ' + babi_char['e_kata']
    trans_table_babibubebo['ボ'] = 'ボ' + babi_char['o_kata']

    for i, c in enumerate(chars):
        if i < len(chars) - 1:
            if chars[i + 1] in relentless_sounds:
                continue
        chars[i] = c.translate(str.maketrans(trans_table_babibubebo))

        
    """母音ごとの変換表を作成
    「ば行」はスキップする
    """
    trans_table = {}
    for c in 'あかさたなはまやらわ' + 'がざだぱ' + 'ぁゃ':
        trans_table[c] = c + babi_char['a_hira']
    for c in 'アカサタナハマヤラワ' + 'ガザダパ' + 'ァャ':
        trans_table[c] = c + babi_char['a_kata']

    for c in 'いきしちにひみり' + 'ぎじぢぴ' + 'ぃ':
        trans_table[c] = c + babi_char['i_hira']
    for c in 'イキシチニヒミリ' + 'ギジヂピ' + 'ィ':
        trans_table[c] = c + babi_char['i_kata']

    for c in 'うくすつぬふむゆるん' + 'ぐずづぷ' + 'ぅゅ':
        trans_table[c] = c + babi_char['u_hira']
    for c in 'ウクスツヌフムユルン' + 'グズヅプ' + 'ゥュ':
        trans_table[c] = c + babi_char['u_kata']

    for c in 'えけせてねへめれ' + 'げぜでぺ' + 'ぇ':
        trans_table[c] = c + babi_char['e_hira']
    for c in 'エケセテネヘメレ' + 'ゲゼデペ' + 'ェ':
        trans_table[c] = c + babi_char['e_kata']

    for c in 'おこそとのほもよろを' + 'ごぞどぽ' + 'ぉょ':
        trans_table[c] = c + babi_char['o_hira']
    for c in 'オコソトノホモヨロヲ' + 'ゴゾドポ' + 'ォョ':
        trans_table[c] = c + babi_char['o_kata']

    for i, c in enumerate(chars):
        if i < len(chars) - 1:
            if chars[i + 1] in relentless_sounds:
                continue
        chars[i] = c.translate(str.maketrans(trans_table))
    return ''.join(chars)


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
    def post(self, request, *args, **kwargs):
        before_text = request.POST['before-text']
        use_only = request.POST['useonly']
        if use_only == '':
            use_only = None
        after_text = babinize(before_text, use_only=use_only)
        context = {'before_text': before_text,
                   'useonly': use_only,
                   'after_text': after_text}
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
