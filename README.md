
## SDK em python para utilizar a API do Escavador

### Como Configurar

- Crie no `.env` do seu projeto uma variável `ESCAVADOR_API_KEY` com seu token da API
- ou
- utilize a função `config()`
```py
import escavador
escavador.config("API_KEY")
```
- para obter seu token da API, acesse o [painel de tokens](https://api.escavador.com/tokens)

### Como Utilizar
```py
from escavador import Processo, TiposBusca

resultado_busca = Processo().informacoes_no_tribunal("8809061-58.2022.8.10.3695")

#Para acessar campos da resposta
print(resultado_busca['status'])

#Para utilizar parametros opcionais de rotas, utilize os keyword arguments, iguais a documentação da API
resultado_busca = Processo().busca_em_lote(TiposBusca.BUSCA_POR_OAB, ['TJSP', 'TJBA'], numero_oab=12345, estado_oab='BA')
```

### Criando Monitoramentos
```py
from escavador import MonitoramentoTribunal, MonitoramentoDiario, TiposMonitoramentosTribunal, TiposMonitoramentosDiario,FrequenciaMonitoramentoTribunal

monitoramento_tribunal = MonitoramentoTribunal().criar_monitoramento(tipo_monitoramento=TiposMonitoramentosTribunal.UNICO,
                                                                     valor="8809061-58.2022.8.10.3695",tribunal='TJSP', 
                                                                     frequencia=FrequenciaMonitoramentoTribunal.SEMANAL)

monitoramento_diario = MonitoramentoDiario().criar_monitoramento(TiposMonitoramentosDiario.PROCESSO, processo_id=2, origens_ids=[2,4,6])
```

### Consultando Tribunais
```py
from escavador import Tribunal

tribunais_disponiveis = Tribunal().get_sistemas_tribunais_disponiveis()
```

### Obter Callbacks de buscas e monitoramentos
```py
from escavador import Callback

callbacks = Callback().get(data_maxima="2022-04-05")
```

### Download de documentos
```py
from escavador import Processo

resultado_busca = Processo().get_processo("8809061-58.2022.8.10.3695",wait=1,autos=1,usuario="user", senha="password")
link_documento = resultado_busca['resposta']['instancia'][0]['documentos_restritos'][2]['link_api']
documento = Processo().get_pdf(link_documento,'/documentos','autos')
```
### Módulos Disponíveis e Referência da API

| Módulo                | Link API                                                          |
|-----------------------|-------------------------------------------------------------------|
| Busca                 | https://api.escavador.com/docs/#busca                             |
| Processo              | https://api.escavador.com/docs/#processos                         |
| Callback              | https://api.escavador.com/docs/#callback                          |
| DiarioOficial         | https://api.escavador.com/docs/#dirios-oficiais                   |
| Instituicao           | https://api.escavador.com/docs/#instituies                        |
| Legislacao            | https://api.escavador.com/docs/#legislao                          |
| Jurisprudencia        | https://api.escavador.com/docs/#jurisprudncias                    |
| MonitoramentoDiario   | https://api.escavador.com/docs/#monitoramento-de-dirios-oficiais  |
| MonitoramentoTribunal | https://api.escavador.com/docs/#monitoramento-no-site-do-tribunal |
| Movimentacao          | https://api.escavador.com/docs/#movimentaes                       |
| Pessoa                | https://api.escavador.com/docs/#pessoas                           |
| Tribunal              | https://api.escavador.com/docs/#tribunais                         |
| Saldo                 | https://api.escavador.com/docs/#saldo-da-api                      | 