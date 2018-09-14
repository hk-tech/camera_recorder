import argparse
import cv2
import datetime
import os
 
def set_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('device_id', type=int, help="通常は、 0: 内蔵カメラ, 1: USBカメラ")
    parser.add_argument('limit', type=int, help="撮影フレーム数")
    parser.add_argument('-f', '--fps', default=30, help="撮影FPS")
    parser.add_argument(‘-o', '--output_directory', help="出力先ディレクトリ")
    parser.add_argument('-p', '--preview', type=int, default=1, help="プレビュー画面の表示有無 0：表示しない 1:表示する(デフォルト)")
    return parser.parse_args()
 
def get_outputpath(output_directory):
    now = datetime.datetime.now()
    file_name = '{}.avi'.format(now.strftime('%Y%m%d_%H%M%S'))
    if output_directory is None:
        output_path = file_name
    else:
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, file_name)
    return output_path
 
def set_camera(device_id, fps):
    fps = int(fps)
    camera = cv2.VideoCapture(device_id)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, fps)
 
    if camera is None:
        raise Exception("Camera not found. Check device id.")
    return camera
 
def capture(camera, output_filepath, show_preview, limit = None):
    frame_number = 0
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    ret, frame = camera.read()
 
    fps = camera.get(cv2.CAP_PROP_FPS)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    writer = cv2.VideoWriter(output_filepath, fourcc, fps, (int(width), int(height)))
 
    while(ret):
        frame_number += 1
        writer.write(frame)
        if show_preview:
            cv2.imshow("preview", frame)
        if cv2.waitKey(int(1 / fps * 1000)) == 27: # ESC Key
            break
        if limit is not None and frame_number >= limit:
            break
        ret, frame = camera.read()
 
if __name__ == '__main__':
    args = set_arguments()
    output_path = get_outputpath(args.output_directory)
    camera = set_camera(args.device_id, args.fps)
    capture(camera, output_path, args.preview, args.limit)
