#!/usr/bin/env python3
"""
MCP Server Configuration Installer for Glaude-Code
Integrates MCP servers into Claude Code configuration
"""

import json
import shutil
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class MCPInstaller:
    """MCP Server configuration installer"""
    
    def __init__(self, config_dir: Path = None):
        """Initialize MCP installer"""
        self.project_root = Path(__file__).parent.parent
        self.config_dir = config_dir or self.project_root / "mcp" / "configs"
        self.claude_config_path = Path.home() / ".claude.json"
        self.mcp_config = self._load_mcp_configs()
        self.metadata = self._load_metadata()
        
    def _load_mcp_configs(self) -> Dict:
        """Load MCP server configurations from individual JSON files"""
        if not self.config_dir.exists():
            raise FileNotFoundError(f"MCP config directory not found: {self.config_dir}")
        
        mcp_servers = {}
        config_files = self.config_dir.glob("*.json")
        
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    # Each config file contains a single server configuration
                    mcp_servers.update(config)
            except json.JSONDecodeError as e:
                print(f"⚠️  Error reading {config_file.name}: {e}")
                continue
        
        return {"mcpServers": mcp_servers}
    
    def _load_metadata(self) -> Dict:
        """Load metadata for MCP servers"""
        # Define metadata for each server
        return {
            "servers": {
                "context7": {
                    "requires_api_key": True,
                    "api_key_env": "CONTEXT7_API_KEY",
                    "category": "documentation",
                    "description": "Official library documentation and code examples (optional API key for higher rate limits)"
                },
                "sequential-thinking": {
                    "requires_api_key": False,
                    "category": "problem-solving",
                    "description": "Multi-step problem solving and systematic analysis"
                },
                "magic": {
                    "requires_api_key": True,
                    "api_key_env": "TWENTYFIRST_API_KEY",
                    "category": "ui-generation",
                    "description": "Modern UI component generation and design systems"
                },
                "playwright": {
                    "requires_api_key": False,
                    "category": "testing",
                    "description": "Cross-browser E2E testing and automation"
                },
                "serena": {
                    "requires_api_key": False,
                    "category": "code-analysis",
                    "description": "Semantic code analysis and intelligent editing"
                },
                "morphllm-fast-apply": {
                    "requires_api_key": True,
                    "api_key_env": "MORPH_API_KEY",
                    "category": "code-modification",
                    "description": "Fast Apply capability for context-aware code modifications"
                },
                "notion": {
                    "requires_api_key": True,
                    "api_key_env": "NOTION_TOKEN",
                    "category": "productivity",
                    "description": "Rate-limited Notion integration (100 ops/hour)",
                    "rate_limit": "100 operations/hour"
                },
                "archon": {
                    "requires_api_key": False,
                    "category": "knowledge-management",
                    "description": "AI-powered knowledge base and task management platform",
                    "requires_docker": True,
                    "note": "Requires Docker running with Archon services (docker compose up)"
                },
                "selenium": {
                    "requires_api_key": False,
                    "category": "testing",
                    "description": "Cross-browser web automation with Selenium WebDriver",
                    "note": "Requires browser drivers (ChromeDriver, GeckoDriver, etc.)"
                }
            }
        }
    
    def _backup_claude_config(self) -> Optional[Path]:
        """Create timestamped backup of Claude configuration"""
        if not self.claude_config_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.claude_config_path.parent / f".claude.json.backup.{timestamp}"
        shutil.copy2(self.claude_config_path, backup_path)
        print(f"✓ Created backup: {backup_path}")
        return backup_path
    
    def _load_claude_config(self) -> Dict:
        """Load user's Claude configuration"""
        if not self.claude_config_path.exists():
            print("⚠️  Claude configuration not found. Creating new configuration...")
            return {}
        
        try:
            with open(self.claude_config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error reading Claude config: {e}")
            sys.exit(1)
    
    def _save_claude_config(self, config: Dict) -> bool:
        """Save updated Claude configuration"""
        try:
            with open(self.claude_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
            return False
    
    def list_servers(self, detailed: bool = False) -> None:
        """List available MCP servers"""
        servers = self.mcp_config.get("mcpServers", {})
        metadata = self.metadata.get("servers", {})
        
        # Group servers by category
        categories = {
            "documentation": [],
            "problem-solving": [],
            "code-analysis": [],
            "code-modification": [],
            "testing": [],
            "ui-generation": [],
            "productivity": [],
            "knowledge-management": [],
            "other": []
        }
        
        for server_name, server_config in servers.items():
            server_meta = metadata.get(server_name, {})
            category = server_meta.get("category", "other")
            categories[category].append((server_name, server_meta))
        
        print("\n📋 Available MCP Servers")
        print("=" * 60)
        
        # Show servers by category
        for category, servers_list in categories.items():
            if not servers_list:
                continue
            
            category_title = category.replace("-", " ").title()
            print(f"\n{category_title}:")
            print("-" * 40)
            
            for server_name, server_meta in servers_list:
                description = server_meta.get("description", "No description")
                
                # Build status indicators
                indicators = []
                if server_meta.get("requires_api_key"):
                    indicators.append("🔑")
                else:
                    indicators.append("✓")
                
                status = " ".join(indicators)
                
                if detailed:
                    print(f"\n  {status} {server_name}")
                    print(f"      {description}")
                    if server_meta.get("requires_api_key"):
                        api_key = server_meta.get("api_key_env", "API_KEY")
                        print(f"      Requires: {api_key}")
                    if server_meta.get("rate_limit"):
                        print(f"      Rate limit: {server_meta['rate_limit']}")
                else:
                    print(f"  {status} {server_name:<25} - {description}")
        
        print("\n" + "=" * 60)
        print("Legend: ✓ = No API key required, 🔑 = API key required")
        print("\nInstall with: python3 install_mcp.py install <server-name>")
    
    def install_servers(self, server_names: List[str] = None, force: bool = False) -> bool:
        """Install selected MCP servers"""
        available_servers = self.mcp_config.get("mcpServers", {})
        metadata = self.metadata.get("servers", {})
        
        # If no servers specified, install all
        if not server_names:
            server_names = list(available_servers.keys())
        
        # Validate server names
        invalid_servers = [s for s in server_names if s not in available_servers]
        if invalid_servers:
            print(f"❌ Unknown servers: {', '.join(invalid_servers)}")
            return False
        
        # Backup existing configuration
        backup_path = self._backup_claude_config()
        
        # Load current Claude configuration
        claude_config = self._load_claude_config()
        
        # Ensure mcpServers section exists
        if "mcpServers" not in claude_config:
            claude_config["mcpServers"] = {}
        
        # Install each server
        installed = []
        skipped = []
        
        for server_name in server_names:
            if server_name in claude_config["mcpServers"] and not force:
                print(f"⏭️  Skipping {server_name} (already configured, use --force to override)")
                skipped.append(server_name)
                continue
            
            server_config = available_servers[server_name].copy()
            # Add description from metadata if available
            if server_name in self.metadata.get("servers", {}):
                server_meta = self.metadata["servers"][server_name]
                # Don't add description to the actual config, just use for display
                print(f"   {server_meta.get('description', '')}")
            
            claude_config["mcpServers"][server_name] = server_config
            installed.append(server_name)
            print(f"✓ Configured: {server_name}")
        
        # Save updated configuration
        if installed:
            if self._save_claude_config(claude_config):
                print(f"\n✅ Successfully installed {len(installed)} MCP server(s)")
                if skipped:
                    print(f"ℹ️  Skipped {len(skipped)} existing server(s)")
                
                # Show API key requirements
                self._show_api_requirements(installed)
                return True
            else:
                if backup_path:
                    print(f"⚠️  Installation failed. Restore from: {backup_path}")
                return False
        else:
            print("ℹ️  No servers were installed")
            return True
    
    def _show_api_requirements(self, server_names: List[str]) -> None:
        """Show API key requirements for installed servers"""
        metadata = self.metadata.get("servers", {})
        api_required = []
        
        for server_name in server_names:
            server_meta = metadata.get(server_name, {})
            if server_meta.get("requires_api_key"):
                api_key = server_meta.get("api_key_env", "API_KEY")
                api_required.append((server_name, api_key))
        
        if api_required:
            print("\n⚠️  The following servers require API keys:")
            print("-" * 40)
            for server_name, api_key in api_required:
                print(f"  • {server_name}: export {api_key}='your-api-key'")
            print("\nAdd these to your shell profile (~/.zshrc or ~/.bashrc)")
    
    def remove_servers(self, server_names: List[str]) -> bool:
        """Remove MCP servers from configuration"""
        claude_config = self._load_claude_config()
        
        if "mcpServers" not in claude_config:
            print("ℹ️  No MCP servers configured")
            return True
        
        # Backup before removal
        self._backup_claude_config()
        
        removed = []
        for server_name in server_names:
            if server_name in claude_config["mcpServers"]:
                del claude_config["mcpServers"][server_name]
                removed.append(server_name)
                print(f"✓ Removed: {server_name}")
            else:
                print(f"⏭️  {server_name} not found in configuration")
        
        if removed:
            if self._save_claude_config(claude_config):
                print(f"\n✅ Successfully removed {len(removed)} MCP server(s)")
                return True
        
        return False
    
    def status(self) -> None:
        """Show current MCP configuration status"""
        claude_config = self._load_claude_config()
        configured_servers = claude_config.get("mcpServers", {})
        available_servers = self.mcp_config.get("mcpServers", {})
        
        print("\n📊 MCP Configuration Status")
        print("-" * 60)
        print(f"Configuration file: {self.claude_config_path}")
        print(f"Configured servers: {len(configured_servers)}")
        print(f"Available servers: {len(available_servers)}")
        
        if configured_servers:
            print("\n✅ Installed Servers:")
            for server_name in configured_servers:
                status = "✓" if server_name in available_servers else "⚠️  (unknown)"
                print(f"  {status} {server_name}")
        
        not_installed = set(available_servers.keys()) - set(configured_servers.keys())
        if not_installed:
            print("\n⏸️  Available but not installed:")
            for server_name in not_installed:
                print(f"  • {server_name}")

    def recommend(self, use_case: str = None) -> None:
        """Recommend MCP servers based on use case"""
        recommendations = {
            "starter": {
                "servers": ["context7", "sequential-thinking"],
                "description": "Basic documentation and problem-solving capabilities"
            },
            "web-dev": {
                "servers": ["context7", "magic", "playwright"],
                "description": "Web development with UI generation and testing"
            },
            "code-review": {
                "servers": ["serena", "sequential-thinking"],
                "description": "Code analysis and systematic review"
            },
            "productivity": {
                "servers": ["notion", "sequential-thinking"],
                "description": "Task management and systematic planning"
            },
            "full-stack": {
                "servers": ["context7", "serena", "playwright", "magic"],
                "description": "Complete development toolkit"
            }
        }
        
        if not use_case:
            print("\n🎯 MCP Server Recommendations by Use Case")
            print("=" * 60)
            for case, info in recommendations.items():
                print(f"\n{case}:")
                print(f"  {info['description']}")
                print(f"  Servers: {', '.join(info['servers'])}")
            print("\nUsage: python3 install_mcp.py recommend <use-case>")
            print("       python3 install_mcp.py install <server-names>")
        else:
            if use_case not in recommendations:
                print(f"❌ Unknown use case: {use_case}")
                print(f"Available: {', '.join(recommendations.keys())}")
                return
            
            rec = recommendations[use_case]
            print(f"\n🎯 Recommended for {use_case}: {rec['description']}")
            print("\nRecommended servers:")
            
            servers = self.mcp_config.get("mcpServers", {})
            metadata = self.metadata.get("servers", {})
            
            for server_name in rec['servers']:
                if server_name in servers:
                    server_meta = metadata.get(server_name, {})
                    description = server_meta.get("description", "")
                    
                    api_indicator = "🔑" if server_meta.get("requires_api_key") else "✓"
                    print(f"  {api_indicator} {server_name}: {description}")
            
            print(f"\nInstall with: python3 install_mcp.py install {' '.join(rec['servers'])}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Server Configuration Manager for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                    # List all available MCP servers
  %(prog)s list --detailed         # Show detailed server information
  %(prog)s recommend               # Show use-case recommendations
  %(prog)s recommend starter       # Get starter recommendations
  %(prog)s install context7        # Install a single server
  %(prog)s install notion serena   # Install multiple servers
  %(prog)s remove magic            # Remove a server
  %(prog)s status                  # Show configuration status
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available MCP servers")
    list_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed information")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install MCP servers")
    install_parser.add_argument("servers", nargs="*", help="Server names to install (all if omitted)")
    install_parser.add_argument("--force", action="store_true", help="Override existing configurations")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove MCP servers")
    remove_parser.add_argument("servers", nargs="+", help="Server names to remove")
    
    # Status command
    subparsers.add_parser("status", help="Show configuration status")
    
    # Recommend command
    recommend_parser = subparsers.add_parser("recommend", help="Get server recommendations")
    recommend_parser.add_argument("use_case", nargs="?", choices=["starter", "web-dev", "code-review", "productivity", "full-stack"], help="Use case for recommendations")
    
    args = parser.parse_args()
    
    # Initialize installer
    installer = MCPInstaller()
    
    # Execute command
    if args.command == "list":
        installer.list_servers(detailed=args.detailed)
    elif args.command == "recommend":
        installer.recommend(args.use_case)
    elif args.command == "install":
        success = installer.install_servers(args.servers, args.force)
        sys.exit(0 if success else 1)
    elif args.command == "remove":
        success = installer.remove_servers(args.servers)
        sys.exit(0 if success else 1)
    elif args.command == "status":
        installer.status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()