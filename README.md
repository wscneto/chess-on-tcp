# chess-on-tcp

Este é um jogo de xadrez multijogador utilizando o protocolo TCP/IP.

O projeto foi realizado como requisito da disciplina Redes de Computadores (ECOM029).

Professor: Dr. Almir Pereira Guimarães.

Equipe:

-   Leandro Lima Albuquerque
-   Nícollas Provatti Gomes
-   Renato de Oliveira Pinto Filho
-   Walter Soares Costa Neto

## Instruções

Para criar um ambiente virtual onde as bibliotecas de Python serão instaladas., execute:

```bash
python3 -m venv .venv
```

Para ativar o ambiente virtual, execute:

```bash
source .venv/bin/activate
```

Para instalar as bibliotecas, execute:

```bash
pip install -r assets/requirements.txt
```

Agora, abra outro terminal na pasta do projeto e também ative o ambiente virtual nesse terminal.
Um terminal será utilizado para executar a aplicação como host, enquanto o outro executará como client.
Em cada um deles, execute:

```bash
python3 MainGame.py
```

Em um terminal, digite 'y' para hostear. No outro, digite 'n' para solicitar conexão com o host.
