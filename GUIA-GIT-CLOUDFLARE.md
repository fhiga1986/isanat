# Guía: de `D:\isanatgit` a isanat.pe

Paso a paso para trabajar el sitio desde tu PC con Git y publicarlo en Cloudflare Pages.
Los comandos son para **PowerShell** en Windows (el que abres con `Win + X` →
*Terminal* o *Windows PowerShell*). Funcionan igual en Git Bash.

---

## Paso 0 — Instalar Git

Comprueba si ya lo tienes:

```powershell
git --version
```

Si responde algo como `git version 2.x.x`, sigue al paso 1. Si dice que no
reconoce el comando, descárgalo de **https://git-scm.com/download/win** e instálalo
con todas las opciones por defecto. Trae incluido el *Git Credential Manager*, que
es lo que después te va a dejar entrar a GitHub desde el navegador sin andar
creando tokens a mano.

Cierra y vuelve a abrir PowerShell después de instalarlo.

---

## Paso 1 — Dejar los archivos en `D:\isanatgit`

Descomprime `isanat-web.zip`. Adentro vas a ver una carpeta `isanat`.

⚠️ **Copia el contenido de esa carpeta, no la carpeta misma.** Esto es lo que más
se equivoca y rompe el deploy.

Tiene que quedar así:

```
D:\isanatgit\
├── index.html          ← este archivo va en la raíz
├── 404.html
├── README.md
├── GUIA-GIT-CLOUDFLARE.md
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── _headers
├── favicon.ico
├── .gitignore
├── .gitattributes
├── fonts\
└── img\
```

Y **no** así: `D:\isanatgit\isanat\index.html`.

Verifícalo:

```powershell
cd D:\isanatgit
dir
```

Debes ver `index.html` en esa lista. Los archivos `.gitignore` y `.gitattributes`
no aparecen en el Explorador de Windows porque empiezan con punto; es normal, Git
sí los ve. Para verlos en la terminal: `dir -Force`.

---

## Paso 2 — Configurar Git (una sola vez en tu PC)

```powershell
git config --global user.name "Fernando"
git config --global user.email "kondorflowhg@gmail.com"
git config --global init.defaultBranch main
```

> **Sobre el correo:** el email que pongas queda escrito dentro de cada commit y es
> visible para cualquiera que vea el repo. Si prefieres no exponerlo, GitHub te da
> una dirección alternativa en *Settings → Emails → Keep my email addresses private*
> (con el formato `12345678+usuario@users.noreply.github.com`). Usa esa en el
> `user.email` y listo.

---

## Paso 3 — Primer commit

```powershell
cd D:\isanatgit
git init
git add .
git status
```

`git status` te muestra todo lo que va a entrar al commit. Deberías ver los 24
archivos en verde. Si ves algo que no debería estar (carpetas del sistema, archivos
temporales), avísame antes de seguir.

```powershell
git commit -m "ISANAT: landing inicial con SEO tecnico y GA4"
```

Ya tienes control de versiones funcionando en local. Todavía no hay nada en internet.

---

## Paso 4 — Crear el repositorio en GitHub

En **https://github.com/new**:

| Campo | Qué poner |
|---|---|
| Repository name | `isanat` |
| Description | `Sitio web de ISANAT — Escuela de natación, La Molina` |
| Visibilidad | **Private** (puedes cambiarlo después; Cloudflare Pages funciona igual con repos privados en el plan gratuito) |
| Add a README file | ❌ **desmarcado** |
| Add .gitignore | ❌ **None** |
| Choose a license | ❌ **None** |

⚠️ Los tres últimos tienen que quedar vacíos. Si GitHub crea archivos, el repo
arranca con un historial distinto al tuyo y el primer `push` va a fallar con
`rejected — fetch first`. No es grave, pero te obliga a hacer un
`git pull --rebase` que a esta altura no necesitas.

Dale a *Create repository*.

---

## Paso 5 — Subir tu código

GitHub te muestra la URL del repo. Úsala aquí (reemplaza `TU-USUARIO`):

```powershell
git remote add origin https://github.com/TU-USUARIO/isanat.git
git branch -M main
git push -u origin main
```

En el primer `push` se abre una ventana del navegador para que entres a GitHub y
autorices. Aceptas, y Windows guarda la credencial: no te la vuelve a pedir nunca
más. GitHub **no** acepta tu contraseña normal por terminal, así que si te aparece
un prompt pidiendo `Password`, cancela y deja que se abra el navegador.

Recarga la página del repo: tus archivos ya están ahí.

---

## Paso 6 — Conectar Cloudflare Pages

1. Crea la cuenta en **https://dash.cloudflare.com/sign-up** (gratis, pide correo
   y contraseña; verifica el correo antes de seguir).
2. En el menú lateral: **Compute (Workers & Pages)** → **Create** → pestaña
   **Pages** → **Connect to Git**.
3. Autoriza GitHub. Te va a pedir a qué repositorios darle acceso: elige `isanat`
   (o todos, da igual).
4. Selecciona `isanat` de la lista y dale **Begin setup**.
5. En la pantalla de configuración, déjalo exactamente así:

   | Campo | Valor |
   |---|---|
   | Project name | `isanat` |
   | Production branch | `main` |
   | Framework preset | **None** |
   | Build command | *vacío* |
   | Build output directory | `/` |
   | Root directory | *vacío* |

   Si Cloudflare intenta adivinar un framework, ponlo en *None*. Este sitio no tiene
   build: son archivos estáticos que se sirven tal cual. El campo que más se
   equivoca la gente es **Build output directory**: tiene que ser `/`, porque el
   `index.html` está en la raíz del repo, no dentro de un `dist/` o `build/`.

6. **Save and Deploy**. En un minuto tienes una URL tipo `isanat.pages.dev`.

El archivo `_headers` del repo aplica solo: cache de un año para fuentes e imágenes
y los headers de seguridad. No tienes que tocar nada de eso en el panel.

Para conectar `isanat.pe` cuando termines de adquirirlo, los pasos están en el
`README.md`, sección 3. Ojo con uno en particular: el dominio tiene que pasar a usar
los **nameservers de Cloudflare**, que se cambian desde NIC.pe. No alcanza con crear
un registro apuntando desde allá.

---

## Paso 7 — El flujo del día a día

A partir de acá, cada vez que cambies algo:

```powershell
cd D:\isanatgit

# ... editas los archivos que sea ...

git status                 # qué cambió
git diff                   # exactamente qué línea cambió
git add .
git commit -m "Agrega horarios reales en la seccion Ubicacion"
git push
```

Y ya. Cloudflare detecta el push y republica solo, en unos 30 segundos. No hay que
subir nada por FTP ni entrar al panel.

**Sobre los mensajes de commit:** escribe qué cambiaste y por qué, no "cambios" ni
"update". Dentro de seis meses, cuando quieras encontrar cuándo se rompió algo, la
diferencia entre `git log` útil e inútil es esa.

```
✅ "Reemplaza coordenadas aproximadas por las del perfil verificado de Google"
✅ "Agrega precios de membresia confirmados por el cliente"
❌ "cambios"
❌ "asdasd"
```

---

## Paso 8 — Ramas: probar sin romper lo que está publicado

Cuando vayas a hacer un cambio grande (rediseñar una sección, agregar precios,
probar otro hero), no lo hagas directo sobre `main`. Crea una rama:

```powershell
git switch -c precios          # crea la rama y te mueve a ella

# ... editas ...

git add .
git commit -m "Agrega tabla de precios por programa"
git push -u origin precios
```

Cloudflare publica **esa rama en una URL de preview aparte**, con la forma
`precios.isanat.pages.dev`, sin tocar producción. La encuentras en el panel del
proyecto, en *Deployments*. Se la puedes pasar al cliente para que opine antes de
que sea definitivo.

Cuando esté aprobado, lo pasas a producción:

```powershell
git switch main
git merge precios
git push
git branch -d precios          # borra la rama local, ya no hace falta
```

Si prefieres hacerlo desde la web, GitHub te ofrece abrir un *Pull Request* apenas
subes la rama. Es el mismo resultado, con la ventaja de que queda registrado el
cambio completo en un solo lugar.

---

## Paso 9 — Marcar versiones

Cuando publiques algo que quieras poder señalar después ("la versión que vio el
cliente en octubre"):

```powershell
git tag -a v1.0 -m "Primera version publicada"
git push origin v1.0
```

`git tag` te lista todas. Para volver a mirar cómo estaba el sitio en esa versión:
`git checkout v1.0` (y `git switch main` para volver al presente).

---

## Comandos de rescate

| Situación | Comando |
|---|---|
| Ver el historial | `git log --oneline -10` |
| Ver qué cambió en un commit | `git show <hash>` |
| Deshacer cambios de un archivo **no** commiteado | `git restore index.html` |
| Deshacer **todos** los cambios no commiteados | `git restore .` |
| Deshacer el último commit pero conservar los cambios *(solo si aún no hiciste push)* | `git reset --soft HEAD~1` |
| Deshacer un commit **ya subido** (crea uno nuevo que revierte; es lo seguro) | `git revert <hash>` |
| Editaste un archivo en github.com y ahora no te deja pushear | `git pull` y después `git push` |
| Ver en qué rama estás | `git branch` |

**Rollback en Cloudflare, sin tocar Git:** panel del proyecto → *Deployments* →
buscas un deploy anterior que funcionaba → menú `⋯` → *Rollback to this deployment*.
Vuelve a esa versión al instante. Útil si algo sale mal un viernes a las 7 de la tarde.

---

## Errores típicos y qué significan

| Mensaje | Qué pasó |
|---|---|
| `fatal: not a git repository` | No estás parado en `D:\isanatgit`. Haz `cd D:\isanatgit`. |
| `rejected — fetch first` | El repo de GitHub tiene commits que tú no tienes. `git pull --rebase` y vuelve a pushear. |
| `remote origin already exists` | Ya habías corrido `git remote add`. Usa `git remote set-url origin <URL>` para corregir la dirección. |
| `Support for password authentication was removed` | Estás intentando entrar con contraseña. Deja que se abra el navegador, o reinstala Git para Windows con el Credential Manager. |
| `nothing to commit, working tree clean` | No hay cambios sin guardar. Todo está commiteado. |
| En Cloudflare: 404 en la home | Los archivos quedaron dentro de una subcarpeta, o el *Build output directory* no es `/`. Revisa el paso 1 y el paso 6. |
| En Cloudflare: se ve el HTML sin estilos ni logo | Mismo problema de rutas: `img/` y `fonts/` tienen que estar al lado de `index.html`. |
| El dominio isanat.pe no resuelve tras horas | Los nameservers en NIC.pe todavía no propagaron, o quedó alguno viejo cargado. En `.pe` puede tardar hasta 24 h. |
