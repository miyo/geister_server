# geister_server

Geister用のゲームサーバ(作りかけ)．

## 動作概要(仮)
- 二つのクライアントとWebSocketで通信し，Geisterを進行する

## 盤面(仮)
        0 1 2 3 4 5
      0   h g f e
      1   d c b a
      2
      3
      4   A B C D
      5   E F G H
- サーバ側では表示のy=0の側を先手番の陣，y=5の側を後手番の陣とする
- プレーヤーは自分が先手なのか後手なのかによらず，y=5の側が自陣であるとする

## ゲームの進行概要(仮)
- 2つのプレーヤインスタンス(それぞれ8個のコマを持つ)を生成してクライアントからの通信を待つ
- クライアントに赤オバケを4つセットしてもらう．("ABCD"などのコマンドを送ってもらう)
- 先手にコマをうたせ，結果の盤面を両者に送信
 - {'a':(1,1), 'b':(2,1), ..., 'A':(1,4), 'B'(2,4),...}みたいに，コマと座標のペア
 - 相手のコマは小文字
 - 取られたコマは(-1,-1)
 - 自分の手番によらず同じ方向(5の側が自陣，0の側が相手陣)


