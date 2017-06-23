from kivy.app import App
from kivy.app import runTouchApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.actionbar import ActionBar, ActionButton
from kivy.uix.actionbar import ActionView, ActionPrevious
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import StringProperty

from win32api import GetSystemMetrics
import datetime
import os
import sys

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

LabelBase.register(DEFAULT_FONT, 'ipaexm.ttf')

WINDOW_HEIGHT = GetSystemMetrics(1) - 100
WINDOW_WIDTH = 800

Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

RED = [1, 0, 0, 1]
GREEN = [0, 1, 0, 1]
BLUE = [0, 0, 1, 1]
GRAY = [1, 1, 1, 0.5]
DEFAULT_COLOR = [1, 1, 1, 1]
state_list = ['', '蕾', '花', '実']

# 列数
LINE_CNT = 3
# 株数
TUFT_CNT = 12
# 花数
FLOWER_CNT = 10

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


# データ保存ダイアログクラス
class SaveDialog():
    def __init__(self, title, txt, size, obj_list):
        print('pop up calss init')
        self.obj_list = obj_list
        self._box = BoxLayout(orientation='vertical')
        self.popup = Popup(title=title,
                           content=self._box,
                           auto_dismiss=False,
                           size_hint=(None, None),
                           size=tuple(size)
                           )
        # label
        self._label = Label(text=txt)
        self._box.add_widget(self._label)

        self._btn_layout = BoxLayout(orientation='horizontal')
        # close button
        self._y_btn = Button(text='はい', height=40, size_hint_y=None)
        self._n_btn = Button(text='いいえ', height=40, size_hint_y=None)
        self._y_btn.bind(on_press=self.save)
        self._n_btn.bind(on_press=self.popup_close)
        self._btn_layout.add_widget(self._y_btn)
        self._btn_layout.add_widget(self._n_btn)
        self._box.add_widget(self._btn_layout)

    # 現在のテキストの状態をcsvに保存する
    def save(self, src):
        print('Dialog Save')
        file_name = str(datetime.datetime.now())[0:10] + '.csv'
        w_txt = str(datetime.datetime.now())[0:10] + ','
        # 3列*12株*10花すべて1列CSVで保存する
        for j in range(LINE_CNT):
            for k in range(TUFT_CNT):
                for i in self.obj_list[j][k]:
                    # i = {'btn':[button obj], 'lbl':[label obj]}
                    w_txt = w_txt + i['lbl'].text + ','
        with open(FILE_PATH + '/' + file_name, 'w') as fp:
            fp.write(w_txt[:-1])
        self.popup.dismiss()

    def popup_open(self, instance):
        print('popup open')
        # ポップアップを開く
        self.popup.open()

    def popup_close(self, instance):
        print('popup close')
        # ポップアップを閉じる
        self.popup.dismiss()


class ScrollApp(App):
    obj_list = [[[] for j in range(TUFT_CNT)] for k in range(LINE_CNT)]
    last_data = [[['' for i in range(FLOWER_CNT)] for j in range(TUFT_CNT)] for k in range(LINE_CNT)]
    line = 1
    tuft = 1

    def app_close(self, instace):
        print('app_close')
        # pythonの終了
        # kivyのライフサイクルが働いているか不明
        sys.exit()

    # メインのスクロール画面の更新
    def disp_change(self, instance):
        print('call disp change')
        # 押下されたボタンが列切り替え
        if instance.id.split('_')[1] == '列':
            self.line = int(instance.id.split('_')[0])
            self.line_lbl.text = str(self.line) + '列目'
        # 押下されたボタンが株切り替え
        elif instance.id.split('_')[1] == '株':
            self.tuft = int(instance.id.split('_')[0])
            self.tuft_lbl.text = str(self.tuft) + '株目'
        else:
            print('Do Nothing(Error)')

        # 親のlayoutだけをクリアするとボタンとboxlayoutが
        # つながったままになってしまうので先にboxlayout以下をクリアする
        for chi in self.layout.children:
            chi.clear_widgets()

        # layout以下を削除
        self.layout.clear_widgets()
        # スクロールないのレイアウト再作成
        self.make_btn_layout()

    # デバッグとかテスト用
    def btn_test(self, instance):
        print('test')

    # スクロールないレイアウトの作成
    def make_btn_layout(self):
        print('make_btn_layout')

        box_obj = self.obj_list[self.line - 1][self.tuft - 1]
        for i in range(FLOWER_CNT):
            # 横並びのレイアウト表示
            boxlayout = BoxLayout(spacing=10, size_hint_y=None)
            # 1行ごとにボタンとラベルを表示
            boxlayout.add_widget(box_obj[i]['btn'])
            boxlayout.add_widget(box_obj[i]['lbl'])
            self.layout.add_widget(boxlayout)

    # 列、株切り替え用のドロップダウンリスト作成
    def make_dropdownlist(self, cnt, unit):
        print('make dropdown list')
        dropdown = DropDown()
        for index in range(cnt):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            btn = Button(text='%d %s' % (index + 1, unit),
                         size_hint_y=None, height=44,
                         id=str(index + 1) + '_' + unit)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            # btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            # 切り替えボタンが押されたとき描画を更新
            # ボタンのプロパティが渡されるので他の引数は不要(やりかたわからん)
            btn.bind(on_press=self.disp_change)

            # then add the button inside the dropdown
            dropdown.add_widget(btn)
        return dropdown

    # ツールバー作成
    def make_actionbar(self):
        # 保存ダイアログの作成
        self.pupupview = SaveDialog('保存ダイアログ', '保存しますか?',
                                    (WINDOW_WIDTH/2, WINDOW_HEIGHT/4),
                                    self.obj_list)
        actionview = ActionView()
        # actionview.use_separator = True
        ap = ActionPrevious(title='Tool Bar', with_previous=False)
        actionview.add_widget(ap)

        # 現在表示中の列、株番号をひょうじ
        # ツールバーにラベルを置けなさそうなのでcallbackのないボタンで作成
        self.line_lbl = ActionButton(text=str(self.line) + '列目')
        self.line_lbl.bind(on_press=self.btn_test)
        actionview.add_widget(self.line_lbl)

        self.tuft_lbl = ActionButton(text=str(self.tuft) + '株目')
        actionview.add_widget(self.tuft_lbl)

        # 押し間違いのためにボタン一つ分開けていたが、使っていない
        """
        self.null_btn2 = ActionButton(text='')
        actionview.add_widget(self.null_btn2)
        self.null_btn3 = ActionButton(text='')
        actionview.add_widget(self.null_btn3)
        """

        # 保存ダイアログを表示するボタン
        self.abtn1 = ActionButton(text='保存')
        # ダイアログ呼び出し
        self.abtn1.bind(on_press=self.pupupview.popup_open)
        actionview.add_widget(self.abtn1)

        # 押し間違いのためにボタン一つ分開けていたが、使っていない
        """
        self.null_btn4 = ActionButton(text='')
        actionview.add_widget(self.null_btn4)
        """

        # 列、株切り替え
        self.abtn2 = ActionButton(text="列変更")
        self.line_dropdown = self.make_dropdownlist(LINE_CNT, '列')
        # ドロップダウンリスト呼び出し
        self.abtn2.bind(on_press=self.line_dropdown.open)
        actionview.add_widget(self.abtn2)

        self.abtn3 = ActionButton(text="株変更")
        self.tufu_dropdown = self.make_dropdownlist(TUFT_CNT, '株')
        # ドロップダウンリスト呼び出し
        self.abtn3.bind(on_press=self.tufu_dropdown.open)
        actionview.add_widget(self.abtn3)

        # 押し間違いのためにボタン一つ分開けていたが、使っていない
        """
        self.null_btn5 = ActionButton(text='')
        actionview.add_widget(self.null_btn5)
        """

        self.abtn4 = ActionButton(text="終了")
        self.abtn4.bind(on_press=self.app_close)
        actionview.add_widget(self.abtn4)

        self.actionbar = ActionBar()
        self.actionbar.add_widget(actionview)
        return self.actionbar

    # 起動時に前回の結果を読み込む関数
    def load(self):
        isFile = False
        d = datetime.datetime.now()
        file_name = str(d)[0:10] + '.csv'
        # とりあえず直近一か月探す
        for i in range(30):
            print(FILE_PATH + '/' + file_name)
            if not os.path.isfile(FILE_PATH + '/' + file_name):
                d = d - datetime.timedelta(days=1)
                file_name = str(d)[0:10] + '.csv'
            else:
                isFile = True
                break
        # ファイルがある場合は読み込み
        # ファイルがない場合 or 一か月以上更新がなければすべて''で更新
        if isFile:
            with open(FILE_PATH + '/' + file_name, 'r') as fp:
                r_txt = fp.read()
            for i, stat in enumerate(r_txt.split(',')[1:]):
                load_line = int(i / (TUFT_CNT * FLOWER_CNT) % LINE_CNT)
                load_tuft = int(i / (FLOWER_CNT) % TUFT_CNT)
                load_flower = int(i % FLOWER_CNT)
                self.last_data[load_line][load_tuft][load_flower] = stat

    # テキストの状態を推移させる
    def change_state(self, src):
        # src.idに「id='b_' + str(i)」が来るので「_」で区切る
        idx = int(src.id.split('_')[1])
        # リストからIDを検索し、テキストラベルの状態を取得
        stat = self.obj_list[self.line - 1][self.tuft - 1][idx - 1]['lbl'].text

        # 見つからない場合、エラーになるのでexceptでキャッチしとく
        try:
            next_stat = state_list.index(stat) + 1
        except:
            print('error')

        # 状態が一周したら0に戻す
        if next_stat >= len(state_list):
            next_stat = 0
        # 状態を一つすすめた値をテキストラベルに書き込む
        self.obj_list[self.line - 1][self.tuft - 1][idx - 1]['lbl'].text = state_list[next_stat]

    # ソフト起動時(kivyのWindow作成時？)に呼ばれる関数
    # self.obj_list[列][株][花]
    def build(self):
        self.mainlayout = BoxLayout(spacing=10, size_hint_y=None,
                                    orientation='vertical')

        self.mainlayout.add_widget(self.make_actionbar())

        # load関数をコール
        self.load()
        # GridLayoutの作成
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Gridlayoutに入れるボタンとラベルの作成
        for j in range(LINE_CNT):
            for k in range(TUFT_CNT):
                for i in range(FLOWER_CNT):
                    # ボタンにidを割り当てる
                    btn = Button(text=str(i + 1) + '花', font_size=70,
                                 size_hint_y=None, height=100,
                                 id='b_' + str(i + 1))
                    text = Label(text=self.last_data[j][k][i],
                                 font_size=70, color=DEFAULT_COLOR,
                                 # kivy 1.9.1 だとshorten_fromが未対応なのでコメントアウト
                                 # outline_color=RED, shorten_from='center',
                                 id='l_' + str(i + 1))

                    # ボタン押下時の関数を割り当てる
                    btn.bind(on_press=self.change_state)
                    self.obj_list[j][k].append({'btn': btn, 'lbl': text})

        # self.make_btn_layout()がかくにんできるまでしばらく残しておく
        """
        for i in range(FLOWER_CNT):
            # 横並びのレイアウト表示
            boxlayout = BoxLayout(spacing=10, size_hint_y=None,
                                  id='box')
            # 1行ごとにボタンとラベルを表示
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['btn'])
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['lbl'])
            self.layout.add_widget(boxlayout)
        """

        self.make_btn_layout()

        # スクロールビューの作成
        root = ScrollView(size_hint=(1, None),
                          size=(Window.width, Window.height - 60))
        root.add_widget(self.layout)
        self.mainlayout.add_widget(root)
        return self.mainlayout

if __name__ == '__main__':
    ScrollApp().run()
