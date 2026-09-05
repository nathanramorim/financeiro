# Frontend — Diretrizes & Qualidade

- **Styling:** Tailwind CSS com classes utilitárias. Utilizar rigorosamente os tokens de cor e tipografia definidos em `.agents/rules/design-system.md` (`--primary`, `--panel`, `--panel-border`, fonte **Montserrat**). Evitar CSS customizado inline ou fora do sistema de design.
- **Tema padrão:** **Light**. Toda interface, componente e gráfico deve ser desenvolvido primariamente no tema light; variações dark (se houverem) são opt-in.
- **Mobile First Obrigatório:** Estilizar primeiro para telas menores (360px a 430px sem prefixo de breakpoint) e usar `sm:`, `md:`, `lg:` apenas para expandir layouts em tablets e desktops. A aplicação de finanças pessoais é consumida prioritariamente em smartphones para consultas rápidas e lançamentos em tempo real.
- **Microinterações e Feedback:** Toda ação assíncrona (chamada de chat, confirmação de transação, carregamento de relatórios) deve fornecer feedback visual imediato (loaders, skeletons ou spinners suaves), mantendo a interface interativa.
- **Validação de Interface:** Ao criar ou alterar componentes visuais, sempre validar o comportamento responsivo tanto em viewports mobile quanto desktop, cobrindo o fluxo principal (golden path) e estados de erro/vazio, além de garantir type-check sem erros (`npm run build` / `tsc`).
