# 🧘 Meditaciones · cómo actualizar la página

La página pública es **auregolden432.com/meditaciones.html**. Se rellena sola a partir de `meditaciones.json`.

La idea: en la web solo hay **fragmentos cortos** (1–2 min) y botones que llevan a las versiones completas en las plataformas. Los audios completos **no** se suben aquí.

## 1. Sube un fragmento

1. Entra en la carpeta `meditaciones/audio/` → **Add file → Upload files** → arrastra el MP3 → **Commit changes**.
2. El fragmento debe ser un **MP3 de 1–2 minutos** a 128–192 kbps (pesa unos 2–3 MB). Ponle un nombre sin espacios, tildes ni ñ, por ejemplo `calma-interior-fragmento.mp3`.

## 2. Actívalo en `meditaciones.json`

Abre `meditaciones/meditaciones.json` → lápiz ✏️. Busca la meditación y rellena:

```json
"fragmento": "audio/calma-interior-fragmento.mp3",
"enlaces": {
  "spotify": "https://open.spotify.com/track/...",
  "youtube": "https://www.youtube.com/watch?v=...",
  "insight_timer": "",
  "apple_music": ""
},
"fecha": "2026-11-02"
```

- Los enlaces que dejes vacíos `""` no aparecen. Cada enlace tiene que empezar por `https://`.
- Mientras una meditación no tenga ni fragmento ni enlaces, su tarjeta muestra **Próximamente**.

Guarda con **Commit changes**. En uno o dos minutos se ve en la web.

## 3. Tus perfiles en las plataformas (una sola vez)

Al principio del archivo está el bloque `"plataformas"`. Pon ahí el enlace a **tu perfil o canal** en cada plataforma. Son los botones grandes de "Escucha las meditaciones completas":

```json
"plataformas": {
  "spotify": "https://open.spotify.com/artist/...",
  "youtube": "https://www.youtube.com/@...",
  "insight_timer": "",
  "apple_music": "",
  "amazon_music": ""
}
```

Mientras estén vacíos, la página dice "Muy pronto en Spotify, YouTube y más plataformas".

## Añadir una meditación nueva

Copia un bloque completo `{ ... }` de la lista `"meditaciones"` y pégalo después del último. Pon una **coma** entre bloques y ninguna después del último. Si usas una `intencion` nueva, aparece un botón de filtro nuevo.

> Si después de guardar la página sale vacía, casi siempre falta o sobra una coma. Pega el contenido en jsonlint.com para revisarlo.
