#!/usr/bin/env python3
"""
Memory Cleanup Script for Chatbot
Provides utilities to manage, backup, and clean chat memory files.

Usage:
    python scripts/cleanup_memory.py --help
    python scripts/cleanup_memory.py --backup
    python scripts/cleanup_memory.py --clear
    python scripts/cleanup_memory.py --stats
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# Add parent directory to path to import project modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from providers.memory_utils import MemoryManager, MemoryEntry
    from utils.logging_utils import setup_basic_logging, get_logger
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print("Make sure you're running this script from the project root or BanDongHanh_Website directory")
    sys.exit(1)

# Setup logging
setup_basic_logging(level="INFO")
logger = get_logger(__name__)


def create_backup(memory_manager: MemoryManager, backup_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Create a backup of the current memory file.
    
    Args:
        memory_manager: MemoryManager instance
        backup_dir: Custom backup directory (uses default if None)
        
    Returns:
        Path to backup file if successful, None otherwise
    """
    if not memory_manager.memory_exists:
        logger.warning("No memory file found to backup")
        return None
    
    try:
        # Create backup directory if specified
        if backup_dir:
            backup_dir.mkdir(exist_ok=True, parents=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"memory_backup_{timestamp}.json"
            
            # Copy memory file content
            memory_content = memory_manager.memory_file.read_text(encoding="utf-8")
            backup_file.write_text(memory_content, encoding="utf-8")
            
            logger.info(f"Memory backup created: {backup_file}")
            return backup_file
        else:
            # Use memory manager's built-in backup
            return memory_manager.backup_memory()
            
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        return None


def clear_memory(memory_manager: MemoryManager, create_backup_first: bool = True) -> bool:
    """
    Clear memory file with optional backup.
    
    Args:
        memory_manager: MemoryManager instance  
        create_backup_first: Whether to create backup before clearing
        
    Returns:
        True if successful, False otherwise
    """
    if create_backup_first and memory_manager.memory_exists:
        logger.info("Creating backup before clearing memory...")
        backup_path = memory_manager.backup_memory()
        if backup_path:
            logger.info(f"Backup created at: {backup_path}")
        else:
            logger.warning("Backup creation failed, but proceeding with clear")
    
    success = memory_manager.clear_memory()
    if success:
        logger.info("Memory cleared successfully")
    else:
        logger.error("Failed to clear memory")
    
    return success


def show_memory_stats(memory_manager: MemoryManager) -> Dict[str, Any]:
    """
    Display detailed memory statistics.
    
    Args:
        memory_manager: MemoryManager instance
        
    Returns:
        Dictionary with memory statistics
    """
    stats = memory_manager.get_memory_stats()
    
    print("\n=== MEMORY STATISTICS ===")
    
    if not stats.get("exists"):
        print("❌ No memory file found")
        return stats
    
    print(f"✅ Memory file exists")
    print(f"📊 Version: {stats.get('version', 'Unknown')}")
    print(f"📝 Summary length: {stats.get('summary_length', 0)} characters")
    print(f"💬 Message count: {stats.get('message_count', 0)}")
    print(f"🏷️  Topics tracked: {stats.get('topics_count', 0)}")
    print(f"⚙️  Preferences stored: {stats.get('preferences_count', 0)}")
    print(f"💾 File size: {stats.get('file_size', 0)} bytes")
    
    # Parse and display last updated time
    last_updated = stats.get('last_updated')
    if last_updated:
        try:
            updated_dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            time_ago = datetime.now() - updated_dt.replace(tzinfo=None)
            print(f"🕒 Last updated: {time_ago.days} days, {time_ago.seconds // 3600} hours ago")
        except Exception:
            print(f"🕒 Last updated: {last_updated}")
    
    # Show content preview if available
    memory = memory_manager.get_current_memory()
    if memory and memory.summary:
        preview = memory.summary[:200] + "..." if len(memory.summary) > 200 else memory.summary
        print(f"\n📖 Content preview:")
        print(f"   {preview}")
    
    return stats


def list_backups(backup_dir: Path = None) -> List[Path]:
    """
    List available backup files.
    
    Args:
        backup_dir: Directory to search for backups (searches common locations if None)
        
    Returns:
        List of backup file paths
    """
    backup_files = []
    search_dirs = []
    
    if backup_dir:
        search_dirs.append(backup_dir)
    else:
        # Search common backup locations
        current_dir = Path.cwd()
        search_dirs.extend([
            current_dir / "data",
            current_dir / "backups",
            current_dir / "logs",
            current_dir
        ])
    
    # Search for backup files
    for search_dir in search_dirs:
        if search_dir.exists():
            # Look for files with backup patterns
            patterns = ["*.bak", "*backup*.json", "*memory*.bak"]
            for pattern in patterns:
                backup_files.extend(search_dir.glob(pattern))
    
    # Sort by modification time (newest first)
    backup_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    
    return backup_files


def restore_from_backup(memory_manager: MemoryManager, backup_file: Path) -> bool:
    """
    Restore memory from a backup file.
    
    Args:
        memory_manager: MemoryManager instance
        backup_file: Path to backup file
        
    Returns:
        True if successful, False otherwise
    """
    if not backup_file.exists():
        logger.error(f"Backup file not found: {backup_file}")
        return False
    
    try:
        # Validate backup file format
        backup_content = backup_file.read_text(encoding="utf-8")
        backup_data = json.loads(backup_content)
        
        # Validate required fields
        required_fields = ["summary", "version", "updated_at"]
        if not all(field in backup_data for field in required_fields):
            logger.error("Invalid backup file format - missing required fields")
            return False
        
        # Create backup of current memory if it exists
        if memory_manager.memory_exists:
            logger.info("Creating backup of current memory before restore...")
            current_backup = memory_manager.backup_memory()
            if current_backup:
                logger.info(f"Current memory backed up to: {current_backup}")
        
        # Restore from backup
        memory_entry = MemoryEntry(**backup_data)
        success = memory_manager.save_memory(memory_entry)
        
        if success:
            logger.info(f"Memory restored from: {backup_file}")
            logger.info(f"Restored version: {memory_entry.version}")
        else:
            logger.error("Failed to save restored memory")
        
        return success
        
    except Exception as e:
        logger.error(f"Failed to restore from backup: {str(e)}")
        return False


def cleanup_old_backups(backup_dir: Path, keep_days: int = 30) -> int:
    """
    Clean up old backup files.
    
    Args:
        backup_dir: Directory containing backup files
        keep_days: Number of days to keep backups for
        
    Returns:
        Number of files deleted
    """
    if not backup_dir.exists():
        logger.warning(f"Backup directory not found: {backup_dir}")
        return 0
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    deleted_count = 0
    
    # Find old backup files
    for backup_file in backup_dir.glob("*.bak"):
        try:
            file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if file_mtime < cutoff_date:
                backup_file.unlink()
                logger.info(f"Deleted old backup: {backup_file}")
                deleted_count += 1
        except Exception as e:
            logger.warning(f"Failed to delete {backup_file}: {str(e)}")
    
    logger.info(f"Cleaned up {deleted_count} old backup files")
    return deleted_count


def main():
    """Main script function."""
    parser = argparse.ArgumentParser(
        description="Memory cleanup and management script for the chatbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cleanup_memory.py --stats
  python scripts/cleanup_memory.py --backup --backup-dir ./backups
  python scripts/cleanup_memory.py --clear --no-backup
  python scripts/cleanup_memory.py --restore backup_20231201_120000.json
  python scripts/cleanup_memory.py --list-backups
  python scripts/cleanup_memory.py --cleanup-old --keep-days 7
        """
    )
    
    # Main actions
    parser.add_argument("--stats", action="store_true", 
                       help="Show memory file statistics")
    parser.add_argument("--backup", action="store_true",
                       help="Create a backup of the current memory")
    parser.add_argument("--clear", action="store_true",
                       help="Clear the memory file")
    parser.add_argument("--restore", metavar="BACKUP_FILE",
                       help="Restore memory from backup file")
    parser.add_argument("--list-backups", action="store_true",
                       help="List available backup files")
    parser.add_argument("--cleanup-old", action="store_true",
                       help="Clean up old backup files")
    
    # Options
    parser.add_argument("--memory-dir", type=Path, default="data",
                       help="Memory file directory (default: data)")
    parser.add_argument("--memory-file", default="memory_chat.json",
                       help="Memory file name (default: memory_chat.json)")
    parser.add_argument("--backup-dir", type=Path,
                       help="Backup directory (default: same as memory dir)")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip backup when clearing memory")
    parser.add_argument("--keep-days", type=int, default=30,
                       help="Days to keep backup files (default: 30)")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress non-essential output")
    
    args = parser.parse_args()
    
    # Adjust logging level
    if args.quiet:
        logger.setLevel("WARNING")
    
    # Create memory manager
    memory_manager = MemoryManager(
        memory_dir=args.memory_dir,
        memory_file=args.memory_file
    )
    
    # Execute requested actions
    if args.stats:
        show_memory_stats(memory_manager)
    
    elif args.backup:
        backup_path = create_backup(memory_manager, args.backup_dir)
        if backup_path:
            print(f"✅ Backup created: {backup_path}")
        else:
            print("❌ Backup failed")
            sys.exit(1)
    
    elif args.clear:
        success = clear_memory(memory_manager, not args.no_backup)
        if success:
            print("✅ Memory cleared")
        else:
            print("❌ Clear failed")
            sys.exit(1)
    
    elif args.restore:
        backup_file = Path(args.restore)
        success = restore_from_backup(memory_manager, backup_file)
        if success:
            print(f"✅ Memory restored from: {backup_file}")
        else:
            print("❌ Restore failed")
            sys.exit(1)
    
    elif args.list_backups:
        backups = list_backups(args.backup_dir)
        if backups:
            print("\n📁 Available backups:")
            for i, backup in enumerate(backups, 1):
                size = backup.stat().st_size
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                print(f"  {i:2}. {backup.name} ({size} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("📁 No backup files found")
    
    elif args.cleanup_old:
        backup_dir = args.backup_dir or args.memory_dir
        deleted = cleanup_old_backups(backup_dir, args.keep_days)
        print(f"✅ Cleaned up {deleted} old backup files")
    
    else:
        # No action specified, show stats by default
        print("No action specified. Showing memory statistics:")
        show_memory_stats(memory_manager)
        print("\nUse --help for available options")


if __name__ == "__main__":
    main()