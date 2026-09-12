# OLEANDER 3D Architecture Blueprint

## Purpose

OLEANDER 3D is not a Blender extension layer. It is a design operating system built on Blender Runtime, where geometry, intent, validation, evidence, manufacturing and presentation are connected through a persistent design graph.

## Reference Systems Absorbed

- Autodesk Alias: Class-A surface quality, reflection analysis, curvature continuity.
- CATIA / 3DEXPERIENCE: knowledge-based engineering, rules, parameters and product structure.
- Rhino Grasshopper: parametric relations and procedural logic.
- Revit: semantic objects and information-rich components.
- Siemens NX / Creo: engineering validation, assembly and manufacturing awareness.
- Git: version history, change traceability and reversible decisions.

OLEANDER combines these mechanisms but extends them with design intent, evidence and AI reasoning.

## Core Architecture

```
AI Design Reasoning Layer
        |
Validation + Evidence Kernel
        |
Semantic + Relation Kernel
        |
Geometry Kernel
        |
Blender Runtime
```

## Kernel Definitions

### 1. OLE Object System

Every design element is a semantic object rather than an isolated mesh.

Required fields:

- Object ID
- Semantic Type
- Design Intent
- Parameters
- Constraints
- Geometry Source
- Material
- Manufacturing Method
- Evidence
- Validation State
- Version History

### 2. Geometry Kernel

Responsible for:

- procedural geometry
- Class-A surfaces
- curvature continuity
- NURBS / mesh / CAD interoperability
- source-controlled rebuild

The Surface System belongs here.

### 3. Relation Kernel

Replaces simple parameter links with design relationships.

Example:

```
Ergonomic Requirement
        ↓
Grip Diameter
        ↓
Shell Geometry
        ↓
Manufacturing Constraint
```

### 4. Semantic Kernel

Blender objects become meaningful design entities.

Example:

```
Cube001
```

becomes:

```
OLE_PANEL_FRONT_COVER_001
Exterior Housing Component
Injection Molded ABS
```

### 5. Validation Kernel

Provides automated review:

- geometry integrity
- dependency conflicts
- manufacturing risks
- surface quality
- export readiness

Machine PASS does not equal design approval. Human visual review remains separate.

### 6. Material Intelligence Kernel

Connects materials with:

- physical properties
- process limitations
- cost
- appearance
- sustainability

### 7. Assembly Kernel

Supports:

- components
- assemblies
- dependencies
- BOM
- lifecycle states

### 8. Manufacturing Kernel

Provides early DFM feedback:

- injection molding
- CNC
- sheet metal
- additive manufacturing

### 9. Documentation Kernel

Generates from source:

- drawings
- exploded views
- BOM
- technical documents
- web presentations

### 10. AI Design Reasoning Layer

AI acts as reviewer and reasoning assistant, not only a generator.

Expected outputs:

- defect diagnosis
- design alternatives
- constraint conflicts
- evidence-based recommendations

## Development Principle

OLEANDER follows:

```
Intent
 ↓
Relation
 ↓
Source Geometry
 ↓
Derived Geometry
 ↓
Validation
 ↓
Evidence Receipt
```

No mesh patching replaces source logic.

No visual result is accepted without traceable source state.

## Current Priority

1. Complete Surface System and Class-A validation.
2. Establish OLE Object Registry.
3. Build Relation Graph foundation.
4. Connect Validation Receipts.
5. Introduce AI Design Reasoning layer.
