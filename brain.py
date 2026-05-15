import easyocr
import numpy as np
import cv2
from multiprocessing import shared_memory
import re
from googletrans import Translator
import sys
import os
import subprocess
import time

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


eye_exe = get_resource_path("TranslationEye.exe")

eye_proc = subprocess.Popen([eye_exe], creationflags=0x08000000)

print("Waiting for Eye to initialize Shared Memory...")
time.sleep(2) 

reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
translator = Translator()
translation_cache = {}

def run_brain():
    shm = None
    try: 
        
        shm = shared_memory.SharedMemory(name="Local\\MandarinCaptureBuffer")
        frame_buffer = np.ndarray((1080, 1920, 4), dtype=np.uint8, buffer=shm.buf)

        print("Brain Online. Press 'q' in the window to exit.")

        while True:
            
            img_rgba = frame_buffer.copy()
            img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)

            results = reader.readtext(img_rgb, detail=1, paragraph=True)

            for (bbox, text) in results:
                if re.search(r'[\u4e00-\u9fff]', text):
                    if text in translation_cache:
                        translated_text = translation_cache[text]
                    else:
                        try:
                            translation = translator.translate(text, src='zh-cn', dest='en')
                            translated_text = translation.text
                            translation_cache[text] = translated_text
                        except:
                            translated_text = "[Translation Timeout]"

                    top_left = tuple(map(int, bbox[0]))
                    cv2.putText(img_rgb, translated_text, (top_left[0], top_left[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 128), 2)
                
                cv2.rectangle(img_rgb, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 1)

            cv2.imshow("Universal Brain View", cv2.resize(img_rgb, (960, 540)))
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                # create folder 
                if not os.path.exists("Screenshots"):
                    os.makedirs("Screenshots")
        
                # make filename based on current time
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"Screenshots/Baidu_Apply_{timestamp}.png"
    
                # save frame
                cv2.imwrite(filename, img_rgb)
                print(f"Captured: {filename}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if shm:
            shm.close()
        cv2.destroyAllWindows()
        eye_proc.terminate()

if __name__ == "__main__":
    run_brain()