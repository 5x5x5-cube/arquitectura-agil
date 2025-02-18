# Monorepo Flask

Este es un monorepo que contiene múltiples aplicaciones Flask.

## Estructura

```
.
├── apps/
│   ├── gateway/
│   │   ├── app.py
│   │   └── requirements.txt
│   └── ...
├── .gitignore
└── README.md
```

## Configuración

Cada aplicación tiene sus propias dependencias y puede configurarse de forma independiente.

Para ejecutar una aplicación:

1. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   cd apps/gateway
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

## Agregar Nuevas Aplicaciones

Para agregar una nueva aplicación:

1. Crear un nuevo directorio dentro de `apps/`
2. Agregar el código de la aplicación Flask
3. Crear un archivo requirements.txt para las dependencias de la aplicación

## Guías de Desarrollo

- Cada aplicación gestiona sus propias dependencias mediante requirements.txt
- Seguir las guías de estilo PEP 8
- Escribir pruebas para las nuevas funcionalidades
