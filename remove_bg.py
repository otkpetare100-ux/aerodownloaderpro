from PIL import Image

def remove_background(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Check if the pixel is close to white
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0)) # Make transparent
        else:
            # If the pixel is very dark (like the "DOWNLOADER PRO" text), make it white 
            # so it contrasts with the app's dark theme
            if item[0] < 80 and item[1] < 80 and item[2] < 80:
                newData.append((230, 230, 230, item[3]))
            else:
                newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    input_file = r"C:\Users\Nanami\Downloads\Logo Aero Dowloader Pro.png"
    output_file = r"C:\Users\Nanami\Downloads\Logo_Aero_Transparent.png"
    remove_background(input_file, output_file)
    print("Background removed successfully.")
