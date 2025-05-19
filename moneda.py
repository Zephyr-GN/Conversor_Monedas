import flet as ft
import requests

API_KEY = "PONER KEY"  # https://www.exchangerate-api.com/
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair"

def main(page: ft.Page):
    page.title = "🌍 Conversor de Monedas"
    page.bgcolor = "#0b0c0c"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    monedas = ["USD", "EUR", "PEN", "COP", "MXN", "GBP"]

    titulo = ft.Text("💱 Conversor de Monedas", size=30, weight="bold", color="white")

    monto = ft.TextField(
        label="Monto",
        width=300,
        border_color="#3399ff",
        focused_border_color="#66ccff",
        text_style=ft.TextStyle(color="white"),
        label_style=ft.TextStyle(color="#cccccc"),
        cursor_color="white",
    )
    de_moneda = ft.Dropdown(
        label="De",
        width=300,
        options=[ft.dropdown.Option(m) for m in monedas],
        border_color="#3399ff",
        color="white",
        label_style=ft.TextStyle(color="#cccccc"),
    )
    a_moneda = ft.Dropdown(
        label="A",
        width=300,
        options=[ft.dropdown.Option(m) for m in monedas],
        border_color="#3399ff",
        color="white",
        label_style=ft.TextStyle(color="#cccccc"),
    )

    resultado = ft.Text("Resultado:", size=22, color="#ffffff", weight="bold")

    def convertir(e):
        try:
            cantidad = float(monto.value)
            de = de_moneda.value
            a = a_moneda.value

            if not de or not a:
                resultado.value = "⚠️ Selecciona ambas monedas."
            elif de == a:
                resultado.value = f"Resultado: {cantidad:.2f} {a}"
            else:
                url = f"{BASE_URL}/{de}/{a}/{cantidad}"
                response = requests.get(url)
                data = response.json()

                if data["result"] == "success":
                    convertido = data["conversion_result"]
                    resultado.value = f"Resultado: {convertido:.2f} {a}"
                else:
                    resultado.value = "❌ Error con la API"
        except Exception as err:
            resultado.value = f"⚠️ Error: {err}"
        page.update()

    boton = ft.ElevatedButton(
        text="Convertir 💹",
        on_click=convertir,
        bgcolor="#1e88e5",
        color="white",
        width=300,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    card = ft.Container(
        content=ft.Column(
            [titulo, monto, de_moneda, a_moneda, boton, resultado],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        border_radius=15,
        bgcolor="#1a1a1a",
        shadow=ft.BoxShadow(blur_radius=15, color="#222222", spread_radius=2),
        width=400,
    )

    page.add(card)

ft.app(target=main)
