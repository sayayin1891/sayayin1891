# NutriSync Pro (prototipo)

Aplicación web estilo **Fitia** para personalizar planes nutricionales por tipo de cuerpo, estilo de alimentación y nivel de suscripción.

## Funcionalidades implementadas

- Selección de somatotipo: **mesomorfo**, **endomorfo** y **ectomorfo**.
- Recomendaciones dinámicas de calorías y macronutrientes según tipo de cuerpo.
- Menús ejemplo por enfoque nutricional:
  - Keto
  - Vegano
  - Proteico
- Constructor básico de menú (selección de alimentos y total de calorías).
- Bloques funcionales para:
  - Integración con **Apple Watch / HealthKit**.
  - Integración con **smartwatch Android / Google Fit**.
- Comparativa de planes:
  - **Free** con funcionalidades básicas.
  - **Premium** con funcionalidades avanzadas.
- Sección de benchmark con apps similares (Fitia, MyFitnessPal, Yazio).
- Medios de pago sugeridos: tarjeta (Stripe), Apple Pay, Google Pay, PayPal.

## Estructura

- `index.html`: interfaz principal.
- `styles.css`: estilos visuales responsivos.
- `app.js`: lógica de selección de cuerpo, plan y armado de menú.
- `.github/workflows/deploy-pages.yml`: despliegue automático a GitHub Pages.

## Cómo visualizar la app

### Opción 1: Local (rápido)

```bash
python3 -m http.server 8000
```

Luego abre:

- `http://localhost:8000`
- o `http://127.0.0.1:8000`

### Opción 2: Publicada con GitHub Pages

Este repositorio ya incluye workflow de despliegue automático para Pages.

1. Ve a **Settings → Pages** del repositorio.
2. En **Source**, selecciona **GitHub Actions**.
3. Haz push a tu rama principal (`main`, `master` o `work`) o ejecuta manualmente el workflow **Deploy static app to GitHub Pages**.
4. GitHub publicará la app y te entregará una URL como:
   - `https://<tu-usuario>.github.io/<tu-repo>/`

## Solución al problema de visualización

Si no podías ver la app, normalmente era por uno de estos motivos:

- Abrir el HTML desde GitHub web **no ejecuta** la app como sitio.
- No había un despliegue automático configurado para Pages.

Con este cambio:

- Puedes verla localmente con servidor estático.
- Puedes verla online mediante GitHub Pages con deploy automático.

## Roadmap recomendado (siguiente fase)

1. Autenticación y perfiles de usuario.
2. API de alimentos real (base nutricional completa).
3. Sincronización real con HealthKit/Google Fit (OAuth + permisos).
4. Pasarela de pago productiva (Stripe subscriptions).
5. Motor de recomendaciones con IA y seguimiento de adherencia.
