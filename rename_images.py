import os

for fis in os.listdir('images'):
    fn, ext = os.path.splitext(fis)
    new_fn = fn.split('_')[0] + ext
    try:
        os.rename(os.path.join("images", fis), os.path.join("images", new_fn))
    except:
        pass
    

