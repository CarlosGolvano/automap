#!/bin/bash

project="/home/carlos/workspace/automap"

if [ -z "$CONDA_PREFIX" ]; then
    conda activate $project/.venv
fi

scenario="discursos_navidad"
exp="pruebas"

core="${project}/core"
case="${project}/PODIO"
data="${case}/data/${scenario}"
exp_dir="${case}/exps/${scenario}_${exp}"

python_prueba="python $project/methods/example/does_nothing.py"
python_eval="python $core/evaluation/compute_metrics.py"
python_post="python $core/postproc/src/postprocess.py"

mkdir -p "${exp_dir}"

# python_prueba \
#     --data_path "${data}" \
#     --ext_data ".csv" \
#     --ext_onto ".rdf" \

cp "$data/mapping.yml" "$exp_dir/mapping.yml"

$python_post \
    "$exp_dir" \
