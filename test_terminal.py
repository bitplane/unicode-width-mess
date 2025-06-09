#!/usr/bin/env python3
import sys
import os
import unicodedata
import hashlib
import platform
from datetime import datetime

try:
    import wcwidth
except ImportError:
    os.system("pip install wcwidth")
    import wcwidth


def get_terminal_info():
    terminal_name = os.environ.get('TERM', 'unknown')
    
    # Try to get the actual terminal binary (grandparent process)
    try:
        # Get parent PID (shell)
        ppid = os.getppid()
        
        # Get grandparent PID (terminal)
        with open(f'/proc/{ppid}/stat', 'r') as f:
            stat_line = f.read().strip()
            # PPID is the 4th field in /proc/pid/stat
            gppid = int(stat_line.split()[3])
        
        # Get terminal binary name and hash
        try:
            binary_path = os.readlink(f'/proc/{gppid}/exe')
            terminal_name = os.path.basename(binary_path)
            
            with open(binary_path, 'rb') as f:
                binary_content = f.read()
            binary_hash = hashlib.sha1(binary_content).hexdigest()[:8]
        except:
            # Fallback to comm if exe link fails
            with open(f'/proc/{gppid}/comm', 'r') as f:
                terminal_name = f.read().strip()
            binary_hash = "unknown"
            
        return terminal_name, binary_hash
    except:
        return terminal_name, "unknown"


def get_cursor_pos():
    sys.stdout.write('\x1b[6n')
    sys.stdout.flush()
    
    response = ""
    while True:
        c = sys.stdin.read(1)
        response += c
        if c == 'R':
            break
    
    if response.startswith('\x1b[') and response.endswith('R'):
        coords = response[2:-1].split(';')
        if len(coords) == 2:
            return int(coords[1])
    return 0


def main():
    terminal_name, binary_hash = get_terminal_info()
    print(f"Unicode Width Test - Terminal: {terminal_name} ({binary_hash})")
    
    mismatches = []
    tested = 0
    
    # Set raw mode for cursor queries
    os.system("stty raw -echo")
    
    try:
        for codepoint in range(32, 0x10FFFF + 1):
            try:
                char = chr(codepoint)
                
                # Skip control chars
                if unicodedata.category(char).startswith('C'):
                    continue
                    
                wcs_width = wcwidth.wcswidth(char)
                if wcs_width is None:
                    wcs_width = -1
                
                # Move to start of line, print char, get position
                sys.stdout.write('\r')
                sys.stdout.write(char)
                sys.stdout.flush()
                
                actual_width = get_cursor_pos() - 1
                
                if wcs_width != actual_width:
                    mismatches.append((
                        char,
                        wcs_width if wcs_width != -1 else None,
                        actual_width
                    ))
                
                tested += 1
                if tested % 100 == 0:
                    # Restore terminal temporarily to print progress
                    os.system("stty -raw echo")
                    print(f"\r{tested}/1114079 ({len(mismatches)}) U+{codepoint:04X}")
                    os.system("stty raw -echo")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                # Print the actual error without clearing screen
                os.system("stty -raw echo")
                print(f"\nError at U+{codepoint:04X}: {e}")
                break
    
    finally:
        os.system("stty -raw echo")
    
    # Get OS and distro info
    os_info = platform.system().lower()
    try:
        distro = "unknown"
        version = ""
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('ID='):
                    distro = line.split('=')[1].strip().strip('"')
                elif line.startswith('VERSION_ID='):
                    version = line.split('=')[1].strip().strip('"')
        
        if version:
            distro_version = f"{distro}{version}"
        else:
            distro_version = distro
    except:
        distro_version = "unknown"
    
    # Create filename (remove colons and other problematic chars)
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_terminal_name = terminal_name.replace(":", "_").replace("/", "_").replace(" ", "_")
    safe_distro_version = distro_version.replace(".", "_").replace(":", "_").replace("/", "_").replace(" ", "_")
    filename_base = f"results/{date_str}_{os_info}_{safe_distro_version}_{safe_terminal_name}_{binary_hash}"
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    # Save TSV results
    with open(f"{filename_base}.tsv", 'w') as f:
        f.write("char\twcswidth\tcursor moved\n")
        for char, wcs_width, actual_width in mismatches:
            wcs = wcs_width if wcs_width is not None else "None"
            f.write(f"{char}\t{wcs}\t{actual_width}\n")
    
    # Save markdown results
    md_content = f"# Unicode Width Test Results\n\n**Terminal:** {terminal_name} ({binary_hash})\n"
    md_content += f"**OS:** {os_info} {distro_version}\n\n"
    md_content += f"Found {len(mismatches)} characters where wcswidth differs from actual cursor movement:\n\n"
    md_content += "| Character | wcswidth | Cursor Moved |\n"
    md_content += "|-----------|----------|-------------|\n"
    
    for char, wcs_width, actual_width in mismatches:
        wcs = wcs_width if wcs_width is not None else "None"
        
        # Escape markdown special chars
        if char in ['|', '\\']:
            char = f"\\{char}"
        elif char.strip() == "":
            char = f"`{repr(char)}`"
            
        md_content += f"| {char} | {wcs} | {actual_width} |\n"
    
    with open(f"{filename_base}.md", 'w') as f:
        f.write(md_content)
    
    print(f"\nFound {len(mismatches)} mismatches")
    print(f"Files: {filename_base}.{{md,tsv}}")


if __name__ == "__main__":
    main()