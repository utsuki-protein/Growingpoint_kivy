from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.properties import StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.actionbar import ActionBar, ActionItem, ActionButton, ActionView, ActionPrevious, ActionGroup
from kivy.uix.popup import Popup

from win32api import GetSystemMetrics
import datetime
import os

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
        for i in self.obj_list:
            w_txt = w_txt + i['lbl'].text + ','
        with open('C:/Users/yuuma_000/savedialog' + file_name, 'w') as fp:
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
    obj_list = []
    last_data = []

    def btn_test(self, instance):
        print('test')

    def make_actionbar(self):
        self.pupupview = SaveDialog('保存ダイアログ', '保存しますか?',
                                    (WINDOW_WIDTH/2, WINDOW_HEIGHT/4),
                                    self.obj_list)
        actionview = ActionView()
        actionview.use_separator = True
        ap = ActionPrevious(title='Action Bar', with_previous=False)
        actionview.add_widget(ap)
        self.abtn1 = ActionButton(text='列切り替え')
        self.abtn1.bind(on_press=)
        actionview.add_widget(self.abtn1)
        self.abtn2 = ActionButton(text="保存")
        self.abtn2.bind(on_press=self.pupupview.popup_open)
        actionview.add_widget(self.abtn2)

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
        if isFile:
            with open('C:/Users/yuuma_000/' + file_name, 'r') as fp:
                r_txt = fp.read()
        else:
            r_txt = ',' * 29

        for stat in r_txt.split(',')[1:]:
            self.last_data.append(stat)

    # テキストの状態を推移させる
    def change_state(self, src):
        # src.idに「id='b_' + str(i)」が来るので「_」で区切る
        idx = int(src.id.split('_')[1])
        # リストからIDを検索し、テキストラベルの状態を取得
        stat = self.obj_list[idx - 1]['lbl'].text

        # 見つからない場合、エラーになるのでexceptでキャッチしとく
        try:
            next_stat = state_list.index(stat) + 1
        except:
            print('error')

        # 状態が一周したら0に戻す
        if next_stat >= len(state_list):
            next_stat = 0
        # 状態を一つすすめた値をテキストラベルに書き込む
        self.obj_list[idx - 1]['lbl'].text = state_list[next_stat]

    # ソフト起動時(kivyのWindow作成時？)に呼ばれる関数
    def build(self):
        # load関数をコール
        self.load()
        # GridLayoutの作成
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(self.make_actionbar())
        # Gridlayoutに入れるボタンとラベルの作成
        # いくつかわからないのでとりあえず定数だけボタン作成
        for i in range(1, 30):
            # 横並びのレイアウト表示
            boxlayout = BoxLayout(spacing=10, size_hint_y=None)
            # ボタンにidを割り当てる
            btn = Button(text=str(i) + '列目', font_size=70,
                         size_hint_y=None, height=100, id='b_' + str(i))

            text = Label(text=self.last_data[i-1],
                         font_size=70, color=DEFAULT_COLOR,
                         outline_color=RED, shorten_from='center',
                         id='l_' + str(i))
            self.obj_list.append({'btn': btn, 'lbl': text})

            # ボタン押下時の関数を割り当てる
            btn.bind(on_press=self.change_state)
            # btn.bind(on_press=lambda x: self.change_state(btn.id, str(i)))

            # 1行ごとにボタンとラベルを表示
            boxlayout.add_widget(btn)
            boxlayout.add_widget(text)
            layout.add_widget(boxlayout)

        # スクロールビューの作成
        root = ScrollView(size_hint=(1, None),
                          size=(Window.width, Window.height))
        root.add_widget(layout)
        return root

if __name__ == '__main__':
    ScrollApp().run()
