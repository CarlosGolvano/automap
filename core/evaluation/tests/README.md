# Tests de Regresión

Este directorio contiene tests de regresión para asegurar que la nueva implementación `grapheval` produce los mismos resultados que la implementación original `rdfeval`.

## 📁 Estructura

```
tests/
├── README.md              # Este archivo
├── generate_baseline.py   # Genera métricas de referencia con rdfeval (antiguo)
├── test_regression.py     # Compara grapheval (nuevo) vs baselines
└── baselines/             # Resultados de referencia (generados automáticamente)
    ├── baseline_gold_pred.json
    └── baseline_gold2_pred.json
```

## 🚀 Uso

### 1. Generar Baselines (Primera vez)

Primero, genera los resultados de referencia usando la implementación antigua:

```bash
python tests/generate_baseline.py
```

Esto creará archivos JSON en `tests/baselines/` con los resultados de la implementación antigua (`rdfeval`) para:
- `data/pred.nt` vs `data/gold.nt`
- `data/pred.nt` vs `data/gold2.nt`

### 2. Ejecutar Tests de Regresión

Luego, ejecuta los tests que comparan la nueva implementación contra los baselines:

```bash
python tests/test_regression.py
```

Esto ejecutará la nueva implementación (`grapheval`) y comparará los resultados métrica por métrica.

### 3. Interpretar Resultados

El script mostrará:
- ✅ **Verde**: Métricas que coinciden exactamente
- ❌ **Rojo**: Métricas que difieren
- ⚠️ **Amarillo**: Métricas faltantes

Ejemplo de salida:

```
✅ triples.precision: 0.8571
✅ triples.recall: 0.8571
✅ triples.f1: 0.8571
✅ subjects.precision: 1.0000
✅ subjects.recall: 1.0000
✅ subjects.f1: 1.0000

SUMMARY
=========================================
Overall:
  Total metrics compared: 48
  ✅ ALL TESTS PASSED! (48/48)
```

## 🔍 Qué se Compara

Los tests comparan las siguientes métricas para cada categoría:

### Métricas Básicas
- **triples**: Evaluación de triples completos
- **subjects**: Evaluación de sujetos
- **subjects_fuzzy**: Evaluación fuzzy de sujetos
- **classes**: Evaluación de clases
- **classes_unique**: Evaluación de clases únicas

### Métricas de Propiedades
- **predicates**: Evaluación de predicados
- **predicates_unique**: Evaluación de predicados únicos
- **predicate_datatype_range**: Evaluación de datatypes
- **predicate_datatype_range_unique**: Evaluación única de datatypes

### Métricas de Objetos
- **objects**: Evaluación de objetos
- **objects_uris**: Evaluación de URIs
- **objects_literals**: Evaluación de literales

### Valores Comparados

Para cada métrica se comparan:
- `tp`: True Positives
- `fp`: False Positives
- `fn`: False Negatives
- `tn`: True Negatives
- `precision`: Precisión
- `recall`: Recall
- `f1`: F1-Score

## 🛠️ Troubleshooting

### Error: "Baseline not found"

Si ves este error:
```
❌ Baseline not found: tests/baselines/baseline_gold_pred.json
   Run: python tests/generate_baseline.py
```

**Solución**: Ejecuta primero el script de generación de baselines:
```bash
python tests/generate_baseline.py
```

### Error al importar rdfeval

Si al generar baselines obtienes un error de importación:
```
ImportError: cannot import name 'RDFeval' from 'rdfeval.rdfeval'
```

**Solución**: Asegúrate de que el paquete antiguo `rdfeval` está disponible. Si ya lo eliminaste, puedes regenerar los baselines más tarde o usar los que ya tienes guardados.

### Diferencias en los resultados

Si encuentras diferencias:

1. **Diferencias pequeñas (< 0.0001)**: Pueden ser por redondeo, generalmente aceptables
2. **Diferencias grandes**: Indica un posible bug en la reimplementación

Para investigar:
```python
# Cargar y comparar manualmente
import json

with open('tests/baselines/baseline_gold_pred.json') as f:
    baseline = json.load(f)

# Ejecutar nuevo
from grapheval import GraphEvaluator
from rdflib import Graph

test = Graph().parse('data/pred.nt', format='nt')
ref = Graph().parse('data/gold.nt', format='nt')
evaluator = GraphEvaluator(test, ref)
new_results = evaluator.evaluate_all()

# Comparar específico
print("Baseline:", baseline['triples'])
print("New:", new_results['triples'])
```

## 📊 Casos de Prueba

### Caso 1: gold_vs_pred
- **Test**: `data/pred.nt`
- **Reference**: `data/gold.nt`
- **Descripción**: Comparación estándar contra gold standard

### Caso 2: gold2_vs_pred
- **Test**: `data/pred.nt`
- **Reference**: `data/gold2.nt`
- **Descripción**: Comparación contra gold standard alternativo

## 🔄 Regenerar Baselines

Si modificas la implementación antigua o necesitas actualizar los baselines:

```bash
# Eliminar baselines existentes
rm -rf tests/baselines/

# Regenerar
python tests/generate_baseline.py
```

⚠️ **Advertencia**: Solo regenera baselines si estás seguro de que la implementación antigua es correcta.

## ✅ Checklist de Migración

Antes de considerar completa la migración:

- [ ] Baselines generados exitosamente
- [ ] Todos los tests de regresión pasan
- [ ] No hay métricas faltantes importantes
- [ ] Diferencias documentadas y justificadas
- [ ] Performance aceptable (nuevo vs antiguo)

## 📝 Notas

- Los baselines se guardan en formato JSON para fácil inspección
- Los tests usan tolerancia de `1e-6` para comparaciones numéricas
- Las métricas basadas en jerarquías pueden no estar en todos los baselines si falta la ontología
