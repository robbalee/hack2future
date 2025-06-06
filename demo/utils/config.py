"""
Configuration utilities for the insurance fraud detection system.
"""
import os
import json
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the application"""
    _instance = None
    _config: Dict[str, Any] = {
        'app': {
            'debug': True,
            'upload_folder': 'uploads',
            'max_file_size': 16 * 1024 * 1024,  # 16MB
            'allowed_extensions': {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        },
        'storage': {
            'claims_dir': 'claims_data',
            'events_dir': 'events_data',
            'backup_dir': 'backups'
        },
        'database': {
            'use_cosmos': False,
            'cosmos_endpoint': os.environ.get('COSMOS_ENDPOINT', ''),
            'cosmos_key': os.environ.get('COSMOS_KEY', ''),
            'cosmos_database': os.environ.get('COSMOS_DATABASE', 'insurance-fraud-db'),
            'cosmos_container': os.environ.get('COSMOS_CONTAINER', 'claims')
        }
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_config()
        return cls._instance
    
    @classmethod
    def _load_config(cls):
        """Load configuration from config.json if it exists"""
        config_path = os.path.join('config', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Convert allowed_extensions from list to set if needed
                    if 'app' in loaded_config and 'allowed_extensions' in loaded_config['app']:
                        if isinstance(loaded_config['app']['allowed_extensions'], list):
                            loaded_config['app']['allowed_extensions'] = set(loaded_config['app']['allowed_extensions'])
                    cls._update_dict_recursive(cls._config, loaded_config)
                print(f"Loaded configuration from {config_path}")
            except (json.JSONDecodeError, IOError) as e:
                # If there's an error loading the config, use defaults
                print(f"Error loading config file: {str(e)}")
                pass
    
    @classmethod
    def _update_dict_recursive(cls, target, source):
        """Update a nested dictionary recursively"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                cls._update_dict_recursive(target[key], value)
            else:
                target[key] = value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        keys = key.split('.')
        result = cls._config
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            else:
                return default
        return result
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a configuration value by key"""
        keys = key.split('.')
        config = cls._config
        for i, k in enumerate(keys[:-1]):
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
