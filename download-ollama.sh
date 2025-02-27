#!/usr/bin/bash

set -e

# Función para verificar si Ollama está instalado
check_ollama_installed() {
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama ya está instalado."
    else
        echo "⬇️  Ollama no está instalado. Descargando e instalando..."
        curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
        sudo tar -C /usr -xzf ollama-linux-amd64.tgz
        rm ollama-linux-amd64.tgz  # Limpiar archivo descargado
    fi
}

# Función para iniciar Ollama si no está corriendo
start_ollama() {
    if pgrep -x "ollama" > /dev/null; then
        echo "✅ Ollama ya está en ejecución."
    else
        echo "🚀 Iniciando Ollama..."
        ollama serve &
        sleep 2  # Darle tiempo para iniciar
    fi
}

# Función para verificar y descargar un modelo si no está presente
download_model() {
    local model_name="$1"

    if [[ -z "$model_name" ]]; then
        echo "❌ Error: No se especificó un modelo."
        exit 1
    fi

    if ollama list | grep -q "$model_name"; then
        echo "✅ El modelo $model_name ya está disponible."
    else
        echo "⬇️  Descargando el modelo $model_name..."
        ollama run "$model_name"
    fi
}

# Función para mostrar la versión de Ollama
show_version() {
    echo "✅ Todo listo. Versión de Ollama:"
    ollama -v
}

# Main
check_ollama_installed
start_ollama
download_model "$1"
show_version
