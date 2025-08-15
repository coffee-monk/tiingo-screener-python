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
        print(f"  💾 Saved version '{version_name}'")

    def load_version(self, buffer_dir: Path, version_name: str, pattern: str = "*.csv") -> None:
        """Load version files into buffer"""
        version_dir = buffer_dir / version_name
        if not version_dir.exists():
            raise FileNotFoundError(f"Version '{version_name}' not found")
        
        self.clear_buffer(buffer_dir, pattern)
        for f in version_dir.glob(pattern):
            shutil.copy2(f, buffer_dir)
        print(f"  🔄 Loaded version '{version_name}\n'")

    def clear_buffer(self, buffer_dir: Path, pattern: str = "*.csv") -> None:
        """Clear buffer files matching pattern without counting"""
        [f.unlink() for f in buffer_dir.glob(pattern) if f.is_file()]
        print("\n  🧹 Cleared buffer files\n")

    # Specialized Operations -----------------------------

    def save_indicators(self, version_name: str) -> None:
        """Save current indicators"""
        self.save_version(self.indicators_dir, version_name)

    def save_scans(self, version_name: str) -> None:
        """Save current scans"""
        self.save_version(self.scanner_dir, version_name, "scan_results_*.csv")

    def save_tickers(self, version_name: str) -> None:
        """Save current tickers"""
        self.save_version(self.tickers_dir, version_name)

    def clear_all_buffers(self) -> None:
        """Clear all working directories while preserving versions"""
        print()
        self.clear_buffer(self.tickers_dir)
        self.clear_buffer(self.indicators_dir)
        self.clear_buffer(self.scanner_dir, "scan_results_*.csv")
        print("\n  ✨ All buffers cleared (versions preserved)")

    def format_duration(self, seconds):
        """Convert seconds to human-readable string (hours, minutes, seconds)"""
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.2f} hours"

    # Version Management --------------------------------

    def list_versions(self, 
                      buffer_dir: Union[Path, str], 
                      version_type: str = "Versions", 
                      limit: int = 10) -> List[str]:
        """List available versions with pretty printing"""
        if isinstance(buffer_dir, str):
            buffer_dir = getattr(self, buffer_dir)
        
        versions = sorted([d.name for d in buffer_dir.iterdir() if d.is_dir()], reverse=True)
        
        print(f"\n  📚 {version_type} ({len(versions)}):\n")
        for i, version in enumerate(versions[:limit]):
            print(f"  {i+1}. {version}")
        if len(versions) > limit:
            print(f"  ... + {len(versions) - limit} more")
        print()
        
        return versions

    def delete_version(self, buffer_dir: Path, version_name: str) -> None:
        """Delete specific version"""
        version_dir = buffer_dir / version_name
        if not version_dir.exists():
            raise FileNotFoundError(f"Version '{version_name}' not found")
        
        shutil.rmtree(version_dir)
        print(f"\n  🗑️ Deleted version '{version_name}'\n")

    def delete_all_versions(self, buffer_dir: Path, confirm: bool = True) -> int:
        """Delete all versions, returns count deleted"""
        versions = [d for d in buffer_dir.iterdir() if d.is_dir()]
        if not versions:
            print("  No versions to delete")
            return 0
            
        if confirm:
            print(f"  ⚠️ This will delete {len(versions)} versions:")
            for v in versions: print(f"  - {v.name}")
            if input("\n  Type 'DELETE' to confirm: ").upper() != "DELETE":
                print("Operation cancelled")
                return 0
        
        for v in versions: shutil.rmtree(v)
        print(f"  🔥 Deleted {len(versions)} versions")
        return len(versions)

    # Listing Functions --------------------------------

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
        all_scans = sorted(self.scanner_dir.glob("scan_results_*.csv"))
        total_scans = len(all_scans)
        scans_to_show = all_scans[:limit]
        
        print(f"\n  Scans in buffer (Total: {total_scans}, Showing first {limit}):\n")
        for i, scan in enumerate(scans_to_show, 1):
            print(f"  {i}. {scan.name}")
        if total_scans > limit:
            print(f"\n  ... + {total_scans - limit} more")
        print()

    def list_ind(self, limit: int = 10) -> None:
        """List indicator files in buffer with nice formatting"""
        all_indicators = sorted(self.indicators_dir.glob("*.csv"))
        total_indicators = len(all_indicators)
        indicators_to_show = all_indicators[:limit]
        
        print(f"\n  Indicators in buffer (Total: {total_indicators}, Showing first {limit}):")
        for i, indicator in enumerate(indicators_to_show, 1):
            print(f"  {i}. {indicator.name}")
        if total_indicators > limit:
            print(f"\n  ... and {total_indicators - limit} more")
        print()

    def list_tickers(self, limit: int = 10, timeframe: Optional[str] = None) -> None:
        """List ticker files in buffer with nice formatting
        
        Parameters:
            limit: Maximum number of files to display
            timeframe: Optional filter for specific timeframe (e.g., 'daily', 'weekly')
        """
        pattern = "*.csv" if timeframe is None else f"*_{timeframe}.csv"
        all_tickers = sorted(self.tickers_dir.glob(pattern))
        total_tickers = len(all_tickers)
        tickers_to_show = all_tickers[:limit]
        
        timeframe_label = f" ({timeframe})" if timeframe else ""
        print(f"\n  Tickers in buffer{timeframe_label} (Total: {total_tickers}, Showing first {limit}):\n")
        for i, ticker in enumerate(tickers_to_show, 1):
            print(f"  {i}. {ticker.name}")
        if total_tickers > limit:
            print(f"\n  ... + {total_tickers - limit} more")
        print()

# Create instance of Class to export
dm = DataManager({
    'INDICATORS_DIR': INDICATORS_DIR,
    'SCANNER_DIR': SCANNER_DIR,
    'TICKERS_DIR': TICKERS_DIR,
    'SCREENSHOTS_DIR': SCREENSHOTS_DIR
})
