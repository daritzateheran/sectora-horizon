## Lab Setup

### 1. Entrar a tu espacio
```bash
cdg <user>
```
### 2. Agregar tu SSH a GitHub
```bash
cat ~/lab/users/<user>/.ssh/id_rsa.pub
```
Cópiala en: *GitHub → Settings → SSH Keys*.

### 3. Clonar repos
```bash
git clone git@github-<git-user>.com/<repo>.git
```

### 4. Datos compartidos

En tu workspace verás **data** → ```~/lab/data```

### 5. Configurar SSH para conexiones remotas
```bash 
Host w-vm-super
    HostName super.eastus.cloudapp.azure.com
    User admin-superintendencia
    IdentityFile /path/to/superintendencia.pem
    LocalForward 3080 localhost:3080 # Metabase
    LocalForward 5050 localhost:5050 # PGAdmin
    LocalForward 5432 localhost:5432 # PostgreSQL
```

### 6. Generación de mapas personalizados

```bash
docker build -t geoprocessor /home/admin-superintendencia/lab/setup/infra/service/geoproccesor
docker run --rm \
  -v /home/admin-superintendencia/lab/data/raw:/data \
  -v /home/admin-superintendencia/lab/data/processed:/out \
  geoprocessor \
  sh -c "mapshaper \
          /data/dep_mun.topojson \
          -target MGN_ANM_DPTOS \
          -o format=geojson /out/colombia_departamentos.geojson"