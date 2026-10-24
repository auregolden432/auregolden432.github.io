# 🧘 Meditaciones · cómo publicar una nueva

La página pública es **auregolden432.com/meditaciones.html**. Se rellena sola a partir de `meditaciones.json`. Para publicar una meditación solo hacen falta dos pasos.

## 1. Sube el audio

1. En GitHub, entra en la carpeta `meditaciones/audio/`.
2. Pulsa **Add file → Upload files**, arrastra el archivo y pulsa **Commit changes**.

Recomendaciones para el archivo:
- Formato **MP3** a 128–192 kbps. Una meditación de 20 minutos ocupa unos 20–30 MB. GitHub no admite archivos de más de 100 MB.
- Nombre **sin espacios, tildes ni ñ**, por ejemplo `calma-interior.mp3`.

## 2. Actívala en `meditaciones.json`

1. Abre `meditaciones/meditaciones.json` y pulsa el lápiz ✏️.
2. Busca la meditación y rellena `"archivo"` con la ruta del audio. Rellena también `"fecha"` con el formato año-mes-día:

```json
"archivo": "audio/calma-interior.mp3",
"fecha": "2026-11-02"
```

3. Pulsa **Commit changes**. En uno o dos minutos aparecerá con su reproductor. Mientras `"archivo"` esté vacío, la tarjeta muestra **Próximamente**.

## Añadir una meditación nueva

Copia un bloque completo `{ ... }` y pégalo después del último. Pon una **coma** entre bloques y ninguna después del último:

```json
  {
    "titulo": "Nombre de la meditación",
    "intencion": "Calma",
    "descripcion": "Una o dos frases sobre la práctica.",
    "duracion": "15 min",
    "nivel": "Principiante",
    "archivo": "audio/nombre-del-archivo.mp3",
    "fecha": "2026-11-15"
  }
```

- `intencion` crea los botones de filtro de la página. Si usas una intención nueva, aparece un botón nuevo.
- Las meditaciones con audio salen primero, y las más recientes arriba.

> Si después de guardar la página sale vacía, casi siempre falta o sobra una coma en el JSON. Puedes pegar el contenido en jsonlint.com para revisarlo.
