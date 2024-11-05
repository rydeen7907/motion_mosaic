
人間全身にモザイクかけるやつ

Python3.12.4で作成

(Pytorch：Python3.13非対応)

YOLOv5：モザイク処理するためインストール必須(v5でなくてもいいかも…)

場合によってはNVIDIAのcudaが必要

参考処理時間：PCのスペックにもよるが60秒のmp4動画で約60分

・元画像の解像度が高いほどモザイクがかかりやすい傾向にある

・フォルダ単位(要追加)での処理になるため

  inputフォルダには加工前の動画は少なめに…

・モザイク処理の対象となるモノ

  ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
