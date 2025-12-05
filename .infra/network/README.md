## Network system

Redes usadas por la infraestructura:

- db → 10.10.2.0/24
- service → 10.10.3.0/24
- security → 10.10.5.0/24

### Crear redes:

```bash
docker compose up -d network
```

### Inspección:

```bash
docker network inspect db
docker network inspect service
docker network inspect security
```

### IP forwarding (si aplica):

```bash
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
