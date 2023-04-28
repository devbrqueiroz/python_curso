from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='mysql.queirozsantana.com.br',
        user='queirozsantana',
        password='banco0001',
        database='queirozsantana'
    )
    return connection

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/cursos', methods=['GET'])
def cursos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cursos')
    cursos = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/curso/<int:id>', methods=['GET'])
def curso(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cursos WHERE id=%s', (id,))
    curso = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('curso.html', curso=curso)

@app.route('/criar_curso', methods=['GET', 'POST'])
def criar_curso():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO cursos (nome, descricao, carga_horaria) VALUES (%s, %s, %s)', (nome, descricao, carga_horaria))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('cursos'))
    return render_template('criar_curso.html')

@app.route('/editar_curso/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        carga_horaria = request.form['carga_horaria']
        cursor.execute('UPDATE cursos SET nome=%s, descricao=%s, carga_horaria=%s WHERE id=%s', (nome, descricao, carga_horaria, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('cursos'))
    cursor.execute('SELECT * FROM cursos WHERE id=%s', (id,))
    curso = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editar_curso.html', curso=curso)

@app.route('/excluir_curso/<int:id>', methods=['GET', 'POST'])
def excluir_curso(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cursos WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('cursos'))

if __name__ == '__main__':
    app.run(debug=True)
