from src.tools.category import CategoryTool

def test_categorize_known_keywords():
    assert CategoryTool.categorize("Supermercado Carrefour") == "Alimentação"
    assert CategoryTool.categorize("Conta de Luz da Enel") == "Moradia"
    assert CategoryTool.categorize("Corrida de Uber") == "Transporte"
    assert CategoryTool.categorize("Farmácia Raia") == "Saúde"

def test_categorize_unknown_keyword():
    assert CategoryTool.categorize("Compra misteriosa") == "Outros"
