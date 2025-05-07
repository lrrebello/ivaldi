import json
import os
import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def load_bible_data():
    """
    Carrega os dados da Bíblia Hebraica.
    Tenta primeiro usar a API Scripture, se configurada.
    Se não for possível, usa dados locais.
    """
    # Verificar se a API Scripture está configurada
    scripture_api_key = os.getenv('SCRIPTURE_API_KEY')
    
    if scripture_api_key:
        try:
            # Tentar carregar dados da API Scripture
            return get_data_from_scripture_api()
        except Exception as e:
            logger.error(f"Erro ao carregar dados da API Scripture: {e}")
            logger.info("Usando dados locais como fallback")
    
    # Fallback para dados locais
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'static', 'bible_data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar dados locais da Bíblia: {e}")
    
    # Retornar dados de exemplo se tudo falhar
    return get_sample_bible_data()

def get_data_from_scripture_api():
    """
    Obtém dados da API Scripture.
    Requer a chave da API configurada no arquivo .env.
    """
    scripture_api_key = os.getenv('SCRIPTURE_API_KEY')
    
    if not scripture_api_key:
        raise ValueError("Chave da API Scripture não configurada")
    
    # Configuração da API
    api_url = "https://api.scripture.api.bible/v1"
    headers = {
        "api-key": scripture_api_key,
        "Content-Type": "application/json"
    }
    
    # Obter a lista de bíblias disponíveis
    response = requests.get(f"{api_url}/bibles", headers=headers)
    response.raise_for_status()
    bibles_data = response.json()
    
    # Encontrar a Bíblia Hebraica (pode ser necessário ajustar o filtro)
    hebrew_bible = None
    for bible in bibles_data.get('data', []):
        if 'Hebrew' in bible.get('name', '') or 'hebrew' in bible.get('language', {}).get('name', '').lower():
            hebrew_bible = bible
            break
    
    if not hebrew_bible:
        raise ValueError("Bíblia Hebraica não encontrada na API")
    
    bible_id = hebrew_bible['id']
    
    # Obter os livros da Bíblia
    response = requests.get(f"{api_url}/bibles/{bible_id}/books", headers=headers)
    response.raise_for_status()
    books_data = response.json()
    
    # Formatar os dados para o formato esperado pelo aplicativo
    formatted_data = {"books": []}
    
    for i, book in enumerate(books_data.get('data', []), 1):
        book_data = {
            "id": i,
            "name_hebrew": book.get('name', ''),  # A API pode não fornecer o nome em hebraico
            "name_portuguese": book.get('name', ''),  # A API pode não fornecer o nome em português
            "name_transliterated": book.get('abbreviation', ''),
            "position": i,
            "testament": "tanakh",  # Assumindo que todos são do Tanakh
            "chapters": []
        }
        
        # Obter os capítulos do livro
        book_id = book['id']
        response = requests.get(f"{api_url}/bibles/{bible_id}/books/{book_id}/chapters", headers=headers)
        response.raise_for_status()
        chapters_data = response.json()
        
        for j, chapter in enumerate(chapters_data.get('data', []), 1):
            if chapter['id'] == 'intro':  # Pular introduções
                continue
                
            chapter_data = {
                "id": j,
                "chapter_number": j,
                "verses": []
            }
            
            # Obter os versículos do capítulo
            chapter_id = chapter['id']
            response = requests.get(f"{api_url}/bibles/{bible_id}/chapters/{chapter_id}/verses", headers=headers)
            response.raise_for_status()
            verses_data = response.json()
            
            for k, verse in enumerate(verses_data.get('data', []), 1):
                verse_data = {
                    "id": k,
                    "verse_number": k,
                    "text_hebrew": verse.get('content', ''),  # A API pode fornecer apenas o texto original
                    "text_transliterated": "",  # A API pode não fornecer transliteração
                    "text_portuguese": ""  # A API pode não fornecer tradução
                }
                
                chapter_data["verses"].append(verse_data)
            
            book_data["chapters"].append(chapter_data)
        
        formatted_data["books"].append(book_data)
    
    return formatted_data

def get_sample_bible_data():
    """
    Retorna dados de exemplo para a Bíblia Hebraica.
    """
    return {
        "books": [
            {
                "id": 1,
                "name_hebrew": "בְּרֵאשִׁית",
                "name_portuguese": "Gênesis",
                "name_transliterated": "Bereshit",
                "position": 1,
                "testament": "tanakh",
                "chapters": [
                    {
                        "id": 1,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 1,
                                "verse_number": 1,
                                "text_hebrew": "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃",
                                "text_transliterated": "Bereshit bara Elohim et hashamayim ve'et ha'aretz.",
                                "text_portuguese": "No princípio, Deus criou os céus e a terra."
                            },
                            {
                                "id": 2,
                                "verse_number": 2,
                                "text_hebrew": "וְהָאָ֗רֶץ הָיְתָ֥ה תֹ֙הוּ֙ וָבֹ֔הוּ וְחֹ֖שֶׁךְ עַל־פְּנֵ֣י תְה֑וֹם וְר֣וּחַ אֱלֹהִ֔ים מְרַחֶ֖פֶת עַל־פְּנֵ֥י הַמָּֽיִם׃",
                                "text_transliterated": "Veha'aretz hayeta tohu vavohu vechoshech al-peney tehom veruach Elohim merachefet al-peney hamayim.",
                                "text_portuguese": "A terra era sem forma e vazia, e havia trevas sobre a face do abismo, e o Espírito de Deus pairava sobre a face das águas."
                            }
                        ]
                    }
                ]
            },
            {
                "id": 2,
                "name_hebrew": "שְׁמוֹת",
                "name_portuguese": "Êxodo",
                "name_transliterated": "Shemot",
                "position": 2,
                "testament": "tanakh",
                "chapters": [
                    {
                        "id": 2,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 3,
                                "verse_number": 1,
                                "text_hebrew": "וְאֵ֗לֶּה שְׁמוֹת֙ בְּנֵ֣י יִשְׂרָאֵ֔ל הַבָּאִ֖ים מִצְרָ֑יְמָה אֵ֣ת יַעֲקֹ֔ב אִ֥ישׁ וּבֵית֖וֹ בָּֽאוּ׃",
                                "text_transliterated": "Ve'eleh shemot beney Yisra'el haba'im Mitzrayma et Ya'akov ish uveyto ba'u.",
                                "text_portuguese": "Estes são os nomes dos filhos de Israel que entraram no Egito com Jacó; cada um entrou com sua família."
                            }
                        ]
                    }
                ]
            }
        ]
    }

def search_bible(query, testament=None):
    """
    Pesquisa na Bíblia Hebraica por uma palavra ou frase.
    
    Args:
        query (str): Termo de pesquisa
        testament (str, optional): Filtrar por testamento ('tanakh' ou 'brit_hadasha')
        
    Returns:
        list: Lista de resultados encontrados
    """
    results = []
    bible_data = load_bible_data()
    
    query = query.lower()
    
    for book in bible_data["books"]:
        if testament and book["testament"] != testament:
            continue
            
        for chapter in book["chapters"]:
            for verse in chapter["verses"]:
                # Pesquisar em todos os campos de texto
                if (query in verse["text_hebrew"].lower() or
                    query in verse["text_transliterated"].lower() or
                    query in verse["text_portuguese"].lower()):
                    
                    results.append({
                        "book": book["name_portuguese"],
                        "book_hebrew": book["name_hebrew"],
                        "chapter": chapter["chapter_number"],
                        "verse": verse["verse_number"],
                        "text_hebrew": verse["text_hebrew"],
                        "text_transliterated": verse["text_transliterated"],
                        "text_portuguese": verse["text_portuguese"]
                    })
    
    return results

def get_book_by_id(book_id):
    """
    Obtém um livro da Bíblia pelo ID.
    
    Args:
        book_id (int): ID do livro
        
    Returns:
        dict: Dados do livro ou None se não encontrado
    """
    bible_data = load_bible_data()
    
    for book in bible_data["books"]:
        if book["id"] == book_id:
            return book
    
    return None

def get_chapter(book_id, chapter_number):
    """
    Obtém um capítulo específico de um livro.
    
    Args:
        book_id (int): ID do livro
        chapter_number (int): Número do capítulo
        
    Returns:
        dict: Dados do capítulo ou None se não encontrado
    """
    book = get_book_by_id(book_id)
    
    if book:
        for chapter in book["chapters"]:
            if chapter["chapter_number"] == chapter_number:
                return chapter
    
    return None

def get_verse(book_id, chapter_number, verse_number):
    """
    Obtém um versículo específico.
    
    Args:
        book_id (int): ID do livro
        chapter_number (int): Número do capítulo
        verse_number (int): Número do versículo
        
    Returns:
        dict: Dados do versículo ou None se não encontrado
    """
    chapter = get_chapter(book_id, chapter_number)
    
    if chapter:
        for verse in chapter["verses"]:
            if verse["verse_number"] == verse_number:
                return verse
    
    return None

def get_all_books():
    """
    Obtém todos os livros da Bíblia.
    
    Returns:
        list: Lista de livros
    """
    bible_data = load_bible_data()
    return bible_data["books"]

def get_books_by_testament(testament):
    """
    Obtém livros de um testamento específico.
    
    Args:
        testament (str): 'tanakh' ou 'brit_hadasha'
        
    Returns:
        list: Lista de livros do testamento especificado
    """
    bible_data = load_bible_data()
    return [book for book in bible_data["books"] if book["testament"] == testament]
