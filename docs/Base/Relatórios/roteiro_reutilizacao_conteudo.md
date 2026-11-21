# Roteiro de apresentação — Reutilização no fórum

**Duração sugerida:** 9 minutos de apresentação e 1 minuto para perguntas. Roteiro para Caio apresentar sua contribuição na SubEquipe 01.

## Antes de começar

Deixe abertas três abas: o [feed](http://127.0.0.1:8501), o [Swagger da API](http://127.0.0.1:8000/docs) e o [Quadro de Participações](../1.2.Participacoes.md). No editor, abra os arquivos indicados nas etapas 3 e 4. Se precisar iniciar o projeto, siga as [instruções de execução](../../../codigo/README.md#feed-e-detalhe-de-conteúdo).

Prepare uma pergunta com a tag `reutilizacao` e uma resposta. No Swagger, use `POST /perguntas` com o primeiro JSON abaixo, copie o `id` retornado e use-o em `POST /perguntas/{pergunta_id}/respostas` com o segundo JSON. Guarde o mesmo ID para publicar o comentário ao vivo. Como os dados ficam em memória, mantenha a API em execução entre o ensaio e a apresentação.

```json
{"titulo":"Por que a resposta aparece no detalhe e não no feed?","corpo":"Perguntas e respostas ficam no mesmo repositório. Como a tela sabe o que exibir?","autor":"Caio","tags":["reutilizacao","python"]}
```

```json
{"corpo":"O feed lista perguntas. No detalhe, cada pergunta traz as respostas e os comentários associados a ela.","autor":"Participante da demonstração"}
```

## 1. Abrir com a pergunta do usuário · 0–1 min

**Na tela**, busque `reutilizacao` no feed e aponte para o título e o contador de respostas.

**Fala sugerida:** “Aqui aparece uma pergunta com uma resposta. O curioso é que a API guarda as duas no mesmo repositório. Por que só a pergunta aparece nessa lista? Vou usar essa conversa para mostrar duas decisões da entrega: como o backend reaproveita a persistência e como o frontend reaproveita a apresentação.”

## 2. Acrescentar um comentário ao vivo · 1–3 min

**Na tela**, abra a pergunta pelo título e mostre a resposta já publicada. No Swagger, execute `POST /perguntas/{pergunta_id}/comentarios` com o ID preparado e o JSON abaixo. Mostre o retorno `201`. Atualize a página de detalhe, localize o novo texto e volte ao feed para mostrar o contador atualizado.

```json
{"corpo":"Acabei de publicar este comentário durante a apresentação.","autor":"Caio"}
```

**Fala sugerida:** “Publiquei pelo Swagger e li o resultado no Streamlit. As duas interfaces conversam com a mesma API. O contador mudou, mas a conversa continua ocupando uma única entrada no feed. Vamos ver onde o código decide isso.”

## 3. Seguir o dado até o repositório · 3–5min30s

**No editor**, comece em `CriadorDeConteudo.publicar()`. Aponte para as chamadas a `criar_conteudo()` e `salvar()`. Em seguida, abra o construtor de `RepositorioConteudo` e termine em `listar_perguntas()`. [Criadores da Entrega 03](../../../codigo/subequipe1_factory_method/criadores.py#L19) · [Repositório de Conteúdo](../../../codigo/subequipe1_factory_method/repositorio.py)

**Fala sugerida:** “Na Entrega 03, já tínhamos o Factory Method. O criador concreto decide qual objeto construir, e a operação de publicar salva o resultado. Na Entrega 04, extraímos duas responsabilidades que estavam juntas. O Singleton cuida de obter a mesma instância por processo. O Repository genérico cuida de salvar, buscar e listar por chave. Conteúdo usa esse componente com UUID como chave e Conteudo como valor.”

**Aponte para** `conteudo.como_pergunta()`. “Aqui está a resposta à pergunta inicial. Cada produto responde à mesma chamada. Pergunta devolve a si própria. Resposta e Comentario herdam o comportamento que devolve None. Assim, o feed recebe somente as perguntas, e o detalhe usa as coleções da pergunta selecionada.” [Produtos do domínio](../../../codigo/subequipe1_factory_method/produtos.py#L15)

**Se perguntarem sobre SOLID:** “A extração separa ciclo de vida e armazenamento, aplicando SRP. As operações de persistência usam o contrato RepositorioBase, e o construtor escolhe a implementação em memória. O polimorfismo permite percorrer todos os produtos pelo contrato de Conteudo.” [Contrato e implementação](../../../codigo/compartilhado/repositorio_memoria.py)

## 4. Mostrar um componente em três contextos · 5min30s–7min30s

**Na tela**, deixe o detalhe da conversa ao lado das chamadas a `CardConteudo` em `app.py`. Aponte para autor, data e corpo nos três cards. Depois, compare as tags da pergunta no detalhe e no feed. [Composição das telas](../../../codigo/frontend_conteudo/app.py) · [Componentes](../../../codigo/frontend_conteudo/componentes.py)

**Fala sugerida:** “No detalhe, estas três chamadas desenham a pergunta, a resposta e o comentário. Todas usam CardConteudo. O que muda são os dados e os parâmetros. A pergunta pede título, tags e status. A resposta pode destacar a marca de aceita quando esse dado vem da API. O comentário usa a apresentação compacta. Se quisermos mudar o formato da data em todo o fórum, temos um único ponto para editar.”

**Volte ao feed.** “Aqui, o mesmo card recebe link_detalhe. O título passa a abrir a conversa e o rodapé mostra as contagens. As tags continuam vindo de ListaTags nas duas telas. Dá para ver o reuso mudando de tela e confirmar no código exatamente qual parâmetro mudou.”

## 5. Mostrar autoria e fechar com uma escolha técnica · 7min30s–9 min

**Na Wiki**, mostre a linha de Caio no Quadro de Participações. No histórico local, destaque `009bd30` (extração dos componentes), `8cee2f1` (primeiro consumidor) e `56953cf` (revisão visual). No relatório, mostre a divisão da dupla entre persistência/exibição e serviço/publicação. [Participações](../1.2.Participacoes.md) · [Relatório](1.1.2.Reutilizacao.md)

**Fala sugerida:** “Minha parte atravessou o backend e o frontend. Um commit introduz o componente genérico e o seguinte mostra o repositório do fórum usando esse componente. Na interface, conseguimos mudar o visual do feed e do detalhe mantendo os contratos de publicação. O armazenamento em memória facilitou a demonstração e tem um limite concreto: reiniciar a API apaga a conversa. O Singleton também vale apenas dentro de um processo.”

**Foco 02 — reserve 20 segundos para seu relato pessoal.** Escolha uma sugestão da IA que você realmente revisou e conte o que decidiu e como verificou. Um episódio documentado nesta entrega é o teste da revisão visual: o navegador revelou que o processo Streamlit ainda carregava a assinatura antiga do card. Após reiniciar o frontend, foram verificados busca, detalhe e retorno ao feed em largura móvel. Use o episódio se ele representar o aprendizado que você quer relatar.

**Frase de encerramento:** “A conversa que criamos passou por um fluxo de publicação compartilhado, ficou disponível pelo mesmo repositório e apareceu em duas telas. A evidência da reutilização está nesses pontos que pudemos acompanhar do clique até o código.”
