#!/bin/sh

for f in results/*.tsv; do
    echo "$(tail -n +2 "$f" | wc -l) $(basename "$f" | cut -d_ -f5)"
done | sort -n | column -t
