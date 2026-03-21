# (c) 2026 Eugene Zavirukha
# Licensed under the Apache License, Version 2.0

import re


def sanitize_filename(url):
    # Cleaning file name because of Windows
    clean = re.sub(r'https?://', '', url)
    clean = re.sub(r'[\\/*?:"<>|.=]', '_', clean)
    return clean[:50]  # Limit length


def save_results(results, base_url, start_id, end_id, file_format=".txt"):
    filename = f"report_{sanitize_filename(base_url)}_{start_id}-{end_id}{file_format}"

    try:
        if file_format == ".txt":
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(results))
        # elif file_format == ".json":
        return filename
    except Exception as e:
        return f"Error: {e}"
