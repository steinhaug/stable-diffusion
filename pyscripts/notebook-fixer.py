#!/usr/bin/env python3
"""
Jupyter Notebook Widget Metadata Fixer

This script scans .ipynb files and fixes widget metadata issues by:
1. Detecting corrupt or incomplete widget metadata
2. Either removing widget metadata entirely or fixing the structure
3. Creating backups before making changes
4. Providing detailed reports of what was fixed

Usage:
    python notebook_widget_fixer.py [path]
    
Arguments:
    path    Path to .ipynb file or directory (default: current directory)
    
Options:
    --dry-run       Show what would be fixed without making changes
    --no-backup     Don't create backup files (.bak)
    --fix-mode      'remove' (default) or 'repair' widget metadata
"""

import json
import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any


class NotebookWidgetFixer:
    def __init__(self, backup=True, fix_mode='remove', dry_run=False):
        self.backup = backup
        self.fix_mode = fix_mode
        self.dry_run = dry_run
        self.fixed_files = []
        self.errors = []
        
    def scan_file(self, filepath: Path) -> Tuple[bool, str]:
        """Scan a single notebook file for widget metadata issues."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Check if metadata exists and has widgets section
            metadata = notebook.get('metadata', {})
            widgets = metadata.get('widgets', None)
            
            if widgets is None:
                return False, "No widget metadata found"
            
            # Check for common widget metadata issues
            issues = []
            
            # Issue 1: widgets exists but missing 'state'
            if isinstance(widgets, dict) and 'state' not in widgets:
                issues.append("Missing 'state' key in widgets metadata")
            
            # Issue 2: widgets is empty dict but should have structure
            if widgets == {}:
                issues.append("Empty widgets metadata (should be removed)")
            
            # Issue 3: Malformed widgets structure
            if not isinstance(widgets, dict):
                issues.append(f"Invalid widgets metadata type: {type(widgets)}")
            
            # Issue 4: Partial widget state
            if isinstance(widgets, dict) and widgets.get('state') == {}:
                state_keys = widgets.get('state', {}).keys()
                if len(state_keys) == 0 and 'version_major' not in widgets:
                    issues.append("Incomplete widget metadata structure")
            
            return len(issues) > 0, "; ".join(issues)
            
        except json.JSONDecodeError as e:
            return True, f"JSON decode error: {str(e)}"
        except Exception as e:
            return True, f"Error reading file: {str(e)}"
    
    def fix_file(self, filepath: Path) -> Tuple[bool, str]:
        """Fix widget metadata issues in a notebook file."""
        try:
            # Read the notebook
            with open(filepath, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Create backup if requested
            if self.backup and not self.dry_run:
                backup_path = filepath.with_suffix('.ipynb.bak')
                shutil.copy2(filepath, backup_path)
                print(f"  → Backup created: {backup_path.name}")
            
            # Get metadata
            metadata = notebook.setdefault('metadata', {})
            
            if self.fix_mode == 'remove':
                # Remove widgets metadata entirely
                if 'widgets' in metadata:
                    del metadata['widgets']
                    action = "Removed widget metadata"
                else:
                    action = "No widget metadata to remove"
            
            elif self.fix_mode == 'repair':
                # Repair/add proper widget metadata structure
                metadata['widgets'] = {
                    "state": {},
                    "version_major": 2,
                    "version_minor": 0
                }
                action = "Repaired widget metadata structure"
            
            # Write the fixed notebook
            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(notebook, f, indent=2, ensure_ascii=False)
            
            return True, action
            
        except Exception as e:
            return False, f"Error fixing file: {str(e)}"
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """Find all .ipynb files in directory and subdirectories."""
        notebook_files = []
        
        if directory.is_file():
            if directory.suffix == '.ipynb':
                notebook_files.append(directory)
        else:
            # Recursively find all .ipynb files
            for filepath in directory.rglob('*.ipynb'):
                # Skip checkpoint files
                if '.ipynb_checkpoints' not in str(filepath):
                    notebook_files.append(filepath)
        
        return notebook_files
    
    def process_files(self, target_path: Path):
        """Main processing function."""
        print(f"🔍 Scanning for notebook files in: {target_path}")
        
        notebook_files = self.scan_directory(target_path)
        
        if not notebook_files:
            print("❌ No notebook files found!")
            return
        
        print(f"📚 Found {len(notebook_files)} notebook files")
        print()
        
        problematic_files = []
        
        # First pass: scan for issues
        print("🔍 Scanning for widget metadata issues...")
        for filepath in notebook_files:
            has_issue, issue_desc = self.scan_file(filepath)
            if has_issue:
                problematic_files.append((filepath, issue_desc))
                print(f"⚠️  {filepath.name}: {issue_desc}")
        
        if not problematic_files:
            print("✅ No widget metadata issues found!")
            return
        
        print(f"\n🛠️  Found {len(problematic_files)} files with issues")
        
        if self.dry_run:
            print("\n🔍 DRY RUN - No changes will be made")
            return
        
        # Second pass: fix issues
        print(f"\n🔧 Fixing files (mode: {self.fix_mode})...")
        fixed_count = 0
        
        for filepath, issue_desc in problematic_files:
            print(f"\n📝 Fixing: {filepath.name}")
            success, result = self.fix_file(filepath)
            
            if success:
                print(f"  ✅ {result}")
                fixed_count += 1
                self.fixed_files.append(str(filepath))
            else:
                print(f"  ❌ {result}")
                self.errors.append(f"{filepath}: {result}")
        
        print(f"\n🎉 Summary:")
        print(f"   Fixed: {fixed_count}/{len(problematic_files)} files")
        if self.errors:
            print(f"   Errors: {len(self.errors)}")


def main():
    parser = argparse.ArgumentParser(
        description="Fix Jupyter Notebook widget metadata issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python notebook_widget_fixer.py                    # Fix current directory
    python notebook_widget_fixer.py my_notebook.ipynb  # Fix single file
    python notebook_widget_fixer.py ./notebooks/       # Fix directory
    python notebook_widget_fixer.py --dry-run         # Preview changes
    python notebook_widget_fixer.py --fix-mode repair # Repair instead of remove
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to .ipynb file or directory (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help="Don't create backup files (.bak)"
    )
    
    parser.add_argument(
        '--fix-mode',
        choices=['remove', 'repair'],
        default='remove',
        help='How to fix widget metadata: remove it or repair structure (default: remove)'
    )
    
    args = parser.parse_args()
    
    target_path = Path(args.path)
    if not target_path.exists():
        print(f"❌ Path does not exist: {target_path}")
        sys.exit(1)
    
    # Initialize fixer
    fixer = NotebookWidgetFixer(
        backup=not args.no_backup,
        fix_mode=args.fix_mode,
        dry_run=args.dry_run
    )
    
    try:
        fixer.process_files(target_path)
        
        if fixer.errors:
            print(f"\n⚠️  Errors occurred:")
            for error in fixer.errors:
                print(f"   {error}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()