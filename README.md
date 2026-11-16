# Sistema de Reservas de Hotel em Python

## Estrutura do Projeto
- `main.py`: Ponto de entrada, menu interativo, validações de datas e fluxo principal.
- `models.py`: Classes de domínio (`Cliente`, `Quarto`, `QuartoSolteiro`, `QuartoCasal`, `Suite`, `Reserva`).
- `exceptions.py`: Exceções personalizadas para regras de negócio do hotel.
- `storage.py`: Persistência de dados em arquivo JSON.

## Como Executar no VS Code
1. Extraia a pasta `sistema_hotel`.
2. Abra a pasta no VS Code (`Arquivo > Abrir Pasta...`).
3. Abra o terminal integrado (`Ctrl + '`) e execute:
```bash
python main.py
```
