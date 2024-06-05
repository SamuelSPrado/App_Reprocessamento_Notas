from datetime import datetime
import json

def logger(message, log_file="registros_erro.txt"):
    erro = {
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    with open(log_file, "a") as file:
        file.write(json.dumps(erro, indent=4) + "\n")