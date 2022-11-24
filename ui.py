import dash
import dash_bootstrap_components as dbc
from dash import html


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
for i in range(1, 6, 1):
    hiragana_line = html.Div([dbc.Button(hiragana_table.get(12-j, i).hiragana , style={"min-width":"5vw"})
                              if hiragana_table.get(12-j, i).hiragana != "*"
                              else dbc.Button("" , style={"min-width":"5vw"}, disabled=True)
                              for j in range(1, 12, 1)],
                             className="d-flex flex-col gap-1 justify-content-evenly")
    buttons.append(hiragana_line)
buttons_div = html.Div(buttons, className="d-flex flex-column gap-1",
                      style={"width":"25vw"})
app = dash.Dash(
    external_stylesheets=[dbc.themes.SUPERHERO]
)

app.layout = html.Div([html.H1("Apprentissage hiraganas"),
                       buttons_div],
                      style={"width":"100vw"},
                      className="d-flex flex-column justify-content-center align-items-center")

if __name__ == "__main__":
    app.run_server()