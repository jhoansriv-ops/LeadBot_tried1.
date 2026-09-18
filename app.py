from flask import Flask, render_template, jsonify
from dao.cliente_dao import ClienteDAO

app = Flask(__name__)


@app.route("/", methods=["GET"])
def vista_clientes():
    """Ruta web: Renderiza la tabla HTML consumiendo ClienteDAO."""
    lista_clientes = ClienteDAO.listar_todos()
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/api/clientes", methods=["GET"])
def api_clientes():
    """Ruta API REST: Retorna el listado en formato JSON."""
    lista_clientes = ClienteDAO.listar_todos()
    # Convertimos la lista de objetos Cliente a diccionarios
    datos = [
        {
            "id_cliente": c.id_cliente,
            "nombre": c.nombre,
            "telefono": c.telefono,
            "email": c.email,
            "estado": c.estado
        }
        for c in lista_clientes
    ]
    return jsonify(datos), 200


if __name__ == "__main__":
    print("Iniciando servidor web de LeadBot en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    