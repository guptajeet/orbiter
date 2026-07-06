import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    config_dir: str = os.getenv("ORBITER_CONFIG_DIR", "")
    
    def _load_yaml(self, filename: str) -> dict:
        dir_path = Path(self.config_dir) if self.config_dir else None
        if not dir_path or not dir_path.exists():
            for p_cand in ["config", "../config", "backend/config", "../../config"]:
                p = Path(p_cand)
                if p.exists() and (p / "plugins.yaml").exists():
                    dir_path = p
                    break
        if not dir_path:
            dir_path = Path("../config")
            
        filepath = dir_path / filename
        if not filepath.exists():
            return {}
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    @property
    def default_config(self):
        return self._load_yaml("default.yaml")

    @property
    def ai_providers(self):
        return self._load_yaml("ai_providers.yaml")

    @property
    def job_sources(self):
        return self._load_yaml("job_sources.yaml")

    @property
    def automation_rules(self):
        return self._load_yaml("automation_rules.yaml")

    @property
    def plugins_config(self):
        return self._load_yaml("plugins.yaml")

    @property
    def schedules(self):
        return self._load_yaml("schedules.yaml")

    @property
    def digest(self):
        return self._load_yaml("digest.yaml")

    @property
    def domain_taxonomy(self):
        return self._load_yaml("domain_taxonomy.yaml")

    @property
    def ats_adapters(self):
        return self._load_yaml("ats_adapters.yaml")

    def _write_yaml(self, filename: str, data: dict):
        dir_path = Path(self.config_dir) if self.config_dir else None
        if not dir_path or not dir_path.exists():
            for p_cand in ["config", "../config", "backend/config", "../../config"]:
                p = Path(p_cand)
                if p.exists() and (p / "plugins.yaml").exists():
                    dir_path = p
                    break
        if not dir_path:
            dir_path = Path("../config")
            
        filepath = dir_path / filename
        with open(filepath, 'w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    def update_config_file(self, filename: str, updates: dict):
        data = self._load_yaml(filename) or {}
        
        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = deep_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d
            
        deep_update(data, updates)
        self._write_yaml(filename, data)

settings = Settings()
