# 🤖 Robô Python de Envio de NPS por SFTP

Este projeto automatiza a geração e envio de arquivos CSV com dados de atendimento hospitalar para plataformas de NPS via SFTP, garantindo robustez com validações de internet, banco de dados e envio de alertas.

---

## ⚙️ Funcionalidades

- Consulta de dados Oracle via SQL
- Geração de múltiplos arquivos CSV segmentados
- Envio automatizado via SFTP
- Verificação de conectividade com a internet e o banco
- Envio de e-mails de alerta em caso de falha
- Logs de execução para auditoria

---

## 📂 Estrutura

| Arquivo | Descrição |
|--------|----------|
| `nps_bot.py` | Script principal |
| `monta_csv()` | Função que consulta dados e gera CSV |
| `enviar_via_sftp()` | Envio de arquivo para servidor remoto |
| `check_internet()` | Verifica conectividade |
| `check_database()` | Verifica disponibilidade do Oracle |
| `sem_internet() / sem_BD()` | Funções de fallback com alerta |

---

## 🧪 Exemplo de uso

```bash
python nps_bot.py
