# Arquitetura e decisões técnicas

## Stack

Python 3.12+ e PySide6 atendem bem ao desktop Windows sem servidor. Qt Multimedia será adicionado junto ao player; instalar WebEngine agora aumentaria muito o pacote sem benefício ao MVP. SQLAlchemy 2 separa persistência do domínio e Alembic mantém o esquema reproduzível. SQLite é suficiente para uma biblioteca local, usando transações curtas e workers nas operações demoradas. RapidFuzz, Mutagen, Pillow, HTTPX e FFmpeg/FFprobe serão usados nas fases que realmente precisarem deles.

## Camadas

1. `ui`: apresentação, coleta de dados e feedback; não contém SQL.
2. `services`: validação e casos de uso; recebe repositórios por construtor.
3. `database`: modelos ORM, sessões transacionais e repositórios.
4. `domain`: estados e regras que não dependem do Qt.
5. `providers` e `workers` serão introduzidos quando biblioteca e processamento começarem, mantendo contratos pequenos e cancelamento cooperativo.

## Modelo do banco

- `Repertoire` agrega os dados e defaults de um repertório.
- `RepertoireItem` preserva nome original e normalizado, ordem, escolha e estado.
- `LibraryFolder` e `LibraryFile` suportam índice incremental e arquivos ausentes.
- `SearchResult` diferencia referência, prévia e URL de download e exige `can_download` explícito.
- `ProcessingJob` persiste fila, tentativas e progresso para recuperação.
- `DownloadRecord` mantém proveniência de transferências autorizadas.
- `AppSetting` guarda configuração local simples.

O esquema usa IDs inteiros, datas com fuso quando suportado, exclusão em cascata apenas para registros dependentes e nunca exclui arquivos físicos.

## Recorte do MVP em etapas

1. Fundação, banco, migrações, logging e shell da interface — entregue na 0.1.
2. Edição completa de repertórios, JSON, drag-and-drop e histórico — próxima etapa.
3. Biblioteca local, indexação incremental, FFprobe e hashes parciais.
4. Busca RapidFuzz, preferências, confiança e confirmação manual.
5. Player local com Qt Multimedia.
6. Fila persistente, cópia, renomeação, cancelamento e recuperação.
7. FFmpeg, presets, extração de áudio e progresso.
8. ZIP, relatórios e histórico completo.
9. Links diretos autorizados com validação SSRF e retomada segura.

## Riscos e mitigação

### Legal

- Reprodução não implica permissão de download: `can_download` começa falso e cada provedor declara capacidades.
- Mudanças de termos/API: provedores são opcionais e isolados; nenhuma extração genérica será criada.
- Direitos autorais: aviso aparece na aplicação e documentação; proveniência e licença serão registradas.

### Segurança

- SSRF e redirecionamento para IP privado: resolver e validar cada destino antes de aceitar links.
- Arquivos maliciosos ou enormes: limites configuráveis, MIME/extensão, escrita temporária e validação antes do destino final.
- Injeção em subprocesso: argumentos em lista, nunca `shell=True`; caminhos e nomes sanitizados.
- Segredos em logs: parâmetros sensíveis de URL e tokens nunca são registrados.

### Técnicos

- UI congelada: indexação, rede, hashes e FFmpeg usarão `QThreadPool` com sinais e cancelamento cooperativo.
- SQLite bloqueado: um `Session` por operação, transações curtas e gravação em lotes.
- Mídia heterogênea: FFprobe é fonte técnica principal e falhas isolam apenas o item.
- Caminhos Windows/OneDrive/rede: `pathlib`, nomes reservados, limites e erros de acesso explícitos.
- Recuperação após encerramento: jobs ativos serão persistidos e reclassificados como interrompidos ao abrir.

