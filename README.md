# htbscan
Este script automatiza un flujo de trabajo para conectarse a una VPN usando OpenVPN y realizar un escaneo de puertos y vulnerabilidades de una máquina en Hack The Box (HTB) utilizando Nmap.

Aquí está el detalle de lo que hace el script:

1. Verificar que `nmap` y `openvpn` están instalados.
    
2. Crear la estructura de carpetas para almacenar los resultados.
    
3. Conectarse a la VPN usando el archivo `.ovpn`.
    
4. Realizar un escaneo de puertos con Nmap.
    
5. Realizar un escaneo detallado de los puertos abiertos si se encuentran.
    
6. Guardar los resultados en un archivo.
    
7. Mantener la VPN activa y dar instrucciones para cerrarla.

- Ejemplo de uso:

```zsh
sudo htbscan -n Eureka -i 10.129.101.174 -v ~/VPN/release_arena_4ly3zz.ovpn
```





- Agregar el script a una carpeta del `$PATH`

1. **Dale permisos de ejecución**

```bash
chmod +x htb_tool.py
```

2. **Renombralo (opcional pero estético)**

Renombralo si querés que suene más a comando:

```bash
mv htb_tool.py htbscan
```

3. **Movelo a `/usr/local/bin`**

Esa ruta está incluida en `$PATH`, por lo que cualquier archivo ahí se puede ejecutar como comando global.

```bash
sudo mv htbscan /usr/local/bin/
```

4. **¡Listo! Ahora podés usarlo desde cualquier parte**

```bash
htbscan -n "Knife" -i 10.10.10.242 -v ~/HTB/knife.ovpn
```
