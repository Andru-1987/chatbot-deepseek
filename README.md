# chatbot-deepseek

Evaluate the posible chatbot with python and deepseek using ollama

**INICIO DE LA INSTALACION DE OLLAMA:**
```bash
chmod +x download-ollama.sh
sh download-ollama.sh deepseek-r1:1.5b
```

---
```bash
# se installa el framework langchain:
pip install langchain
pip install chromadb
```

---
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload

```