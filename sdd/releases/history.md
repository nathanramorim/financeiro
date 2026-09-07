# Release Notes — financeiro

Este arquivo registra o histórico de entregas de produto deste projeto.

## Entregas

- **Feat 2320**: O Dashboard (saldo, gráficos e despesas fixas) agora aparece tudo junto em uma única tela, sem precisar trocar de aba, e o Assistente ganhou seu próprio espaço, acessível por uma barra de navegação fixa na parte de baixo da tela — pensado para uso no celular.
- **Fix 5362**: Corrigimos uma falha em que apagar todos os lançamentos na planilha, seguida de uma instabilidade temporária de conexão, podia fazer despesas ou receitas já removidas voltarem a aparecer nos relatórios.
- **Feat c094**: Reorganizamos as pastas do projeto para deixar mais claro o que é o backend e o que é o frontend — sem nenhuma mudança visível para quem usa o sistema.
- **Fix 5a01**: Agora o agente reconhece mensagens de inclusão/cadastro de despesas no modo de contingência local, extraindo valor e descrição e registrando a nova despesa corretamente.
