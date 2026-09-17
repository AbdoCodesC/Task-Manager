import re
import uuid 

def create_slug(name: str) -> str: 
  base = name.lower().strip()
  base = re.sub(r"[^a-z0-9\s-]", "", base)
  base = re.sub(r"[\s-]+", "-", base).strip("-")
  return f"{base}-{uuid.uuid4().hex[:8]}"