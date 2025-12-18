from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import mysql.connector
import html

HOST = "localhost"
PORT = 8000

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Tqmad123hh11@_",
    "database": "proyecto_cdi"
}

ADMIN_PASSWORD = "cdi2025"  


def insertar_mensaje(nombre, correo, mensaje):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mensajes_contacto (nombre, correo, mensaje) VALUES (%s, %s, %s)",
        (nombre, correo, mensaje)
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_mensajes():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, correo, mensaje, fecha FROM mensajes_contacto ORDER BY fecha DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/enviar":
            self.handle_enviar()
        elif self.path == "/admin":
            self.handle_admin()
        else:
            self.send_error(404, "Ruta no encontrada")

    def parse_form(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        return urllib.parse.parse_qs(body)

    def handle_enviar(self):
        datos = self.parse_form()
        nombre = datos.get("nombre", [""])[0]
        correo = datos.get("correo", [""])[0]
        mensaje = datos.get("mensaje", [""])[0]

        try:
            insertar_mensaje(nombre, correo, mensaje)
            contenido = f"""
                <html><head><meta charset="utf-8"><title>Mensaje enviado</title></head>
                <body style="font-family:Segoe UI, sans-serif; background:#111; color:#f4f4f4; text-align:center;">
                    <h2>✅ Mensaje enviado correctamente</h2>
                    <p>Gracias, {html.escape(nombre or "")}, tu mensaje ha sido registrado.</p>
                    <a href="http://localhost:5500/contacto.html" style="color:#ffc400;">Volver al formulario</a>
                </body></html>
            """
        except Exception as e:
            print("Error al insertar mensaje:", e)
            contenido = """
                <html><head><meta charset="utf-8"><title>Error</title></head>
                <body style="font-family:Segoe UI, sans-serif; background:#111; color:#f4f4f4; text-align:center;">
                    <h2>❌ Ocurrió un error al guardar el mensaje</h2>
                    <p>Revisa la configuración de la base de datos.</p>
                </body></html>
            """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(contenido.encode("utf-8"))

    def handle_admin(self):
        datos = self.parse_form()
        password = datos.get("password", [""])[0]

        if password != ADMIN_PASSWORD:
            contenido = """
                <html><head><meta charset="utf-8"><title>Acceso denegado</title></head>
                <body style="font-family:Segoe UI, sans-serif; background:#111; color:#f4f4f4; text-align:center;">
                    <h2>❌ Contraseña incorrecta</h2>
                    <a href="http://localhost:5500/admin_mensajes.html" style="color:#ffc400;">Volver</a>
                </body></html>
            """
        else:
            filas = obtener_mensajes()
            filas_html = ""
            for (id_, nombre, correo, mensaje, fecha) in filas:
                filas_html += "<tr>"
                filas_html += f"<td>{id_}</td>"
                filas_html += f"<td>{html.escape(nombre)}</td>"
                filas_html += f"<td>{html.escape(correo)}</td>"
                filas_html += f"<td>{html.escape(mensaje)}</td>"
                filas_html += f"<td>{fecha}</td>"
                filas_html += "</tr>"

            contenido = f"""
                <html><head><meta charset="utf-8">
                    <title>Mensajes recibidos</title>
                </head>
                <body style="font-family:Segoe UI, sans-serif; background:#111; color:#f4f4f4;">
                    <h2 style="text-align:center;">📨 Mensajes recibidos desde el formulario</h2>
                    <table border="1" cellspacing="0" cellpadding="6" style="margin:20px auto; border-collapse:collapse; width:90%; background:#000;">
                        <thead>
                            <tr style="background:#ffc400; color:#111;">
                                <th>ID</th>
                                <th>Nombre</th>
                                <th>Correo</th>
                                <th>Mensaje</th>
                                <th>Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_html}
                        </tbody>
                    </table>
                    <p style="text-align:center;">
                        <a href="http://localhost:5500/admin_mensajes.html" style="color:#ffc400;">Cerrar sesión</a>
                    </p>
                </body></html>
            """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(contenido.encode("utf-8"))


def run():
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Servidor en http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
