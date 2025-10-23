#!/bin/bash

project="/home/carlos/workspace/automap"

if [ -z "$CONDA_PREFIX" ]; then
    source /home/carlos/miniconda3/bin/activate $project/.venv
fi

# Directories paths
automap="$project/automap"
dataset="$project/datasets/blinkg"
# -------------------------
scenario="scenario1/1A"
exp="example"
# -------------------------
data="$dataset/data/$scenario"
exp_dir="$dataset/exps/${scenario}_$exp"

mkdir -p "$exp_dir"

# Link data to exp directory
for file in "$data"/*; do
    ln -sf "$file" "$exp_dir/"
done
ln -sf $data/../config.yaml $exp_dir/config.yaml

# ==============================================================================
# executables
python="python"

# Method
example="$python $automap/methods/example/example.py"

# Evaluation
eval="$python $automap/grapheval/compute_metrics.py"

# Postprocessing
post="$python $automap/postprocess/postprocess.py"
map2rml="$python $automap/converters/map2rml.py"
map2graph="java -jar $project/resources/rmlmapper-8.0.0-r378-all.jar"

# Data paths
mapping_yml_path="$exp_dir/mapping.yml"
mapping_rml_path="$exp_dir/mapping.rml.ttl"
pred_graph_path="$exp_dir/graph.nt"
gold_graph_path="$exp_dir/gold_graph.nt"
eval_results_path="$exp_dir/eval_results.json"
logs_path="$exp_dir/logs"
mkdir -p $logs_path
# ==============================================================================

# ==============================================================================
# PREDICTIONS
# ==============================================================================

$example \
    --output $mapping_yml_path

# ==============================================================================
# ==============================================================================
# MAPPING TO RML AND GRAPH GENERATION
# ==============================================================================

cat $mapping_yml_path | $map2rml > $mapping_rml_path 2> $logs_path/map2rml.log

touch $pred_graph_path
$map2graph \
    -m $mapping_rml_path \
    -o $pred_graph_path 2> $logs_path/rmlmapper.log

# ==============================================================================
# ==============================================================================
# EVALUATION
# ==============================================================================

cat $gold_graph_path | sort > $gold_graph_path.sorted
mv $gold_graph_path.sorted $gold_graph_path

cat $pred_graph_path | sort > $pred_graph_path.sorted
mv $pred_graph_path.sorted $pred_graph_path

cat $pred_graph_path | $eval \
    --config $exp_dir/config.yaml \
    --pred_mapping $mapping_rml_path \
    --gold_graph $gold_graph_path > $eval_results_path 

# ==============================================================================
