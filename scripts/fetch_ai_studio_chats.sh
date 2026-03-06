#!/bin/bash
OUTPUT_DIR="./google_ai_studio_sessions"
mkdir -p "$OUTPUT_DIR"

PARENT_ID=$(gog drive ls -j | jq -r '.files[] | select(.name=="Google AI Studio") | .id')

gog drive ls --parent="$PARENT_ID" --max=200 -j | jq -c '.files[]' | while read -r file; do
    ID=$(echo "$file" | jq -r '.id')
    NAME=$(echo "$file" | jq -r '.name')
    DATE=$(echo "$file" | jq -r '.modifiedTime | split("T")[0] | gsub("-"; "")')
    
    gog drive download "$ID" --out "$OUTPUT_DIR/"
    
    SRC=$(find "$OUTPUT_DIR" -maxdepth 1 -name "${ID}*" -print -quit)
    
    if [ -f "$SRC" ]; then
        DST="${OUTPUT_DIR}/${DATE}_${NAME}"
        [[ "$DST" != *.json ]] && DST="${DST}.json"
        mv "$SRC" "$DST"
        echo "Saved: $(basename "$DST")"
    fi
done
