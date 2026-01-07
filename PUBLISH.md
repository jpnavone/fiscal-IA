# Cómo publicar este repositorio en GitHub

Este proyecto ya tiene un repositorio Git local inicializado. Sigue estos pasos para subirlo a GitHub.

## 1. Crear un repositorio en GitHub
1. Ve a [github.com/new](https://github.com/new).
2. Nombre del repositorio: `judicial-voice-2-text` (o el que prefieras).
3. **No** inicialices el reenpositorio con README, .gitignore o licencia (ya los tenemos).
4. Haz clic en "Create repository".

## 2. Conectar tu repositorio local
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
# Reemplaza <TU_USUARIO> con tu nombre de usuario de GitHub
git remote add origin https://github.com/<TU_USUARIO>/judicial-voice-2-text.git
git branch -M main
git push -u origin main
```

> [!IMPORTANT]
> Si ves un error de "Authentication failed", es porque GitHub ya no acepta contraseñas. Necesitas usar un **Personal Access Token (PAT)**.
> 1. Ve a GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic).
> 2. Genera un nuevo token con permisos de `repo`.
> 3. Cuando la terminal te pida contraseña, pega ese token.

## 3. Verificar
Visita la URL de tu repositorio en GitHub para ver tus archivos publicados.
