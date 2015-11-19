#!/bin/sh

# ruta al binario "unlzs"
unlzs=./unlzs
ROM_DIR=../tmp/
#ROM_FILE=rom-0asdasd
ROM_FILE=rom-0

# extraer spt.dat
rm -f $ROM_DIR/spt.dat
dd if=$ROM_DIR/$ROM_FILE of=$ROM_DIR/spt.dat bs=1 skip=8552 count=39600 2>/dev/null

# extraer data comprimida
rm -f $ROM_DIR/data
dd if=$ROM_DIR/spt.dat of=$ROM_DIR/data bs=1 count=220 skip=16 2>/dev/null

# descomprimir data y extraer password
pass=$($unlzs $ROM_DIR/data | strings | head -n 1)

echo -ne "\e[0;32m[+] Clave obtenida: \e[1;32m${pass}\e[0m\n"
echo -ne "\e[0;32m[+] Finalizado }:)\e[0m\n"
