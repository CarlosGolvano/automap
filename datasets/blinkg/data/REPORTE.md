Autor: Carlos Golvano

# Informe detallado del contenido

scenario1: datos en json y xml (1H también en csv).
scenario2: datos en csv (d6 también en xml).
scenario3: datos en xml.

KG: solo en scenario1 (.nt)
Los mappings están en formato tabular (.md) -> habría que pasarlos a RML y crear el grafo.

- Escenarios con datos en json:
```
carlos@🦆:data/blinkg/scenarios ❯ ls ./*/* | grep -B 10 ".json" | grep '\./sce'
./scenario1/1A:
./scenario1/1B:
./scenario1/1C:
./scenario1/1D:
./scenario1/1E:
./scenario1/1F:
./scenario1/1G:
./scenario1/1H:
```
- Escenarios con datos en xml:
```
carlos@🦆:data/blinkg/scenarios ❯ ls ./*/* | grep -B 10 ".xml" | grep '\./sce'
./scenario1/1A:
./scenario1/1B:
./scenario1/1C:
./scenario1/1D:
./scenario1/1E:
./scenario1/1F:
./scenario1/1G:
./scenario1/1H:
./scenario2/d6:
./scenario3/1:
./scenario3/2:
```
- Escenarios con datos en csv:
```
carlos@🦆:data/blinkg/scenarios ❯ ls ./*/* | grep -B 10 ".csv" | grep '\./sce'
./scenario1/1H:
./scenario2/complete:
./scenario2/d1:
./scenario2/d2:
./scenario2/d3:
./scenario2/d4:
./scenario2/d5:
./scenario2/d6:
```

