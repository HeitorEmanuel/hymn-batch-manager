# Hymn Batch Manager

Aplicação desktop local para Windows que transforma listas de hinos em repertórios organizados. A versão 0.1 entrega a fundação do MVP: criação, limpeza, normalização, remoção assistida de duplicados, persistência SQLite e reabertura de repertórios em uma interface PySide6 clara ou escura.

> Esta ferramenta foi desenvolvida para organizar e processar arquivos locais,
> conteúdos em domínio público e mídias disponibilizadas oficialmente para
> download. O usuário é responsável por garantir que possui autorização para
> baixar, copiar, converter e utilizar cada arquivo.

Ela não é um “baixador universal”, não contorna DRM, autenticação, paywalls ou limitações de plataformas.

## Download para Windows

Baixe a versão portátil na página de [releases do GitHub](https://github.com/HeitorEmanuel/hymn-batch-manager/releases/latest). Extraia o ZIP inteiro e execute `HymnBatchManager.exe` — não mova somente o `.exe`, pois a pasta `_internal` faz parte do aplicativo.

## Versão web

A versão web pode ser usada em [hymn-batch-manager.heitoremanuelamorim.chatgpt.site](https://hymn-batch-manager.heitoremanuelamorim.chatgpt.site). Ela organiza, deduplica, reordena, salva localmente e exporta repertórios sem enviar a lista para um servidor. O código está no repositório [hymn-batch-manager-web](https://github.com/HeitorEmanuel/hymn-batch-manager-web).

## Funcionalidades atuais

- Janela principal em português do Brasil, navegação lateral e temas claro/escuro.
- Criação de repertório com destino, data, evento, igreja, tipo, formato e qualidade.
- Entrada por linha, vírgula ou ponto e vírgula; importação de TXT/CSV.
- Remoção de numeração e marcadores, normalização Unicode e detecção de duplicados.
- Revisão dos duplicados antes da remoção e tabela editável dos itens.
- SQLite local, SQLAlchemy 2, migração Alembic e lista de repertórios recentes.
- Logs rotativos sem telemetria em `data/logs/` no modo de desenvolvimento.
- Atalhos `Ctrl+N` e `Ctrl+S` e estrutura pronta para as próximas fases.

Biblioteca, indexação, pesquisa aproximada, player, fila, FFmpeg, ZIP e relatórios estão planejados nas próximas etapas do MVP; veja [ROADMAP.md](ROADMAP.md).

## Requisitos

- Windows 10 ou 11.
- Python 3.12 ou superior.
- FFmpeg será necessário nas fases de análise e conversão, mas ainda não é necessário nesta versão.

## Instalação e execução no PowerShell

```powershell
git clone URL_DO_REPOSITORIO
cd hymn-batch-manager
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
$env:HBM_DEVELOPMENT = "1"
python -m app.main
```

Sem `HBM_DEVELOPMENT=1`, os dados ficam em `%LOCALAPPDATA%\HymnBatchManager`. Para escolher outro local, defina `HBM_DATA_DIR`.

## Testes e qualidade

```powershell
pytest
ruff check .
ruff format --check .
```

Os testes não dependem de internet e usam bancos temporários isolados.

## Migrações

Na inicialização, a aplicação executa `alembic upgrade head`. Para criar uma futura migração durante o desenvolvimento:

```powershell
alembic revision --autogenerate -m "descricao"
alembic upgrade head
```

## Build para Windows

```powershell
pip install -e ".[build]"
.\scripts\build.ps1
```

O executável será gerado em `dist\HymnBatchManager`. O FFmpeg não é incluído.

O build usa o modo `onedir`: distribua a pasta inteira ou o ZIP gerado, pois a pasta
`_internal` contém as bibliotecas do Qt e do Python necessárias ao executável. Para usar
uma release portátil, extraia o ZIP e execute `HymnBatchManager.exe`.

## Arquitetura

```text
app/
├── domain/       regras e enums sem dependência da interface
├── database/     modelos, sessões e repositórios SQLAlchemy
├── services/     casos de uso da aplicação
├── ui/           janelas, páginas e temas PySide6
└── utils/        normalização e utilitários puros
migrations/       histórico Alembic
tests/            testes unitários, de integração e UI
```

Decisões, modelo de dados, riscos e recorte do MVP estão em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Privacidade e segurança

A aplicação funciona sem conta, não possui telemetria e não envia repertórios. A internet será usada no futuro somente após ação explícita em provedores autorizados. Links diretos deverão bloquear redes privadas, validar redirecionamentos, MIME, tamanho e protocolo antes de qualquer gravação. Consulte [SECURITY.md](SECURITY.md).

## Limitações da versão 0.1

- Repertórios abertos são apresentados para consulta; edição persistente entra na próxima fatia.
- Apenas TXT/CSV UTF-8 é importado; JSON e arrastar/soltar virão depois.
- As páginas futuras aparecem desabilitadas para deixar claro o escopo disponível.
- Nenhuma fonte externa ou download foi implementado.

## Licença

Código sob licença MIT. Direitos sobre hinos, gravações, vídeos, capas e metadados continuam pertencendo aos respectivos titulares.
