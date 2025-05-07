import os
import json

def create_sample_bible_data():
    """
    Cria um arquivo JSON com dados de exemplo para a Bíblia Hebraica.
    """
    data = {
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
                            },
                            {
                                "id": 3,
                                "verse_number": 3,
                                "text_hebrew": "וַיֹּ֥אמֶר אֱלֹהִ֖ים יְהִ֣י א֑וֹר וַֽיְהִי־אֽוֹר׃",
                                "text_transliterated": "Vayomer Elohim yehi or vayehi or.",
                                "text_portuguese": "E disse Deus: Haja luz. E houve luz."
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "chapter_number": 2,
                        "verses": [
                            {
                                "id": 4,
                                "verse_number": 1,
                                "text_hebrew": "וַיְכֻלּ֛וּ הַשָּׁמַ֥יִם וְהָאָ֖רֶץ וְכָל־צְבָאָֽם׃",
                                "text_transliterated": "Vayechulu hashamayim veha'aretz vechol tzeva'am.",
                                "text_portuguese": "Assim foram concluídos os céus e a terra, e todo o seu exército."
                            },
                            {
                                "id": 5,
                                "verse_number": 2,
                                "text_hebrew": "וַיְכַ֤ל אֱלֹהִים֙ בַּיּ֣וֹם הַשְּׁבִיעִ֔י מְלַאכְתּ֖וֹ אֲשֶׁ֣ר עָשָׂ֑ה וַיִּשְׁבֹּת֙ בַּיּ֣וֹם הַשְּׁבִיעִ֔י מִכָּל־מְלַאכְתּ֖וֹ אֲשֶׁ֥ר עָשָֽׂה׃",
                                "text_transliterated": "Vayechal Elohim bayom hashevi'i melachto asher asah vayishbot bayom hashevi'i mikol melachto asher asah.",
                                "text_portuguese": "E havendo Deus acabado no dia sétimo a sua obra, que tinha feito, descansou no sétimo dia de toda a sua obra, que tinha feito."
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
                        "id": 3,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 6,
                                "verse_number": 1,
                                "text_hebrew": "וְאֵ֗לֶּה שְׁמוֹת֙ בְּנֵ֣י יִשְׂרָאֵ֔ל הַבָּאִ֖ים מִצְרָ֑יְמָה אֵ֣ת יַעֲקֹ֔ב אִ֥ישׁ וּבֵית֖וֹ בָּֽאוּ׃",
                                "text_transliterated": "Ve'eleh shemot beney Yisra'el haba'im Mitzrayma et Ya'akov ish uveyto ba'u.",
                                "text_portuguese": "Estes são os nomes dos filhos de Israel que entraram no Egito com Jacó; cada um entrou com sua família."
                            },
                            {
                                "id": 7,
                                "verse_number": 2,
                                "text_hebrew": "רְאוּבֵ֣ן שִׁמְע֔וֹן לֵוִ֖י וִיהוּדָֽה׃",
                                "text_transliterated": "Reuven Shimon Levi viYehudah.",
                                "text_portuguese": "Rúben, Simeão, Levi e Judá."
                            }
                        ]
                    }
                ]
            },
            {
                "id": 3,
                "name_hebrew": "וַיִּקְרָא",
                "name_portuguese": "Levítico",
                "name_transliterated": "Vayikra",
                "position": 3,
                "testament": "tanakh",
                "chapters": [
                    {
                        "id": 4,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 8,
                                "verse_number": 1,
                                "text_hebrew": "וַיִּקְרָ֖א אֶל־מֹשֶׁ֑ה וַיְדַבֵּ֤ר יְהוָה֙ אֵלָ֔יו מֵאֹ֥הֶל מוֹעֵ֖ד לֵאמֹֽר׃",
                                "text_transliterated": "Vayikra el-Moshe vayedaber Adonai elav me'ohel mo'ed lemor.",
                                "text_portuguese": "E chamou o Senhor a Moisés, e falou com ele da tenda da congregação, dizendo:"
                            }
                        ]
                    }
                ]
            },
            {
                "id": 4,
                "name_hebrew": "בְּמִדְבַּר",
                "name_portuguese": "Números",
                "name_transliterated": "Bamidbar",
                "position": 4,
                "testament": "tanakh",
                "chapters": [
                    {
                        "id": 5,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 9,
                                "verse_number": 1,
                                "text_hebrew": "וַיְדַבֵּ֨ר יְהוָ֧ה אֶל־מֹשֶׁ֛ה בְּמִדְבַּ֥ר סִינַ֖י בְּאֹ֣הֶל מוֹעֵ֑ד בְּאֶחָד֩ לַחֹ֨דֶשׁ הַשֵּׁנִ֜י בַּשָּׁנָ֣ה הַשֵּׁנִ֗ית לְצֵאתָ֛ם מֵאֶ֥רֶץ מִצְרַ֖יִם לֵאמֹֽר׃",
                                "text_transliterated": "Vayedaber Adonai el-Moshe bemidbar Sinai be'ohel mo'ed be'echad lachodesh hasheni bashanah hashenit letzetam me'eretz Mitzrayim lemor.",
                                "text_portuguese": "E falou o Senhor a Moisés no deserto de Sinai, na tenda da congregação, no primeiro dia do segundo mês, no segundo ano da sua saída da terra do Egito, dizendo:"
                            }
                        ]
                    }
                ]
            },
            {
                "id": 5,
                "name_hebrew": "דְּבָרִים",
                "name_portuguese": "Deuteronômio",
                "name_transliterated": "Devarim",
                "position": 5,
                "testament": "tanakh",
                "chapters": [
                    {
                        "id": 6,
                        "chapter_number": 1,
                        "verses": [
                            {
                                "id": 10,
                                "verse_number": 1,
                                "text_hebrew": "אֵ֣לֶּה הַדְּבָרִ֗ים אֲשֶׁ֨ר דִּבֶּ֤ר מֹשֶׁה֙ אֶל־כָּל־יִשְׂרָאֵ֔ל בְּעֵ֖בֶר הַיַּרְדֵּ֑ן בַּמִּדְבָּ֡ר בָּֽעֲרָבָה֩ מ֨וֹל ס֜וּף בֵּֽין־פָּארָ֧ן וּבֵֽין־תֹּ֛פֶל וְלָבָ֥ן וַחֲצֵרֹ֖ת וְדִ֥י זָהָֽב׃",
                                "text_transliterated": "Eleh hadevarim asher diber Moshe el-kol-Yisra'el be'ever haYarden bamidbar ba'aravah mol suf beyn-Paran uveyn-Tofel veLavan vaChatzerot veDi Zahav.",
                                "text_portuguese": "Estas são as palavras que Moisés falou a todo o Israel além do Jordão, no deserto, na planície defronte do Mar Vermelho, entre Parã e Tofel, e Labã, e Hazerote, e Di-Zaabe."
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/static', exist_ok=True)
    
    # Salvar dados em arquivo JSON
    with open(os.path.dirname(os.path.abspath(__file__)) + '/static/bible_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

if __name__ == "__main__":
    create_sample_bible_data()
