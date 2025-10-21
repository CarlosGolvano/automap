#!/bin/bash

project="~/workspace/automap"
conda activate $project/.venv

scenario="discursos_navidad"
exp="pruebas"

core="${project}/core"
case="${project}/PODIO"
data="${case}/data/${scenario}"
exp_dir="${case}/exps/${scenario}_${exp}"

python_eval="python $core/evaluation/compute_metrics.py "

mkdir -p "${exp_dir}"


