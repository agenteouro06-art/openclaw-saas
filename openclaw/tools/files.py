def save_file(name, content):
    with open(name, "w") as f:
        f.write(content)
    return "Archivo guardado"
