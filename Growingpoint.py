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
        for j in range(LINE_CNT):
            for k in range(TUFT_CNT):
                for i in self.obj_list[j][k]:
                    w_txt = w_txt + i['lbl'].text + ','
                with open('C:/Users/yuuma_000/' + file_name, 'w') as fp:
                    fp.write(w_txt[:-1])
                self.popup.dismiss()

    def popup_open(self, instance):
        print('popup open')
        print(type(instance))
        # ポップアップを開く
        self.popup.open()

    def popup_close(self, instance):
        print('popup close')
        print(type(instance))
        # ポップアップを閉じる
        self.popup.dismiss()


class ScrollApp(App):
    obj_list = [[[] for j in range(TUFT_CNT)] for k in range(LINE_CNT)]
    last_data = [[['' for i in range(FLOWER_CNT)] for j in range(TUFT_CNT)] for k in range(LINE_CNT)]
    line = 1
    tuft = 1

    def app_close(self, instace):
        print('app_close')
        sys.exit()

    def disp_change(self, instance):
        print('call disp change')
        if instance.id.split('_')[1] == '列':
            self.line = int(instance.id.split('_')[0])
            self.line_lbl.text = str(self.line) + '列目'
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
        # 新規作成
        self.make_btn_layout()

    def btn_test(self, instance):
        print('test')

    def make_btn_layout(self):
        print('make_btn_layout')
        print(self.line, self.tuft)

        for i in range(FLOWER_CNT):
            # 横並びのレイアウト表示
            boxlayout = BoxLayout(spacing=10, size_hint_y=None)
            # 1行ごとにボタンとラベルを表示
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['btn'])
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['lbl'])
            self.layout.add_widget(boxlayout)

    def make_dropdownlist(self, cnt, unit):
        print('make dropdown list')
        dropdown = DropDown()
        for index in range(cnt):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            print('make button %d %s' % (index + 1, unit))
            btn = Button(text='%d %s' % (index + 1, unit),
                         size_hint_y=None, height=44,
                         id=str(index + 1) + '_' + unit)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            # btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn.bind(on_press=self.disp_change)

            # then add the button inside the dropdown
            dropdown.add_widget(btn)
        return dropdown

    def make_actionbar(self):
        self.pupupview = SaveDialog('保存ダイアログ', '保存しますか?',
                                    (WINDOW_WIDTH/2, WINDOW_HEIGHT/4),
                                    self.obj_list)
        actionview = ActionView()
        # actionview.use_separator = True
        ap = ActionPrevious(title='Tool Bar', with_previous=False)
        actionview.add_widget(ap)

        self.line_lbl = ActionButton(text=str(self.line) + '列目')
        self.line_lbl.bind(on_press=self.btn_test)
        actionview.add_widget(self.line_lbl)

        self.tuft_lbl = ActionButton(text=str(self.tuft) + '株目')
        actionview.add_widget(self.tuft_lbl)

        """
        self.null_btn2 = ActionButton(text='')
        actionview.add_widget(self.null_btn2)
        self.null_btn3 = ActionButton(text='')
        actionview.add_widget(self.null_btn3)
        """

        self.abtn1 = ActionButton(text='保存')
        self.abtn1.bind(on_press=self.pupupview.popup_open)
        actionview.add_widget(self.abtn1)

        """
        self.null_btn4 = ActionButton(text='')
        actionview.add_widget(self.null_btn4)
        """

        self.abtn2 = ActionButton(text="列変更")
        self.line_dropdown = self.make_dropdownlist(LINE_CNT, '列')
        self.abtn2.bind(on_press=self.line_dropdown.open)
        actionview.add_widget(self.abtn2)

        self.abtn3 = ActionButton(text="株変更")
        self.tufu_dropdown = self.make_dropdownlist(TUFT_CNT, '株')
        self.abtn3.bind(on_press=self.tufu_dropdown.open)
        actionview.add_widget(self.abtn3)

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
            if not os.path.isfile('C:/Users/yuuma_000/' + file_name):
                d = d - datetime.timedelta(days=1)
                file_name = str(d)[0:10] + '.csv'
            else:
                isFile = True
                break
        # ファイルがある場合は読み込み
        if isFile:
            with open('C:/Users/yuuma_000/' + file_name, 'r') as fp:
                r_txt = fp.read()
            for i, stat in enumerate(r_txt.split(',')[1:]):
                load_line = int(i / (TUFT_CNT * FLOWER_CNT) % LINE_CNT)
                load_tuft = int(i / (FLOWER_CNT) % TUFT_CNT)
                load_flower = int(i % FLOWER_CNT)
                if i < 10:
                    print(stat)
                    print(i, load_line, load_tuft)
                self.last_data[load_line][load_tuft][load_flower] = stat
            print(self.last_data[0][0])

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
        # いくつかわからないのでとりあえず定数だけボタン作成
        for j in range(LINE_CNT):
            for k in range(TUFT_CNT):
                for i in range(FLOWER_CNT):
                    # ボタンにidを割り当てる
                    btn = Button(text=str(i + 1) + '花株', font_size=70,
                                 size_hint_y=None, height=100, id='b_' + str(i + 1))
                    txt = self.last_data[j][k][i]
                    text = Label(text=txt,
                                 font_size=70, color=DEFAULT_COLOR,
                                 outline_color=RED, shorten_from='center',
                                 id='l_' + str(i + 1))

                    # ボタン押下時の関数を割り当てる
                    btn.bind(on_press=self.change_state)
                    self.obj_list[j][k].append({'btn': btn, 'lbl': text})

        for i in range(FLOWER_CNT):
            # 横並びのレイアウト表示
            boxlayout = BoxLayout(spacing=10, size_hint_y=None,
                                  id='box')
            # 1行ごとにボタンとラベルを表示
            print(self.obj_list[self.line - 1][self.tuft - 1][i]['btn'])
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['btn'])
            boxlayout.add_widget(self.obj_list[self.line - 1][self.tuft - 1][i]['lbl'])
            self.layout.add_widget(boxlayout)


#        self.make_btn_layout()

        # スクロールビューの作成
        root = ScrollView(size_hint=(1, None),
                          size=(Window.width, Window.height - 60))
        root.add_widget(self.layout)
        self.mainlayout.add_widget(root)
        return self.mainlayout

if __name__ == '__main__':
    ScrollApp().run()
