# Mapeamento de consoantes e vogais hebraicas
HEBREW_MAPPINGS = {
    'consoantes': [
        {'hebraico': 'א', 'transliteracao': ['nada'], 'nome': 'Aleph'},
        {'hebraico': 'בּ', 'transliteracao': ['b'], 'nome': 'Bet com dagesh'},
        {'hebraico': 'ב', 'transliteracao': ['v'], 'nome': 'Vet'},
        {'hebraico': 'גּ', 'transliteracao': ['g'], 'nome': 'Gimel com dagesh'},
        {'hebraico': 'ג', 'transliteracao': ['g (leve)'], 'nome': 'Gimel'},
        {'hebraico': 'דּ', 'transliteracao': ['d'], 'nome': 'Dalet com dagesh'},
        {'hebraico': 'ד', 'transliteracao': ['d (leve)'], 'nome': 'Dalet'},
        {'hebraico': 'ה', 'transliteracao': ['h'], 'nome': 'He'},
        {'hebraico': 'ו', 'transliteracao': ['v', 'w'], 'nome': 'Vav'},
        {'hebraico': 'וּ', 'transliteracao': ['u'], 'nome': 'Vav com dagesh'},
        {'hebraico': 'וֹ', 'transliteracao': ['o'], 'nome': 'Vav com Holam'},
        {'hebraico': 'ז', 'transliteracao': ['z'], 'nome': 'Zayin'},
        {'hebraico': 'ח', 'transliteracao': ['ch', 'rrr'], 'nome': 'Het'},
        {'hebraico': 'ט', 'transliteracao': ['t'], 'nome': 'Tet'},
        {'hebraico': 'י', 'transliteracao': ['y'], 'nome': 'Yod'},
        {'hebraico': 'כּ', 'transliteracao': ['k'], 'nome': 'Kaf com dagesh'},
        {'hebraico': 'כ', 'transliteracao': ['kh', 'rrr'], 'nome': 'Khaf'},
        {'hebraico': 'ך', 'transliteracao': ['ch final'], 'nome': 'Khaf sofit'},
        {'hebraico': 'ל', 'transliteracao': ['l'], 'nome': 'Lamed'},
        {'hebraico': 'מ', 'transliteracao': ['m', 'm normal'], 'nome': 'Mem'},
        {'hebraico': 'ם', 'transliteracao': ['m final'], 'nome': 'Mem sofit'},
        {'hebraico': 'נ', 'transliteracao': ['n'], 'nome': 'Nun'},
        {'hebraico': 'ן', 'transliteracao': ['n final'], 'nome': 'Nun sofit'},
        {'hebraico': 'ס', 'transliteracao': ['s'], 'nome': 'Samekh'},
        {'hebraico': 'ע', 'transliteracao': ['nada'], 'nome': 'Ayin'},
        {'hebraico': 'פּ', 'transliteracao': ['p'], 'nome': 'Pe com dagesh'},
        {'hebraico': 'פ', 'transliteracao': ['f'], 'nome': 'Fe'},
        {'hebraico': 'ף', 'transliteracao': ['f final'], 'nome': 'Fe sofit'},
        {'hebraico': 'צ', 'transliteracao': ['ts'], 'nome': 'Tsade'},
        {'hebraico': 'ץ', 'transliteracao': ['ts final'], 'nome': 'Tsade sofit'},
        {'hebraico': 'ק', 'transliteracao': ['q'], 'nome': 'Qof'},
        {'hebraico': 'ר', 'transliteracao': ['r'], 'nome': 'Resh'},
        {'hebraico': 'שׁ', 'transliteracao': ['sh'], 'nome': 'Shin'},
        {'hebraico': 'שׂ', 'transliteracao': ['s'], 'nome': 'Sin'},
        {'hebraico': 'תּ', 'transliteracao': ['t'], 'nome': 'Tav com dagesh'},
        {'hebraico': 'ת', 'transliteracao': ['t (leve)'], 'nome': 'Tav'},
    ],
    'vogais': [
        {'hebraico': 'ַ', 'transliteracao': ['a'], 'nome': 'Patach'},
        {'hebraico': 'ָ', 'transliteracao': ['a'], 'nome': 'Kamatz'},
        {'hebraico': 'ֵ', 'transliteracao': ['e'], 'nome': 'Tsere'},
        {'hebraico': 'ֶ', 'transliteracao': ['e'], 'nome': 'Segol'},
        {'hebraico': 'ִ', 'transliteracao': ['i'], 'nome': 'Hirik'},
        {'hebraico': 'ְ', 'transliteracao': ['e (leve)'], 'nome': 'Shva'},
        {'hebraico': 'ֹ', 'transliteracao': ['o'], 'nome': 'Holam'},
        {'hebraico': 'ֻ', 'transliteracao': ['u'], 'nome': 'Kubutz'},
        {'hebraico': 'ֳ', 'transliteracao': ['o (leve)'], 'nome': 'Hataf Kamatz'},
        {'hebraico': 'ֲ', 'transliteracao': ['a (leve)'], 'nome': 'Hataf Patach'},
        {'hebraico': 'ֱ', 'transliteracao': ['e (leve)'], 'nome': 'Hataf Segol'},
    ]
}

# Mapeamento de sílabas hebraicas
HEBREW_SYLLABLES = {
    # Módulo 1
    'הִ': {'transliteracao': ['hi'], 'nome': 'He com Hirik'},
    'נֵּ': {'transliteracao': ['ne'], 'nome': 'Nun com Tsere e Dagesh'},
    'מַ': {'transliteracao': ['ma'], 'nome': 'Mem com Patach'},
    'טּוֹ': {'transliteracao': ['to'], 'nome': 'Tet com Holam e Dagesh'},
    'נָּ': {'transliteracao': ['na'], 'nome': 'Nun com Kamatz e Dagesh'},
    'עִי': {'transliteracao': ['i'], 'nome': 'Ayin com Hirik e Yod'},
    'שֶׁ': {'transliteracao': ['she'], 'nome': 'Shin com Sheva'},
    'בֶ': {'transliteracao': ['ve'], 'nome': 'Vet com Segol'},
    'אַ': {'transliteracao': ['a'], 'nome': 'Aleph com Patach'},
    'חִי': {'transliteracao': ['chi'], 'nome': 'Het com Hirik e Yod'},
    'גַּ': {'transliteracao': ['ga'], 'nome': 'Gimel com Patach e Dagesh'},
    'יָ': {'transliteracao': ['ya'], 'nome': 'Yod com Kamatz'},
    # Módulo 2
    'בְּ': {'transliteracao': ['be'], 'nome': 'Bet com Sheva e Dagesh'},
    'רֵ': {'transliteracao': ['re'], 'nome': 'Resh com Tsere'},
    'שִׁי': {'transliteracao': ['shi'], 'nome': 'Shin com Hirik e Yod'},
    'בָּ': {'transliteracao': ['ba'], 'nome': 'Bet com Kamatz e Dagesh'},
    'רָ': {'transliteracao': ['ra'], 'nome': 'Resh com Kamatz'},
    'לֹ': {'transliteracao': ['lo'], 'nome': 'Lamed com Holam'},
    'הִי': {'transliteracao': ['hi'], 'nome': 'He com Hirik e Yod'},
    'אֵ': {'transliteracao': ['e'], 'nome': 'Aleph com Tsere'},
    'הַ': {'transliteracao': ['ha'], 'nome': 'He com Patach'},
    'שָּׁׁ': {'transliteracao': ['sha'], 'nome': 'Shin com Kamatz e Dagesh'},
    'יִ': {'transliteracao': ['yi'], 'nome': 'Yod com Hirik'},
    'וְ': {'transliteracao': ['ve'], 'nome': 'Vav com Sheva'},
    'עֶ': {'transliteracao': ['e'], 'nome': 'Ayin com Segol'},
    # Módulo 3
    'הוֹ': {'transliteracao': ['ho'], 'nome': 'He com Holam'},
    'דוּ': {'transliteracao': ['du'], 'nome': 'Dalet com Vav e Dagesh'},
    'לַ': {'transliteracao': ['la'], 'nome': 'Lamed com Patach'},
    'יְ': {'transliteracao': ['ye'], 'nome': 'Yod com Sheva'},
    'הוָ': {'transliteracao': ['hwa'], 'nome': 'He com Kamatz'},
    'כִּי': {'transliteracao': ['ki'], 'nome': 'Kaf com Hirik e Yod e Dagesh'},
    'טוֹ': {'transliteracao': ['to'], 'nome': 'Tet com Holam'},
    'לְ': {'transliteracao': ['le'], 'nome': 'Lamed com Sheva'},
    'עוֹ': {'transliteracao': ['o'], 'nome': 'Ayin com Holam'},
    'לָ': {'transliteracao': ['la'], 'nome': 'Lamed com Kamatz'},
    'חַ': {'transliteracao': ['cha'], 'nome': 'Het com Patach'},
    'סְ': {'transliteracao': ['se'], 'nome': 'Samekh com Sheva'},
    'דּוֹ': {'transliteracao': ['do'], 'nome': 'Dalet com Holam e Dagesh'},
    # Módulo 4
    'שָּׁׁ': {'transliteracao': ['sha'], 'nome': 'Shin com Kamatz e Dagesh'},
    'מְ': {'transliteracao': ['me'], 'nome': 'Mem com Sheva'},
    'סַ': {'transliteracao': ['sa'], 'nome': 'Samekh com Patach'},
    'פְּ': {'transliteracao': ['pe'], 'nome': 'Pe com Sheva e Dagesh'},
    'רִי': {'transliteracao': ['ri'], 'nome': 'Resh com Hirik e Yod'},
    'כְּ': {'transliteracao': ['ke'], 'nome': 'Kaf com Sheva e Dagesh'},
    'בוֹ': {'transliteracao': ['bo'], 'nome': 'Bet com Holam'},
    'ד': {'transliteracao': ['d'], 'nome': 'Dalet'},
    'ל': {'transliteracao': ['l'], 'nome': 'Lamed'},
    # Módulo 5
    'לֹ': {'transliteracao': ['lo'], 'nome': 'Lamed com Holam'},
    'יָ': {'transliteracao': ['ya'], 'nome': 'Yod com Kamatz'},
    'נוּ': {'transliteracao': ['nu'], 'nome': 'Nun com Vav e Dagesh'},
    'יִי': {'transliteracao': ['yi'], 'nome': 'Yod com Hirik e Yod'},
    'שָׁׁ': {'transliteracao': ['sha'], 'nome': 'Shin com Kamatz'},
    'שׁוֹ': {'transliteracao': ['sho'], 'nome': 'Shin com Holam'},
    'מֵ': {'transliteracao': ['me'], 'nome': 'Mem com Tsere'},
    'שְׂ': {'transliteracao': ['se'], 'nome': 'Sin com Sheva'},
    'רָ': {'transliteracao': ['ra'], 'nome': 'Resh com Kamatz'},
    'אֵ': {'transliteracao': ['e'], 'nome': 'Aleph com Tsere'}
}

def get_hebrew_mappings():
    """Retorna o mapeamento completo de caracteres hebraicos."""
    return HEBREW_MAPPINGS

def get_consonants():
    """Retorna a lista de consoantes hebraicas."""
    return HEBREW_MAPPINGS['consoantes']

def get_vowels():
    """Retorna a lista de vogais hebraicas."""
    return HEBREW_MAPPINGS['vogais']

def get_character_info(character):
    """Retorna informações sobre um caractere hebraico específico (consoantes, vogais ou sílabas)."""
    # Primeiro, busca em consoantes e vogais
    for category in ['consoantes', 'vogais']:
        for item in HEBREW_MAPPINGS[category]:
            if item['hebraico'] == character:
                return item
    
    # Se não encontrar, busca nas sílabas
    if character in HEBREW_SYLLABLES:
        return HEBREW_SYLLABLES[character]
    
    return None

def parse_module_data(module):
    """Processa os dados de um módulo para uso nas lições."""
    if not module:
        return None
    
    return {
        'id': module.id,
        'module_number': module.module_number,
        'hebrew_text': module.hebrew_text,
        'consonants': module.consonants.split(',') if module.consonants else [],
        'vowels': module.vowels.split(',') if module.vowels else [],
        'syllables': module.syllables.split(',') if module.syllables else [],
        'visible': module.visible
    }

def init_modules_data():
    """Retorna os dados iniciais para os módulos."""
    return [
        {
            'module_number': 1,
            'hebrew_text': 'הִנֵּ֣ה מַה־טּ֭וֹב וּמַה־נָּעִ֑ים שֶׁ֖בֶת אַחִ֣ים גַּם־יָֽחַד',
            'consonants': 'ה,נ,מ,ט,ו,ב,ע,י,שׁ,ת,א,ח,ג,ד',
            'vowels': 'ִ,ֵ,ַ,ָ,ֹ,֑,ֽ',
            'syllables': 'הִ,נֵּ,מַ,טּוֹ,נָּעִי,שֶׁבֶ,אַ,חִי,גַּ,יָ'
        },
        {
            'module_number': 2,
            'hebrew_text': 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ',
            'consonants': 'ב,ר,א,שׁ,י,ת,ל,ה,מ,ו,ע,צ',
            'vowels': 'ְ,ֵ,ִ,֖,ָ,֣,ֹ,֑,֥,ַ,ֽ',
            'syllables': 'בְּ,רֵ,שִׁי,בָּ,רָ,לֹ,הִי,אֵ,הַ,שָּׁׁ,מַ,יִ,וְ,עֶ'
        },
        {
            'module_number': 3,
            'hebrew_text': 'הוֹד֣וּ לַיהוָ֣ה כִּי־ט֑וֹב כִּ֖י לְעוֹלָ֣ם חַסְדּֽוֹ',
            'consonants': 'ה,ו,ד,י,ל,ת,ב,כ,ע,מ,ח,ס',
            'vowels': 'ֹ,֣,ּ,ַ,ָ,֑,֖,ְ,ֽ',
            'syllables': 'הוֹ,דוּ,לַ,יְהוָ,כִּי,טוֹ,ב,לְ,עוֹ,לָ,חַ,סְ,דּוֹ'
        },
        {
            'module_number': 4,
            'hebrew_text': 'הַשָּׁמַ֗יִם מְֽסַפְּרִ֥ים כְּבֽוֹד־אֵ֑ל',
            'consonants': 'ה,שׁ,מ,י,ס,פ,ר,כ,ב,ו,ד,א,ל',
            'vowels': 'ַ,ָ,֗,ִ,֥,ְ,ֽ,ֹ,֑',
            'syllables': 'הַ,שָׁׁ,מַ,יִ,מְ,סַ,פְּ,רִי,כְּ,בוֹ,ד,אֵ,ל'
        },
        {
            'module_number': 5,
            'hebrew_text': 'הִנֵּ֣ה לֹֽא־יָ֭נוּם וְלֹ֣א יִישָׁ֑ן שׁ֝וֹמֵ֗ר יִשְׂרָאֵֽל',
            'consonants': 'ה,נ,ל,א,י,ו,מ,שׁ,שׂ,ר,ע,ב',
            'vowels': 'ִ,ֵ,֣,ֹ,ֽ,ָ,֭,ּ,ִי,֑,֗,ְ,֝',
            'syllables': 'הִ,נֵּ,לֹ,יָ,נוּ,וְ,יִי,שָׁׁ,שׁוֹ,מֵ,שְׂ,רָ,אֵ,ל'
        }
    ]


# ... (código existente do utils.py)

def calculate_progress(user_id):
    """Calcula o aproveitamento total do usuário em porcentagem considerando todos os 5 módulos (15 testes)."""
    from .models import Module, TestResult

    # Total de módulos e testes esperados (fixo: 5 módulos, 3 testes por módulo)
    TOTAL_MODULES = 5
    TESTS_PER_MODULE = 3
    TOTAL_TESTS = TOTAL_MODULES * TESTS_PER_MODULE  # 15 testes no total
    WEIGHT_PER_TEST = 100 / TOTAL_TESTS  # 6,67% por teste

    # Buscar todos os resultados dos testes do usuário
    test_results = TestResult.query.filter_by(user_id=user_id).all()

    if not test_results:
        return 0  # Se não houver resultados, o progresso é 0%

    total_progress = 0

    for result in test_results:
        if result.total_questions == 0:
            continue  # Evitar divisão por zero
        # Calcular o aproveitamento no teste (em porcentagem)
        test_achievement = (result.correct_answers / result.total_questions) * 100
        # Cada teste contribui com WEIGHT_PER_TEST (6,67%) do progresso total
        test_contribution = (test_achievement / 100) * WEIGHT_PER_TEST
        total_progress += test_contribution

    return round(total_progress, 2)  # Arredondar para 2 casas decimais