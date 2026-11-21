import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

COLUNAS_EDITAVEIS = {
    "nome", "preco", "quantidade_estoque",
    "tam_p", "tam_m", "tam_g", "tam_gg", "tam_xg",
}


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def cadastrar_produto(nome, preco, estoque, p, m, g, gg, xg):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO produtos
               (nome, preco, quantidade_estoque, tam_p, tam_m, tam_g, tam_gg, tam_xg)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (nome, preco, estoque, p, m, g, gg, xg),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def listar_produtos():
    conn = conectar()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM produtos ORDER BY id")
        return cur.fetchall()
    finally:
        conn.close()


def buscar_produto(id_produto):
    conn = conectar()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
        return cur.fetchone()  # None se não existir
    finally:
        conn.close()


def editar_produto(id_produto, **campos):
    """Ex.: editar_produto(3, preco=59.9, tam_m=10)"""
    campos = {c: v for c, v in campos.items() if c in COLUNAS_EDITAVEIS}
    if not campos:
        return False

    set_sql = ", ".join(f"{c} = %s" for c in campos)
    valores = list(campos.values()) + [id_produto]

    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE produtos SET {set_sql} WHERE id = %s", valores)
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def excluir_produto(id_produto):
    conn = conectar()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM produtos WHERE id = %s", (id_produto,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()