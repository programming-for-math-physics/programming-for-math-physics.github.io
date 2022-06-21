(** md

# {C.inc_section}. Jupyter環境の基本

Jupyter環境は今まさに使っているもので, 様々なプログラミング言語をウェブブラウザを通して実行し, プログラム, その出力, このようなドキュメント, を一緒にして保存できる仕組み.

Jupyter is an environment you are just seeing now.  It allows you to execute various programming languages through the web browser and save programs, their outputs and documents like this together.

Jupyterでは以下のような四角を __セル__ と呼ぶ.

In Jupyter, we call a rectangle like below a __cell__.

 *)

(** empty-code *)

(** md

 * セルの上でマウスをクリックするとセルが「選択」され, 入力できる状態になる(その他にもキーボードの矢印キーで, 選択することもできる).
 * You can _select_ a cell by clicking the mouse on the cell and enter a program into it (you can also select a cell by arrow keys).

 * セルが選択された状態で`Shift + Enter` を入力する (`Shift`キーを押しながら`Enter`キーを押す)と, セルの中身が計算される (「計算する」=「式の値を規則に従って求める」ということなので, 「評価する」ということもある).
 * Press `Shift + Enter` (Hold the `Shift` key pressed and press the Enter key) on a selected cell to compute its contents (we also say "evaluate", as "compute" is to "find the value of the expression according to the rule").

 *)

(* execute this cell *)
1 + 2 * 3;;

(** md 

 * このようなテキストが表示されている部分もセルであり, クリックすることで編集可能になり, `Shift + Enter`で編集結果を表示できる.

 * Text areas such as this are also cells, which can be edited by clicking on them and can be displayed by `Shift + Enter`.

 *)

(** md

**このセルを編集して, 名前と学生証番号を書け.**

**Edit this cell and enter your name and student ID.**

 * 名前 Name : 
 * 学生証番号 Student ID : 

  *)

(** md

 * セルを編集したり実行したら**こまめに保存** (`Ctrl-S`) せよ
 * After you edit or execute a cell, **save it frequently** (by `Ctrl-S`)

  *)
