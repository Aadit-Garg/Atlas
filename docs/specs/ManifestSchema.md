# Worker Manifest Schema

Every Worker must provide a `worker.yaml` file to declare its identity, Roles, execution policies, capabilities, and language implementation details.

There is exactly ONE canonical manifest format across the entire platform. Solon, Miron, Varsity, and the Runtime all consume this exact file.

## Schema Draft

```yaml
version: "1.0"

worker:
  id: string              # e.g. "atlas.worker.sqlite"
  name: string            
  version: string         
  language: string        # e.g. "python", "rust", "wasm"
  roles:                  
    - string              # e.g. "database", "storage"

execution:
  policy: string          # e.g. "singleton", "pool"

communication:
  transports:             # Transports supported by this Worker
    - string              # e.g. "shared_memory", "tcp"
  serialization:          # Serializations supported
    - string              # e.g. "json", "protobuf"

imports:                  
  capabilities:
    - name: string        
      version: string     
      optional: boolean   
      reason: string      

exports:                  
  capabilities:
    - name: string        
      version: string     
```
