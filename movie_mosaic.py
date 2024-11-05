"""

動画の中の人間全身にモザイクをかける
・Python 3.12.4
  Python 3.13非対応(Pytorch)
・出力がmp4なため他形式はあらかじめ別手段で変換するか
  このコードで設定を書き換えるかをする
・60secのmp4で 処理約60分
・alpha値は max = 1.0

2024.10.10

"""

import glob
import torch
import cv2
import numpy as np
import os

# 学習モデル YOLOv5 を使用
model =torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
# 入力ディレクトリからファイルを読み込む
input_dir = 'c:/     /' # 任意のフォルダ
# 出力ディレクトリへファイルを書き出す 
output_dir = 'c:/     /' # 任意のフォルダ

# モザイク処理を適用する関数 mosaic を設定
def mosaic(img, alpha):
    w = img.shape[1]
    h = img.shape[0]

    # リサイズ後の幅と高さが少なくとも1ピクセル以上になるようにする
    # 0ピクセルになるとエラーで停止する
    w_resized = max(int(w * alpha), 1)
    h_resized = max(int(h * alpha), 1)

    img = cv2.resize(img, (w_resized, h_resized))
    img = cv2.resize(img, (w,h), interpolation=cv2.INTER_NEAREST)
    return img

def movie_mosaic(input_video, out_video): 
    # videoファイルを読み込み サイズなどを取得し出力
    video = cv2.VideoCapture(input_video)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (w,h)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # 出力動画は mp4 に指定
    writer = cv2.VideoWriter(out_video, fmt, float(frame_rate),(w,h))
    num = 0
    while(video.isOpened()):
        ret,frame = video.read() # 1フレーム単位で処理
        if ret == True:            
            results = model(frame)
            # results = model(frame, conf=0.25)  # 例: conf=0.25で信頼度閾値を指定

            # results から適切なデータ構造を取得
            detections = results.pandas().xyxy[0]

            # 検出結果が得られた場合のみ処理を行う
            if len(detections) > 0:
                for i in range(len(detections)):
                    # class が 0 (人間)の場合のみモザイク処理
                    # class の値を変更するとモザイク処理の対象も変わる
                    if detections.iloc[i]["class"] == 0:
                        ymin = int(detections.iloc[i]["ymin"])
                        ymax = int(detections.iloc[i]["ymax"])
                        xmin = int(detections.iloc[i]["xmin"])
                        xmax = int(detections.iloc[i]["xmax"]) 
                        # buffer = 5  # ピクセル単位で拡張する量
                        # ymin = max(int(detections.iloc[i]["ymin"]) - buffer, 0)
                        # ymax = min(int(detections.iloc[i]["ymax"]) + buffer, h)
                        # xmin = max(int(detections.iloc[i]["xmin"]) - buffer, 0)
                        # xmax = min(int(detections.iloc[i]["xmax"]) + buffer, w)
                        
                        # モザイク処理
                        frame[ymin:ymax,xmin:xmax] = mosaic(frame[ymin:ymax,xmin:xmax], alpha)                        
            
            writer.write(frame)
            print(input_video, num, frame_count) # ターミナルに処理状況が表示される仕組
            num += 1
        else:
            break
    
    # リソース解放
    writer.release()
    video.release()

if __name__ == '__main__':
    alpha = 0.05 # モザイクの粗さを調整(任意)
    files = glob.glob(input_dir + "*.mp4")
    for f in files:
        input_video = f
        out_video = output_dir+os.path.basename(f)
        movie_mosaic(input_video, out_video)