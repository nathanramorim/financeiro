class CategoryTool:
    """Ferramenta para categorização de despesas com base em palavras-chave e suporte a fallback."""

    CATEGORIES = {
        "Moradia": ["aluguel", "condomínio", "iptu", "luz", "energia", "água", "gás", "internet"],
        "Alimentação": ["supermercado", "mercado", "feira", "restaurante", "ifood", "padaria", "lanche"],
        "Transporte": ["uber", "combustível", "gasolina", "estacionamento", "pedágio", "ônibus", "metrô"],
        "Saúde": ["farmácia", "remédio", "médico", "consulta", "plano de saúde", "dentista", "academia", "gym", "treino"],
        "Lazer": ["cinema", "viagem", "shows", "streaming", "netflix", "spotify", "jogos"],
        "Educação": ["escola", "faculdade", "curso", "livro", "mensalidade"],
    }

    @classmethod
    def categorize(cls, description: str) -> str:
        if not description:
            return "Outros"

        desc_lower = description.lower()
        for category, keywords in cls.CATEGORIES.items():
            if any(kw in desc_lower for kw in keywords):
                return category

        return "Outros"
