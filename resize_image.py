from PIL import Image
import os

required_width = None #declaring the variable so that it's accessible within the whole global scope

# check if folder or filename exists
def check_path(value, check_file_or_folder):
    #check if the value is folder
    if check_file_or_folder == "folder":
        return os.path.isdir(value)
    #check if the value is path to file
    if check_file_or_folder == "file":
        return os.path.isfile(value)
    return False


# resize image function
def resizeImage(image_path):
    try:
        img = Image.open(image_path)  # PIL automatically handles binary mode
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return
    except Exception as e: # Catch other potential PIL errors
        print(f"Error opening image: {e}")
        return

    if required_width >= img.width: # corrected comparison
        print(f"THE REQUIRED WIDTH TO RESIZE OF {image_path} IS LOWER THAN THE ACTUAL WIDTH OF THE CURRENT FILE!!!")
        return

    w_percent = required_width / float(img.width)
    new_height = int(img.height * w_percent)

    path_to_file = os.path.dirname(image_path) # Get path here
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()[1:] # remove the "." from the extention
    output_path = os.path.join(path_to_file, f"resized_{filename}") # save the file with same name and prefix "resized_"
    try:
        img = img.resize((required_width, new_height), Image.LANCZOS)
        img.save(output_path)
    except Exception as e:
        print(f"Error during resizing or saving: {e}")
        return

# iterate through folder and search for image files
def iterateFolder(path_to_folder):
    files_in_folder = os.listdir(path_to_folder)
    for file in files_in_folder:
        name, ext = os.path.splitext(file)
        ext = ext.lower()[1:] # remove the "." from the extention
        #if image file, then resize
        if ext in {"jpeg", "jpg", "png", "webp", "gif"}:
            resizeImage(os.path.join(path_to_folder, file))
       


multiple_or_single = input(f"To resize all image files in the folder, enter 'all', for single file, enter 'single': ").strip().lower()
if multiple_or_single not in ("all", "single"):
    print("Incorrect value entered!!! Only 'all' or 'single' must be entered.")
    exit()

# SINGLE FILE TO RESIZE REQUEST
if multiple_or_single == "single":
    img_to_resize = input("Enter the path and filename you want to resize: ")
    if not check_path(img_to_resize, 'file'):
        print("The entered file was not found!")
        exit()
    try:
        required_width = int(input("Enter the required width in pixels: ")) # convert to int immediately
    except ValueError:
        print("Invalid width input. You must enter a number!")
        exit()
    resizeImage(img_to_resize)    
    print("The image was resized and renamed to 'resized_ORIGINAL NAME'")  
       

# MULTIPLE FILES TO RESIZE REQUEST
if multiple_or_single == "all":
    folder_with_images = input('Enter the path to the folder where you want to resize all image files: ')
    if not check_path(folder_with_images, 'folder'):
        print("The entered directory was not found!")
        exit()
    try:
        required_width = int(input('Enter the required width in pixels: ')) # convert to int immediately
    except ValueError:
        print("Invalid width input. You must enter a number!")
        exit()
    iterateFolder(folder_with_images)  
    print("All images in the folder were resized and renamed to 'resized_ORIGINAL NAME'")  
