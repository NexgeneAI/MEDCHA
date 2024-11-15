from dotenv import load_dotenv

load_dotenv()

from openCHA import openCHA

cha = openCHA(verbose=True)
cha.run_with_interface()
