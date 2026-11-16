# Sistema de Reservas de Hotel em Python

## Estrutura do Projeto
- `main.py`: Ponto de entrada, menu interativo, validações de entrada e datas, fluxo principal.
- `models.py`: Classes de domínio (`Cliente`, `Quarto`, `QuartoSolteiro`, `QuartoCasal`, `Suite`, `Reserva`).
- `exceptions.py`: Exceções personalizadas para regras de negócio do hotel.
- `storage.py`: Persistência de dados em arquivo JSON (com cópia de segurança `.bak` se o arquivo estiver corrompido).
- `dados_hotel.json`: Arquivo de dados (clientes, quartos e reservas). É criado/atualizado automaticamente.
- `PRINTS/`: Capturas de tela da execução.

## Como Executar no VS Code
1. Extraia a pasta `sistema_hotel`.
2. Abra a pasta no VS Code (`Arquivo > Abrir Pasta...`).
3. Abra o terminal integrado (`Ctrl + '`) e execute:
```bash
python main.py
```
