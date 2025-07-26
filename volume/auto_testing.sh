#!/bin/bash

fail_list=()
success_list=()

for script in test_*.py; do
    echo "Running $script ..."
    if python "$script"; then
        success_list+=("$script")
    else
        echo "❌ $script failed!"
        fail_list+=("$script")
    fi
done

echo "-----------------------------"
echo "Success scripts:"
for s in "${success_list[@]}"; do
    echo "  $s"
done

echo "-----------------------------"
echo "Failed scripts:"
for f in "${fail_list[@]}"; do
    echo "  $f"
done

if [ ${#fail_list[@]} -gt 0 ]; then
    exit 1
else
    echo "All test scripts finished successfully."
fi