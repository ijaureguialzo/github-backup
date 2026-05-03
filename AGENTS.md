# AGENTS.md — Guía para agentes de IA

Este fichero describe el proyecto, su estructura, las convenciones de desarrollo y las instrucciones que deben seguir
los agentes de IA (GitHub Copilot, etc.) al trabajar en este repositorio.

## Descripción del proyecto

Utilidad de backup de los repositorios de GitHub.

## Instrucciones para agentes

- **Leer siempre el AGENTS.md** antes de empezar a trabajar en el proyecto.
- **No leer ni exponer el contenido** de ningún fichero del subdirectorio `private/` (credenciales, certificados,
  keystores, etc.). Tratar todos sus ficheros como de solo lectura y usarlos exclusivamente por su ruta.

## Convenciones de commits

> **Regla fundamental**: cada funcionalidad completada o corrección de bug debe tener su propio commit independiente. No
> agrupar cambios no relacionados en un mismo commit.

### Cuándo hacer commit

- Al completar una funcionalidad nueva (aunque sea parcial pero funcional).
- Al corregir un bug concreto.
- Al añadir o actualizar documentación relevante.
- **No** hacer commit de código roto o que no compila.

### Formato del mensaje de commit

Usar [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<scope>): <descripción breve en imperativo>
```

- **El mensaje debe escribirse en español.**
- Ejemplos de tipos: `feat`, `fix`, `docs`, `refactor`, `chore`.

### Trailer obligatorio

Todo commit creado por un agente de IA debe incluir el trailer con su información de co-autoría al final del mensaje.
