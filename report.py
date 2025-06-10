#!/usr/bin/env python3
import os
import argparse
import json
from collections import defaultdict
from datetime import datetime

def parse_filename(filename):
    """Extract info from filename like 2025-06-09_linux_ubuntu24_04_konsole_d589539d.tsv"""
    base = os.path.basename(filename)
    parts = base.split('_')
    
    if len(parts) < 6:
        return None
    
    date = parts[0]
    os_name = parts[1]
    distro = '_'.join(parts[2:-2])  # Handle distro names with underscores
    terminal = parts[-2]
    hash_part = parts[-1].split('.')[0]
    
    return {
        'date': date,
        'os': os_name,
        'distro': distro,
        'terminal': terminal,
        'hash': hash_part,
        'filename': filename
    }

def count_mismatches(tsv_file):
    """Count lines in TSV file (excluding header)"""
    with open(tsv_file, 'r') as f:
        return sum(1 for line in f) - 1  # Subtract header line

def get_latest_results():
    """Get the latest results for each terminal"""
    results_dir = 'results'
    if not os.path.exists(results_dir):
        print(f"Error: {results_dir} directory not found")
        return []
    
    # Group by terminal
    terminals = defaultdict(list)
    
    for file in os.listdir(results_dir):
        if file.endswith('.tsv'):
            parsed = parse_filename(os.path.join(results_dir, file))
            if parsed:
                terminals[parsed['terminal']].append(parsed)
    
    # Get latest for each terminal
    latest_results = []
    for terminal, entries in terminals.items():
        # Sort by date descending
        latest = sorted(entries, key=lambda x: x['date'], reverse=True)[0]
        latest['mismatches'] = count_mismatches(latest['filename'])
        latest_results.append(latest)
    
    # Sort by mismatch count
    return sorted(latest_results, key=lambda x: x['mismatches'])

def output_tsv(results):
    """Output as TSV"""
    headers = ['terminal', 'mismatches', 'date', 'os', 'distro', 'hash']
    print('\t'.join(headers))
    
    for r in results:
        row = [r['terminal'], str(r['mismatches']), r['date'], r['os'], r['distro'], r['hash']]
        print('\t'.join(row))

def output_csv(results):
    """Output as CSV"""
    headers = ['terminal', 'mismatches', 'date', 'os', 'distro', 'hash']
    print(','.join(headers))
    
    for r in results:
        row = [r['terminal'], str(r['mismatches']), r['date'], r['os'], r['distro'], r['hash']]
        print(','.join(row))

def output_markdown(results):
    """Output as Markdown table with proper padding"""
    # Calculate column widths
    col_widths = {
        'terminal': max(len('Terminal'), max(len(r['terminal']) for r in results)),
        'mismatches': max(len('Mismatches'), max(len(str(r['mismatches'])) for r in results)),
        'date': max(len('Date'), max(len(r['date']) for r in results)),
        'os': max(len('OS'), max(len(r['os']) for r in results)),
        'distro': max(len('Distro'), max(len(r['distro']) for r in results)),
        'hash': max(len('Hash'), max(len(r['hash']) for r in results))
    }
    
    # Header
    header = f"| {'Terminal'.ljust(col_widths['terminal'])} | {'Mismatches'.ljust(col_widths['mismatches'])} | {'Date'.ljust(col_widths['date'])} | {'OS'.ljust(col_widths['os'])} | {'Distro'.ljust(col_widths['distro'])} | {'Hash'.ljust(col_widths['hash'])} |"
    print(header)
    
    # Separator
    sep = f"|{'-' * (col_widths['terminal'] + 2)}|{'-' * (col_widths['mismatches'] + 2)}|{'-' * (col_widths['date'] + 2)}|{'-' * (col_widths['os'] + 2)}|{'-' * (col_widths['distro'] + 2)}|{'-' * (col_widths['hash'] + 2)}|"
    print(sep)
    
    # Data rows
    for r in results:
        row = f"| {r['terminal'].ljust(col_widths['terminal'])} | {str(r['mismatches']).ljust(col_widths['mismatches'])} | {r['date'].ljust(col_widths['date'])} | {r['os'].ljust(col_widths['os'])} | {r['distro'].ljust(col_widths['distro'])} | {r['hash'].ljust(col_widths['hash'])} |"
        print(row)

def output_json(results):
    """Output as JSON"""
    output = []
    for r in results:
        output.append({
            'terminal': r['terminal'],
            'mismatches': r['mismatches'],
            'date': r['date'],
            'os': r['os'],
            'distro': r['distro'],
            'hash': r['hash']
        })
    print(json.dumps(output, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Generate report from Unicode width test results')
    parser.add_argument('--format', choices=['tsv', 'csv', 'markdown', 'json'], 
                        default='tsv', help='Output format (default: tsv)')
    
    args = parser.parse_args()
    
    results = get_latest_results()
    
    if not results:
        print("No results found")
        return
    
    # Output in requested format
    if args.format == 'tsv':
        output_tsv(results)
    elif args.format == 'csv':
        output_csv(results)
    elif args.format == 'markdown':
        output_markdown(results)
    elif args.format == 'json':
        output_json(results)

if __name__ == '__main__':
    main()