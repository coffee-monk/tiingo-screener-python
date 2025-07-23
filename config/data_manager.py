import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union
from config.settings import (
                             INDICATORS_DIR, 
                             SCANNER_DIR, 
                             TICKERS_DIR, 
                             SCREENSHOTS_DIR
                            )

# Create DataManager Class
class DataManager:

    def __init__(self, config):
        """Initialize with paths from config"""
        self.indicators_dir  = Path(config['INDICATORS_DIR'])
        self.scanner_dir     = Path(config['SCANNER_DIR'])
        self.tickers_dir     = Path(config['TICKERS_DIR'])
        self.screenshots_dir = Path(config['SCREENSHOTS_DIR'])

    # Core File Operations --------------------------------

    def save_version(self, buffer_dir: Path, version_name: str, pattern: str = "*.csv") -> None:
        """Save current buffer files to a version folder"""
        version_dir = buffer_dir / version_name
        version_dir.mkdir(exist_ok=True)
        
        # Clear existing version files
        for f in version_dir.glob('*'):
            f.unlink()
        
        # Copy matching files
        for f in buffer_dir.glob(pattern):
            if f.is_file():
                shutil.copy2(f, version_dir)
        print(f"💾 Saved version '{version_name}'")

    def load_version(self, buffer_dir: Path, version_name: str, pattern: str = "*.csv") -> None:
        """Load version files into buffer"""
        version_dir = buffer_dir / version_name
        if not version_dir.exists():
            raise FileNotFoundError(f"Version '{version_name}' not found")
        
        self.clear_buffer(buffer_dir, pattern)
        for f in version_dir.glob(pattern):
            shutil.copy2(f, buffer_dir)
        print(f"🔄 Loaded version '{version_name}'")

    def clear_buffer(self, buffer_dir: Path, pattern: str = "*.csv") -> None:
        """Clear buffer files matching pattern without counting"""
        [f.unlink() for f in buffer_dir.glob(pattern) if f.is_file()]
        print("🧹 Cleared buffer files")

    # Specialized Operations -----------------------------

    def save_indicators(self, version_name: str) -> None:
        """Save current indicators"""
        self.save_version(self.indicators_dir, version_name)

    def save_scans(self, version_name: str) -> None:
        """Save current scans"""
        self.save_version(self.scanner_dir, version_name, "scan_results_*.csv")

    def clear_all_buffers(self) -> None:
        """Clear all working directories while preserving versions"""
        self.clear_buffer(self.tickers_dir)
        self.clear_buffer(self.indicators_dir)
        self.clear_buffer(self.scanner_dir, "scan_results_*.csv")
        self.clear_buffer(self.screenshots_dir)
        print("✨ All buffers cleared (versions preserved)")

    # Version Management --------------------------------

    def list_versions(self, 
                      buffer_dir: Union[Path, str], 
                      version_type: str = "Versions", 
                      limit: int = 10) -> List[str]:
        """List available versions with pretty printing"""
        if isinstance(buffer_dir, str):
            buffer_dir = getattr(self, buffer_dir)
        
        versions = sorted([d.name for d in buffer_dir.iterdir() if d.is_dir()], reverse=True)
        
        print(f"\n📚 {version_type} ({len(versions)}):")
        for i, version in enumerate(versions[:limit]):
            print(f"  {i+1}. {version}")
        if len(versions) > limit:
            print(f"  ... and {len(versions) - limit} more")
        
        return versions

    def delete_version(self, buffer_dir: Path, version_name: str) -> None:
        """Delete specific version"""
        version_dir = buffer_dir / version_name
        if not version_dir.exists():
            raise FileNotFoundError(f"Version '{version_name}' not found")
        
        shutil.rmtree(version_dir)
        print(f"🗑️ Deleted version '{version_name}'")

    def delete_all_versions(self, buffer_dir: Path, confirm: bool = True) -> int:
        """Delete all versions, returns count deleted"""
        versions = [d for d in buffer_dir.iterdir() if d.is_dir()]
        if not versions:
            print("No versions to delete")
            return 0
            
        if confirm:
            print(f"⚠️ This will delete {len(versions)} versions:")
            for v in versions: print(f"  - {v.name}")
            if input("Type 'DELETE' to confirm: ").upper() != "DELETE":
                print("Operation cancelled")
                return 0
        
        for v in versions: shutil.rmtree(v)
        print(f"🔥 Deleted {len(versions)} versions")
        return len(versions)

    def list_files(self, directory: Union[Path, str], pattern: str = "*", 
                  limit: int = 10, sort_by: str = "mtime") -> List[Path]:
        """List files in directory with various options"""
        if isinstance(directory, str):
            directory = getattr(self, directory)
            
        files = list(directory.glob(pattern))
        
        if sort_by == "mtime":
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        elif sort_by == "name":
            files.sort(key=lambda f: f.name)
            
        return files[:limit] if limit else files

    def list_scans(self, limit: int = 10) -> None:
        """List scan files in buffer with nice formatting"""
        scans = self.list_files(self.scanner_dir, "scan_results_*.csv", limit)
        
        print(f"\nCurrent scans in buffer ({len(scans)}):")
        for i, scan in enumerate(scans):
            print(f"  {i+1}. {scan.name}")

    def list_ind(self, limit: int = 10) -> None:
        """List indicator files in buffer with nice formatting"""
        indicators = self.list_files(self.indicators_dir, "*.csv", limit)
        
        print(f"\nCurrent indicators in buffer ({len(indicators)}):")
        for i, indicator in enumerate(indicators):
            print(f"  {i+1}. {indicator.name}")

    # Advanced Workflows --------------------------------
    
    def timestamped_run(self, fetch_fn, ind_fn, scan_fn) -> Dict[str, str]:
        """Run full pipeline with auto-versioning"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.clear_all_buffers()
        
        fetch_fn()
        ind_fn()
        self.save_indicators(f"auto_{timestamp}")
        
        scan_fn()
        self.save_scans(f"auto_{timestamp}")
        
        return {
            'indicators': f"auto_{timestamp}",
            'scans': f"auto_{timestamp}",
            'timestamp': timestamp
        }


# Create instance of Class to export
dm = DataManager({
    'INDICATORS_DIR': INDICATORS_DIR,
    'SCANNER_DIR': SCANNER_DIR,
    'TICKERS_DIR': TICKERS_DIR,
    'SCREENSHOTS_DIR': SCREENSHOTS_DIR
})
