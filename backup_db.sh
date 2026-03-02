#!/bin/bash

# Configurações
BACKUP_DIR="/opt/ProjetoSigepe/backups"
DB_PATH="/opt/ProjetoSigepe/db.sqlite3"
REMOTE_HOST="192.168.1.14"
REMOTE_SHARE="backups - z"
REMOTE_PATH="BACKUP-SIGEPE"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="sigepe_backup_${TIMESTAMP}"
LOG_FILE="/opt/ProjetoSigepe/backup.log"

# Credenciais
USERNAME="DTI001515"
PASSWORD="suportedti@1"

# Criar diretório de backup local se não existir
mkdir -p "$BACKUP_DIR"

# Registrar início do backup
echo "[$(date)] Iniciando backup do banco de dados" >> "$LOG_FILE"

# Criar dump SQL do banco de dados
SQL_FILE="$BACKUP_DIR/${BACKUP_NAME}.sql"
if ! sqlite3 "$DB_PATH" .dump > "$SQL_FILE"; then
    echo "[$(date)] Erro ao criar dump SQL do banco de dados" >> "$LOG_FILE"
    exit 1
fi

# Compactar o dump SQL
if gzip -f "$SQL_FILE"; then
    SQL_FILE="${SQL_FILE}.gz"
    echo "[$(date)] Dump SQL criado e compactado: $SQL_FILE" >> "$LOG_FILE"
else
    echo "[$(date)] Erro ao compactar o dump SQL" >> "$LOG_FILE"
    exit 1
fi

# Manter uma cópia do banco de dados original
if cp "$DB_PATH" "$BACKUP_DIR/${BACKUP_NAME}.db"; then
    echo "[$(date)] Cópia do banco de dados criada: $BACKUP_DIR/${BACKUP_NAME}.db" >> "$LOG_FILE"
else
    echo "[$(date)] Erro ao criar cópia do banco de dados" >> "$LOG_FILE"
    exit 1
fi

# Enviar arquivos para o servidor remoto
echo "[$(date)] Enviando backup para o servidor remoto..." >> "$LOG_FILE"

# Criar o diretório remoto se não existir
if ! smbclient "//$REMOTE_HOST/$(echo -n "$REMOTE_SHARE" | sed 's/ /\ /g')" -U "$USERNAME%$PASSWORD" -c "mkdir '$REMOTE_PATH'" 2>/dev/null; then
    echo "[$(date)] Aviso: Não foi possível criar o diretório remoto. Continuando..." >> "$LOG_FILE"
fi

# Enviar os arquivos
ERROR_COUNT=0
for file in "$BACKUP_DIR/${BACKUP_NAME}."*; do
    if [ ! -e "$file" ]; then
        continue
    fi
    
    filename=$(basename "$file")
    if smbclient "//$REMOTE_HOST/$(echo -n "$REMOTE_SHARE" | sed 's/ /\ /g')" -U "$USERNAME%$PASSWORD" -c "cd '$REMOTE_PATH' 2>/dev/null || exit 1; put \"$file\" \"$filename\""; then
        echo "[$(date)] Arquivo $filename enviado com sucesso para //$REMOTE_HOST/$REMOTE_SHARE/$REMOTE_PATH/" >> "$LOG_FILE"
    else
        echo "[$(date)] Erro ao enviar o arquivo $filename para o servidor remoto" >> "$LOG_FILE"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
done

# Manter apenas os últimos 10 backups locais
(cd "$BACKUP_DIR" && ls -t | grep '^sigepe_backup_' | grep -E '\.(db|sql\.gz)$' | sort -r | awk 'NR>10 {print}' | xargs -r rm -f)

# Verificar se houve erros
if [ $ERROR_COUNT -eq 0 ]; then
    echo "[$(date)] Backup concluído com sucesso" >> "$LOG_FILE"
    exit 0
else
    echo "[$(date)] Backup concluído com $ERROR_COUNT erro(s)" >> "$LOG_FILE"
    exit 1
fi
