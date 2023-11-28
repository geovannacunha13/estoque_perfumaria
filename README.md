# Perfumaria

Bem-vindo ao sistema Perfumaria! Este sistema permite o gerenciamento de produtos em uma perfumaria. Foi desenvolvido utilizando Flask (Python) para o backend, PostgreSQL como banco de dados, e HTML/CSS/JS para o frontend.

## Recursos

- Cadastro e autenticação de clientes.
- Cadastro de pedidos, incluindo produtos e forma de pagamento.
- Administração de produtos e formas de pagamento.
- Interface intuitiva e responsiva para facilitar o uso em diferentes dispositivos.

## Instruções de Instalação e Uso

### Pré-requisitos

- Python instalado.
- PostgreSQL instalado.
- Ambiente virtual ativado.
- Flask instalado: pip install flask
- psycopg2 instalado: pip install psycopg2

### Configuração do Banco de Dados

1. Crie um banco de dados chamado `perfumes` no PostgreSQL.

2. Execute os seguintes comandos SQL dentro do banco de dados `perfumes` para criar as tabelas necessárias:

```sql
-- Tabelas
CREATE TABLE public.cliente (
    idcliente integer NOT NULL,
    celular character varying(45),
    cpf character varying(45),
    nome character varying(45),
    email character varying(255),
    senha character varying(255)
);

CREATE TABLE public.pagamento (
    idpagamento integer NOT NULL,
    tipo_pagamento character varying(45)
);

CREATE TABLE public.pedido (
    idpedido serial PRIMARY KEY,
    motoboy character varying(45),
    endereco character varying(255),
    idcliente integer,
    idpagamento integer,
    preco_total numeric(10,2)
);

CREATE TABLE public.perfume (
    idperfumaria serial PRIMARY KEY,
    nome_perfume character varying(45),
    quantidade integer,
    preco numeric(10,2),
    imagem text
);

### Configuração da Conexão com o Banco de Dados

1. Ajuste as configurações no arquivo `conexao.py`. Modifique as seguintes linhas de acordo com as configurações do seu banco de dados PostgreSQL:

    ```python
    import psycopg2
    import psycopg2.extras

    # Configurações do Banco de Dados
    DB_HOST = "localhost"
    DB_NAME = "perfumes"
    DB_USER = "seu_usuario_do_banco"
    DB_PASS = "sua_senha_do_banco"

    # Conectar ao Banco de Dados
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    ```

    Certifique-se de substituir `"seu_usuario_do_banco"` e `"sua_senha_do_banco"` pelos valores apropriados do seu banco de dados PostgreSQL.

### Executando o Projeto

1. Acesse a pasta do projeto.

2. Ative o ambiente virtual:

    ```bash
    .venv\Scripts\activate
    ```

3. Execute o projeto:

    ```bash
    python app.py run
    ```

O sistema estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000). Acesse [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin) para cadastrar e deletar perfumes, realizar cadastro de formas de pagamento, visualizar clientes cadastrados e realizar pedidos.
