import streamlit as st
import database as db
import hashlib

# Função para hash de senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Inicialização do banco de dados
db.create_tables()

def login_form():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        hashed_password = hash_password(password)
        user = db.get_user(username)
        if user and user[2] == hashed_password:
           st.session_state["user"] = username
           st.success("Login realizado com sucesso!")
           st.rerun()
        else:
             st.error("Credenciais incorretas. Tente novamente.")

def registration_form():
    st.header("Cadastro")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Cadastrar"):
        hashed_password = hash_password(password)
        if db.add_user(username, hashed_password):
            st.success("Cadastro realizado com sucesso! Faça o login agora.")
            st.rerun()
        else:
            st.error("Username já cadastrado. Tente outro username.")


def todo_app():
    user_id = db.get_user_id_by_name(st.session_state["user"])
    todos = db.get_todos(user_id)

    st.header(f"Lista de tarefas de {st.session_state['user']}")
    new_task = st.text_input("Nova tarefa")
    if st.button("Adicionar tarefa"):
        if new_task:
            db.add_todo(user_id, new_task)
            st.rerun()


    for index, todo in enumerate(todos):
        col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
        with col1:
          checkbox = st.checkbox(label=todo[2], value=todo[3], key=f"checkbox_{index}")
        with col2:
            if st.button("Excluir",key=f"delete_{index}"):
               db.delete_todo(todo[0])
               st.rerun()
               
        if checkbox != todo[3]:
           db.update_todo(todo[0], int(checkbox))
           st.rerun()
           

def main():
    st.title("Lista de Tarefas")
    
    if "user" not in st.session_state:
        login_or_register = st.radio("Login ou Cadastro",["Login","Cadastro"])
        if login_or_register == "Login":
          login_form()
        else:
           registration_form()
    else:
        todo_app()
        if st.button("Logout"):
           del st.session_state["user"]
           st.rerun()
           

if __name__ == "__main__":
    main()