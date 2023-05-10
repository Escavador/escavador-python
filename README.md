# O SDK em Python da API do Escavador

## Documentação disponível

- [API V1](https://api.escavador.com/v1/docs/)
- [API V2](https://api.escavador.com/v2/docs/)

## Instalação

O SDK pode ser instalado via `pip` através do comando:
```bash
python -m pip install escavador
```

##  Requisitos

- Python 3.6+

## Como Configurar

No arquivo `.env` na raíz do seu projeto, crie uma variável chamada `ESCAVADOR_API_KEY` e atribua a ela o seu token da API. A linha onde a variável é definida deve ficar parecida com:
```bash
ESCAVADOR_API_KEY="SUA_API_KEY"
```

Alternativamente, utilize a função `config()` durante a execução do seu projeto, antes de utilizar qualquer outro módulo do SDK.
```py
import escavador
escavador.config("SUA_API_KEY")
```

Para obter seu token da API, acesse o [painel de tokens](https://api.escavador.com/tokens)

## Exemplos

### Consultando os processos de uma empresa pelo CNPJ usando a API V2

[Processos de um envolvido pelo seu nome ou documento](https://api.escavador.com/v2/docs/#processos-de-envolvidos-por-nome-ou-cpfcnpj)

```py
from escavador.v2 import Processo

envolvido, processos = Processo.por_cnpj(cnpj="00000000000000")  # Também aceita o formato 00.000.000/0000-00)

print(f"Processos da empresa {envolvido.nome}:")
for processo in processos:
    print(f"{processo.numero_cnj}:")
    print(f"Fonte: {processo.fontes[0].nome}")
    print(f"Data de início: {processo.data_inicio}")
    print(f"Última movimentação: {processo.data_ultima_movimentacao}")
```

### Consultando o processo mais recente de um advogado usando a API V2

[Consultando processos de um advogado usando sua OAB](https://api.escavador.com/v2/docs/#processos-de-um-advogado-por-oab)

```py
from escavador import CriterioOrdenacao, Ordem
from escavador.v2 import Processo

busca = Processo.por_oab(numero=12345,
                         estado="SP",
                         ordena_por=CriterioOrdenacao.INICIO,
                         ordem=Ordem.DESC)

processo = busca.pop()

print(f"{processo.numero_cnj}: {processo.titulo_polo_ativo} X {processo.titulo_polo_passivo}")
```

### Buscando as movimentações de um processo usando a API V2

[Consultando movimentações de um processo](https://api.escavador.com/v2/docs/#movimentaes-de-um-processo)

```py
from escavador.v2 import Processo

resultado = Processo.movimentacoes(numero_cnj="0000000-00.0000.0.00.0000")

while resultado:
    for movimentacao in resultado:
        print(f"{movimentacao.data} - {movimentacao.tipo}:")
        print(f"{movimentacao.conteudo}")
        print()
    resultado = resultado[0].continuar_busca() # Solicita mais movimentações.
```

### Consultando a última movimentação dos processos mais recentes de uma pessoa pelo nome usando a API V2

[Processos de um envolvido pelo seu nome ou documento](https://api.escavador.com/v2/docs/#processos-de-envolvidos-por-nome-ou-cpfcnpj)

```py
from escavador import CriterioOrdenacao, Ordem
from escavador.v2 import Processo

envolvido, processos = Processo.por_nome(nome="Fulano de Tal da Silva",
                                         ordena_por=CriterioOrdenacao.INICIO,
                                         ordem=Ordem.DESC)

for processo in processos:
    print(f"{processo.numero_cnj}:")
    print(f"Fonte: {processo.fontes[0].nome}")
    print(f"Data de início: {processo.data_inicio}")
    movimentacoes = Processo.movimentacoes(numero_cnj=processo.numero_cnj)
    if movimentacoes:
        print(f"Última movimentação: {movimentacoes[0].conteudo}")
```

### Solicitar busca assíncrona de processo usando a API V1
[Buscando informações do processo no sistema do Tribunal](https://api.escavador.com/v1/docs/#pesquisar-processo-no-site-do-tribunal-assncrono) (Assíncrono)
```py
from escavador import Processo

resultado_busca = Processo.informacoes_no_tribunal("0000000-00.0000.0.00.0000")  # Gera uma busca assíncrona

if resultado_busca['resposta']['status'] == 'SUCESSO':
    for instancia in resultado_busca['resposta']['resposta']['instancias']:
        print(instancia['assunto'])

elif resultado_busca['resposta']['status'] == 'PENDENTE':
    # O ID de uma busca assíncrona pode ser usado para consultar seu status 
    # ou identificar a requisição originária ao receber o callback no seu servidor.
    id_async = resultado_busca['resposta']['id']
```

É recomendado que se utilize o callback ao invés de continuamente consultar o resultado. Entretanto, é possível consultar em massa os seus callbacks cadastrados utilizando a classe `Callback`.

O módulo `server` da biblioteca `http` oferece uma interface simples para receber callbacks. Basta definir o recebimento de requests `POST` conformando com [a documentação do conteúdo dos callbacks](https://api.escavador.com/v1/docs/#detalhes-dos-callbacks).

### Consultar manualmente o status de uma busca assíncrona previamente solicitada

Embora não seja recomendado devido à possibilidade de saturação do seu limite de requisições por minuto, é possível consultar periodicamente o status de uma busca assíncrona.

```py
from escavador import BuscaAssincrona
from time import sleep

while True:
    resultado_busca = BuscaAssincrona.por_id(id_async)
    if resultado_busca['resposta']['status'] != 'PENDENTE':
        break
    sleep(15)

if resultado_busca['resposta']['status'] == 'SUCESSO':
    # Os dados consultados estarão disponíveis no campo ['resposta']['resposta']
    pass
elif resultado_busca['resposta']['status'] == 'ERRO':
    print("Algo deu errado, tente novamente mais tarde.")
```

### Criando Monitoramentos na API V1

```py
from escavador import MonitoramentoTribunal, MonitoramentoDiario, TiposMonitoramentosTribunal, TiposMonitoramentosDiario,FrequenciaMonitoramentoTribunal

# Monitoramento nos sisteams dos Tribunais
monitoramento_tribunal = MonitoramentoTribunal.criar(tipo_monitoramento=TiposMonitoramentosTribunal.UNICO,
                                                       valor="0000000-00.0000.0.00.0000",
                                                       tribunal="TJSP",
                                                       frequencia=FrequenciaMonitoramentoTribunal.SEMANAL)

# Monitoramento em Diários Oficiais
monitoramento_diario = MonitoramentoDiario.criar(TiposMonitoramentosDiario.PROCESSO, processo_id=2, origens_ids=[2,4,6])
```

### Consultando os Tribunais e sistemas disponíveis para a API V1

```py
from escavador import Tribunal

tribunais_disponiveis = Tribunal.sistemas_disponiveis()
```

### Módulos Disponíveis e Referência da API

#### V1:
| Módulo                | Link API                                                             |
|-----------------------|----------------------------------------------------------------------|
| Busca                 | https://api.escavador.com/v1/docs/#busca                             |
| Processo              | https://api.escavador.com/v1/docs/#processos                         |
| Callback              | https://api.escavador.com/v1/docs/#callback                          |
| DiarioOficial         | https://api.escavador.com/v1/docs/#dirios-oficiais                   |
| Instituicao           | https://api.escavador.com/v1/docs/#instituies                        |
| Legislacao            | https://api.escavador.com/v1/docs/#legislao                          |
| Jurisprudencia        | https://api.escavador.com/v1/docs/#jurisprudncias                    |
| MonitoramentoDiario   | https://api.escavador.com/v1/docs/#monitoramento-de-dirios-oficiais  |
| MonitoramentoTribunal | https://api.escavador.com/v1/docs/#monitoramento-no-site-do-tribunal |
| Movimentacao          | https://api.escavador.com/v1/docs/#movimentaes                       |
| Pessoa                | https://api.escavador.com/v1/docs/#pessoas                           |
| Tribunal              | https://api.escavador.com/v1/docs/#tribunais                         |
| Saldo                 | https://api.escavador.com/v1/docs/#saldo-da-api                      |


#### V2:

| Módulo                | Link API                                                             |
|-----------------------|----------------------------------------------------------------------|
| v2.Processo           | https://api.escavador.com/v2/docs/#processos                         |
