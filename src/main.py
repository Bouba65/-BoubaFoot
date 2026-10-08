import flet as ft
import requests

LEAGUES = {
    "Premier League": "eng.1",
    "La Liga": "esp.1",
    "Ligue 1": "fra.1",
    "Bundesliga": "ger.1",
    "Serie A": "ita.1",
}

def get_matches(league_code):
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_code}/scoreboard"
        data = requests.get(url, timeout=8).json()
        return data.get("events", [])
    except:
        return []

def main(page: ft.Page):
    page.title = "BOUBA FOOT WORLD"
    page.bgcolor = "#0A0E21"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    selected_league = "eng.1"
    matches_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    def build_match_card(ev):
        comp = ev["competitions"][0]
        status = comp["status"]["type"]["description"]
        is_live = "in progress" in status.lower() or "half" in status.lower()

        team1 = comp["competitors"][0]
        team2 = comp["competitors"][1]

        # Mettre équipe à domicile en premier si possible
        t1_name = team1["team"]["shortDisplayName"]
        t2_name = team2["team"]["shortDisplayName"]
        t1_score = team1.get("score", "0")
        t2_score = team2.get("score", "0")
        t1_logo = team1["team"].get("logo", "")
        t2_logo = team2["team"].get("logo", "")

        dot_color = "#00FF87" if is_live else "#555555"
        status_text = "● LIVE" if is_live else comp["status"]["type"]["shortDetail"]

        return ft.Container(
            bgcolor="#1A1F3D",
            border_radius=15,
            padding=15,
            content=ft.Column([
                ft.Row([
                    ft.Container(width=8, height=8, bgcolor=dot_color, border_radius=4),
                    ft.Text(status_text, size=11, color=dot_color, weight=ft.FontWeight.BOLD),
                ]),
                ft.Row([
                    ft.Image(src=t1_logo, width=30, height=30) if t1_logo else ft.Text("⚽"),
                    ft.Text(t1_name, color="white", weight=ft.FontWeight.BOLD, expand=True),
                    ft.Text(t1_score, color="white", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Image(src=t2_logo, width=30, height=30) if t2_logo else ft.Text("⚽"),
                    ft.Text(t2_name, color="white", weight=ft.FontWeight.BOLD, expand=True),
                    ft.Text(t2_score, color="white", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], spacing=8)
        )

    def load_scores(e=None):
        matches_col.controls.clear()
        matches_col.controls.append(ft.ProgressRing(color="#00FF87"))
        page.update()

        events = get_matches(selected_league)
        matches_col.controls.clear()

        if not events:
            matches_col.controls.append(ft.Text("Aucun match aujourd'hui. Essaie une autre ligue.", color="white"))
        else:
            for ev in events[:12]:
                matches_col.controls.append(build_match_card(ev))
        page.update()

    def league_change(e):
        nonlocal selected_league
        selected_league = LEAGUES[e.control.value]
        load_scores()

    header = ft.Container(
        bgcolor="#000000",
        padding=20,
        content=ft.Column([
            ft.Text("BOUBA FOOT WORLD", size=26, weight=ft.FontWeight.BOLD, color="white"),
            ft.Text("LIVE SCORES • GUINÉE • MONDE", size=11, color="#00FF87"),
            ft.Dropdown(
                value="Premier League",
                options=[ft.dropdown.Option(k) for k in LEAGUES.keys()],
                on_change=league_change,
                bgcolor="#1A1F3D",
                color="white",
                border_color="#00FF87",
                width=200,
            ),
        ])
    )

    btn = ft.Container(
        padding=10,
        content=ft.ElevatedButton(
            "🔄 ACTUALISER LES SCORES LIVE",
            on_click=load_scores,
            bgcolor="#00FF87",
            color="black",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            height=50,
        )
    )

    page.add(
        ft.Column([
            header,
            ft.Container(content=matches_col, padding=15, expand=True),
            btn
        ], expand=True)
    )
    load_scores()

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)