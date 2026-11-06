#!/bin/zsh
# Execute every notebook in order and save the outputs in place.
cd "$(dirname "$0")/notebooks" || exit 1
for nb in *.ipynb; do
  echo "Running $nb"
  /opt/anaconda3/bin/jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=1800 "$nb" || echo "FAILED: $nb"
done
