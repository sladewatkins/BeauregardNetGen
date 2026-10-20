#!/usr/bin/env python3
"""
Beauregard NetGen is a quick static site generator for PHP-based websites.
all the benefits of PHP, but on Cloudflare Workers/Pages and GitHub Pages.
"""

import os
import re
import sys

def get_parts(parts_dir):
    """
    Reads parts from .html if present, else falls back to .php.
    """
    parts = {}
    for part_name in ["head", "navbar", "footer"]:
        html_part = os.path.join(parts_dir, f"{part_name}.html")
        php_part = os.path.join(parts_dir, f"{part_name}.php")
        if os.path.exists(html_part):
            with open(html_part, "r", encoding="utf-8") as f:
                parts[part_name] = f.read()
        elif os.path.exists(php_part):
            with open(php_part, "r", encoding="utf-8") as f:
                parts[part_name] = f.read()
        else:
            print(f"Warning: part '{part_name}' not found in {parts_dir}", file=sys.stderr)
    return parts

def build(root_dir="."):
    parts_dir = os.path.join(root_dir, "assets", "website", "parts")
    if not os.path.isdir(parts_dir):
        print(f"Error: asset/parts directory not found at {parts_dir}", file=sys.stderr)
        sys.exit(1)

    # 1. Also generate .html versions of the parts for clarity/editing
    for part in ["head", "navbar", "footer"]:
        php_p = os.path.join(parts_dir, f"{part}.php")
        html_p = os.path.join(parts_dir, f"{part}.html")
        if os.path.exists(php_p) and not os.path.exists(html_p):
            with open(php_p, "r", encoding="utf-8") as src, open(html_p, "w", encoding="utf-8") as dst:
                dst.write(src.read())

    parts = get_parts(parts_dir)

    # Matches PHP include snippets
    php_include_regex = re.compile(
        r"<\?php\s+\$path\s*=\s*\$_SERVER\[[\x27\x22]DOCUMENT_ROOT[\x27\x22]\];\s+\$path\s*\.=\s*[\x27\x22]/assets/website/parts/(\w+)\.php[\x27\x22];\s+include_once\(\$path\);\s*\?>"
    )

    converted_count = 0

    for dirpath, _, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir != "." and (rel_dir == "dist" or rel_dir.startswith("dist/") or rel_dir.startswith(".")):
            continue

        for filename in filenames:
            if not filename.endswith(".php"):
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            # Skip the reusable parts themselves
            if "assets/website/parts" in rel_path:
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            html_content = php_include_regex.sub(lambda m: parts.get(m.group(1), m.group(0)), content)
            
            html_filepath = os.path.splitext(filepath)[0] + ".html"
            with open(html_filepath, "w", encoding="utf-8") as out:
                out.write(html_content)

            converted_count += 1

    print(f"Successfully converted {converted_count} of the PHP pages in this directory to static HTML.")

if __name__ == "__main__":
    build()