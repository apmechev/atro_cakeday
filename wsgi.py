import os
import sys
from logging import Formatter, FileHandler

APP_HOME = "/home/cakedays/astro_cakeday"

activate_this = os.path.join("/home/cakedays/astro_cakeday/astro_cakeday/bin/activate_this.py")
exec(open(activate_this).read(), {'__file__': activate_this})



sys.path.insert(0, APP_HOME)
os.chdir(APP_HOME)



from astro_cakeday import create_app 

app = create_app()

handler = FileHandler("app.log")
handler.setFormatter(Formatter("[%(asctime)s | %(levelname)s] %(message)s"))
app.logger.addHandler(handler)
application = app

