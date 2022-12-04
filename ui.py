import json
from random import randint, choice

import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, MATCH, State, ALL
from dash.dcc import Store
from dash.html import Data
from dash_bootstrap_components import icons


class Hiragana:
    def __init__(self, hiragana, romaji, n_col, n_line):
        self.hiragana = hiragana
        self.romaji = romaji
        self.n_col = n_col
        self.n_line = n_line


class HiraganaTable:
    def __init__(self, file):
        self._hiraganas = {i: {j: None for j in range(1, 6, 1)} for i in range(1, 12, 1)}
        self._romaji_hiragana_dict = {}
        self._indices_list = []
        hiragana_romaji_list = f.read().split("\n")
        for _ in hiragana_romaji_list:
            hiragana, romaji, n_col, n_line = _.split(" ")
            n_col = int(n_col)
            n_line = int(n_line)
            self._indices_list.append([n_col, n_line])
            self._hiraganas[n_col][n_line] = Hiragana(hiragana, romaji, n_col, n_line)
            self._romaji_hiragana_dict[romaji] = self._hiraganas[n_col][n_line]

    def get(self, n_col, n_line):
        if [n_col, n_line] in self._indices_list:
            return self._hiraganas[n_col][n_line]
        return Hiragana("*", "*", None, None)

    def get_by_romaji(self, romaji):
        return self._romaji_hiragana_dict[romaji]

    def __str__(self):
        helper_list_line = ['n', 'w', 'r', 'y', 'm', 'h', 'n', 't', 's', 'k', '-']
        output = ""
        output += '{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}\n'
        hiraganas_list = []
        for i in range(1, 6, 1):
            hiragana_line = [hiragana_table.get(12 - j, i).hiragana for j in range(1, 12, 1)]
            hiraganas_list += hiragana_line
            output += '{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}\n'
        return output.format(*list(helper_list_line + hiraganas_list))


with open("hiragana_list.txt", "r", encoding="utf-8") as f:
    hiragana_table = HiraganaTable(f)

buttons = []
helper_list_line = ['n', 'w', 'r', 'y', 'm', 'h', 'n', 't', 's', 'k', '-']
output = ""
output += '{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}{:<2}\n'
hiraganas_list = []

chosen_hiraganas = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]


def color(i, j, chosen_list):
    if [i, j] in chosen_list:
        return "success"
    return "primary"


star_button = html.I(className="fa-solid fa-star text-muted")


def gen_buttons(style, chosen_list):
    buttons = []
    if style == "hiragana":
        for i in range(1, 6, 1):
            hiragana_line = html.Div([dbc.Button(hiragana_table.get(12 - j, i).hiragana, style={"min-width": "7vw"},
                                                 id={"type": "hiragana-button",
                                                     "value": hiragana_table.get(12 - j, i).romaji},
                                                 color=color(12 - j, i, chosen_list), className="fs-2")
                                      if hiragana_table.get(12 - j, i).hiragana != "*"
                                      else dbc.Button("", style={"min-width": "7vw"}, disabled=True)
                                      for j in range(1, 12, 1)],
                                     className="d-flex flex-col gap-1 justify-content-evenly")
            buttons.append(hiragana_line)
    else:
        for i in range(1, 6, 1):
            hiragana_line = html.Div([dbc.Button(star_button, style={"min-width": "7vw"},
                                                 id={"type": "hiragana-button",
                                                     "value": hiragana_table.get(12 - j, i).romaji},
                                                 color=color(12 - j, i, chosen_list), className="fs-2")
                                      if hiragana_table.get(12 - j, i).hiragana != "*"
                                      else dbc.Button("", style={"min-width": "7vw"}, disabled=True)
                                      for j in range(1, 12, 1)],
                                     className="d-flex flex-col gap-1 justify-content-evenly")
            buttons.append(hiragana_line)
    return buttons


buttons_div = html.Div(gen_buttons("hiragana", chosen_hiraganas), className="d-flex flex-column gap-1",
                       style={"width": "100%"}, id="buttons-div")
app = dash.Dash(
    external_stylesheets=[dbc.themes.SUPERHERO, icons.FONT_AWESOME]
)

app.layout = html.Div([html.Div(html.H1("Apprentissage hiraganas"),
                                className="m-2 d-flex flex-column justify-content-evenly align-items-center"),
                       html.Div([
                           html.Div([dbc.Button(html.I(className="fa-solid fa-eye"), id="hide-button", color="primary"),
                                     buttons_div], className="d-flex flex-row gap-2"),
                           html.Div([
                               html.P("かい", className="fs-1", id="hiragana-test-text"),
                               html.Div([dbc.Input(placeholder="romaji translation", className="fs-4"),
                                         dbc.Button(html.I(className="fa-solid fa-circle-arrow-right fs-4"))],
                                        className="d-flex flex-row"),
                           ], className="d-flex flex-column m-3 justify-content-center align-items-center",
                               style={"width": "50vw"}), ],
                           style={"width": "100vw", "height": "60vh"},
                           className="d-flex flex-column justify-content-evenly align-items-center"),
                       Store(data=chosen_hiraganas, id="chosen-hiraganas"),
                       Store(data=False, id="hidden-state")])


@callback(
    Output("hide-button", "color"),
    Output("buttons-div", "children"),
    Output("chosen-hiraganas", "data"),
    Output("hidden-state", "data"),

    Input({"type": "hiragana-button", "value": ALL}, "n_clicks"),
    Input("hide-button", "n_clicks"),
    State("hide-button", "color"),
    State({"type": "hiragana-button", "value": ALL}, "color"),
    State("chosen-hiraganas", "data"),
    State("hidden-state", "data"),
    prevent_initial_call=True
)
def change_color(n_hiragana, n_hide, previous_hide_color, hiraganas_color, old_chosen_hiraganas, hidden):
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"].split(".")[0] == "hide-button":
        if not hidden:
            return "secondary", gen_buttons("stars", old_chosen_hiraganas), old_chosen_hiraganas, True
        return "primary", gen_buttons("hiragana", old_chosen_hiraganas), old_chosen_hiraganas, False

    elif "hiragana-button" in ctx.triggered[0]["prop_id"].split(".")[0]:
        input_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
        romaji = input_id["value"]
        hiragana = hiragana_table.get_by_romaji(romaji)
        if [hiragana.n_col, hiragana.n_line] in old_chosen_hiraganas:
            old_chosen_hiraganas.remove([hiragana.n_col, hiragana.n_line])
        else:
            old_chosen_hiraganas.append([hiragana.n_col, hiragana.n_line])

        output_type = "hiragana"
        if hidden:
            output_type = "star"

        return "primary", gen_buttons(output_type, old_chosen_hiraganas), old_chosen_hiraganas, hidden

@callback(
    Output("hiragana-test-text", "children"),
    Input("chosen-hiraganas", "data"),

)
def change_test(chosen_hiraganas):
    n = randint(2, int(len(chosen_hiraganas)//2))
    text = "".join([hiragana_table.get(*choice(chosen_hiraganas)).hiragana for i in range(n)])
    return text
if __name__ == "__main__":
    app.run_server(debug=True)
