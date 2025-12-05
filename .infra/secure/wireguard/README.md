## WireGuard

Levantar servicio:

```bash
docker compose up -d wireguard
``` 
Abrir el puerto ```51820/udp``` en el firewall o proveedor de la VM.
Se generan automáticamente los perfiles de conexión según el valor de ```PEERS``` en la carpeta ```data```.