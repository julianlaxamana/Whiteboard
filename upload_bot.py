import os, time, cv2

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Website
CHAT_URL    = "https://chat.openai.com/chat"
PROMPT_TEXT = "Convert this image into a Studio Ghibli style illustration"

# Chrome Port
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
driver.get(CHAT_URL)

# wait until the upload input is ready
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
)

def capture_and_upload():
    # 1) Warm up & snapshot
    cam = cv2.VideoCapture(0)
    time.sleep(1)            # let the camera adjust
    for _ in range(3): cam.read()
    ok, frame = cam.read()
    cam.release()
    if not ok:
        raise RuntimeError("Camera read failed")
    shot_path = f"shot_{int(time.time())}.png"
    cv2.imwrite(shot_path, frame)
    print(" Captured:", shot_path)

    # 2) Upload the image to GPT
    uploader = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    uploader.send_keys(os.path.abspath(shot_path))
    time.sleep(2)            # wait for ChatGPT to register the file

    # 3) Make new chat box
    boxes = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
    chat_box = boxes[-1]
    chat_box.click()
    chat_box.send_keys(PROMPT_TEXT)

    # 4) Click the hit ENTER
    try:
        send_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']"))
        )
        send_btn.click()
        print(" Prompt sent via button.")

        time.sleep(90)            # wait for ChatGPT to register the file
        print("Wait")
        img_element = WebDriverWait(driver, 100000000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt=\"Generated image\"]"))
        )
        img_url = img_element.get_attribute("src")

        # Download the image using requests
        img_data = requests.get(img_url).content
        print(img_data)
        with open("downloaded_image.jpg", "wb") as f:
            f.write(img_data)

        print("Image Written")
    except Exception:
        chat_box.send_keys(Keys.ENTER)
        print(" Prompt sent via ENTER key.")

if __name__ == "__main__":
    print("Warming up for 30 s…")
    try:
        capture_and_upload()
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        driver.quit()


