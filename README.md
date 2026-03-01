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

## Ejecución local

Puedes abrir `index.html` directamente en el navegador o levantar un servidor estático:

```bash
python3 -m http.server 8000
```

Luego visita `http://localhost:8000`.

## Roadmap recomendado (siguiente fase)

1. Autenticación y perfiles de usuario.
2. API de alimentos real (base nutricional completa).
3. Sincronización real con HealthKit/Google Fit (OAuth + permisos).
4. Pasarela de pago productiva (Stripe subscriptions).
5. Motor de recomendaciones con IA y seguimiento de adherencia.
