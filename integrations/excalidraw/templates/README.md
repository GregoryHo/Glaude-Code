# Excalidraw Templates

JSON templates for common diagram types.

## Available Templates

### architecture.json
System architecture diagram template with components for:
- Frontend applications
- Backend services
- Databases
- External APIs
- Message queues

**Use for**: Microservices, system design, infrastructure diagrams

### mindmap.json
Mind map template with:
- Central idea node
- Branch nodes
- Leaf nodes
- Connectors

**Use for**: Brainstorming, concept maps, hierarchical structures

### uml-class.json
UML class diagram template with:
- Class boxes
- Properties and methods
- Inheritance relationships
- Associations

**Use for**: Object-oriented design, class hierarchies, data models

## Using Templates

### Method 1: Copy and Edit

```bash
# Copy template
cp templates/architecture.json my-diagram.excalidraw

# Open and edit with Excalidraw
open my-diagram.excalidraw
```

### Method 2: Modify with Claude Code

```bash
# Read template
Read integrations/excalidraw/templates/architecture.json

# Ask Claude to modify for your needs
# "Create an architecture diagram with these components: ..."

# Claude writes modified JSON
Write my-architecture.excalidraw '{...modified JSON...}'

# Open in Excalidraw
open my-architecture.excalidraw
```

## Customizing Templates

### Element Structure

Each element in the `elements` array has this structure:

```json
{
  "id": "unique-id",
  "type": "rectangle|ellipse|diamond|arrow|text|line",
  "x": 100,          // X coordinate
  "y": 100,          // Y coordinate
  "width": 200,      // Width
  "height": 100,     // Height
  "angle": 0,        // Rotation angle
  "strokeColor": "#000000",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",  // hachure, cross-hatch, solid
  "strokeWidth": 1,
  "strokeStyle": "solid",  // solid, dashed, dotted
  "roughness": 1,    // 0 = sharp, 2 = very rough
  "opacity": 100,
  "text": "Label"    // For text elements
}
```

### Common Element Types

#### Rectangle (Box)
```json
{
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100
}
```

#### Ellipse (Circle/Oval)
```json
{
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 150
}
```

#### Arrow (Connector)
```json
{
  "type": "arrow",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [200, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

#### Text
```json
{
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 25,
  "text": "Your text here",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center"
}
```

### Color Palette

Common colors:
- Black: `#000000`
- White: `#ffffff`
- Red: `#fa5252`
- Green: `#12b886`
- Blue: `#228be6`
- Yellow: `#fab005`
- Orange: `#fd7e14`
- Purple: `#9775fa`
- Gray: `#495057`

### Layout Tips

1. **Grid Alignment**: Use multiples of 20 for x/y coordinates
2. **Spacing**: Leave ~100px between major components
3. **Text Size**: Use 16-20px for labels, 24-32px for titles
4. **Roughness**: Keep at 1 for most diagrams (hand-drawn style)

## Creating New Templates

1. **Create a basic diagram in Excalidraw**
2. **Export as .excalidraw file**
3. **Clean up the JSON**:
   - Remove `fileId` references
   - Simplify element IDs
   - Add comments (for documentation)
4. **Test the template**
5. **Add to this directory**

## Template Variables

When asking Claude to modify templates, you can use placeholders:

```json
{
  "text": "{{COMPONENT_NAME}}",
  "x": "{{X_POSITION}}",
  "y": "{{Y_POSITION}}"
}
```

Claude can replace these with actual values.

## Examples

### Example 1: Add Component to Architecture

```
User: "Add a Redis cache component between API and Database"

Claude:
1. Reads architecture.json
2. Adds new rectangle element for Redis
3. Adds connectors (arrows)
4. Positions between API and DB
5. Writes modified JSON
```

### Example 2: Expand Mind Map

```
User: "Add these branches: Research, Implementation, Testing"

Claude:
1. Reads mindmap.json
2. Adds 3 new branch nodes
3. Connects to central node
4. Writes modified JSON
```

### Example 3: Add UML Class

```
User: "Add a User class with name, email properties and login() method"

Claude:
1. Reads uml-class.json
2. Creates class box
3. Adds property and method text elements
4. Positions appropriately
5. Writes modified JSON
```

## Validation

After modifying a template, validate the JSON:

```bash
# Using Python
python3 -m json.tool my-diagram.excalidraw

# Using jq
jq . my-diagram.excalidraw

# Using Node
node -e "JSON.parse(require('fs').readFileSync('my-diagram.excalidraw'))"
```

## See Also

- [Excalidraw JSON Schema](https://docs.excalidraw.com/docs/codebase/json-schema)
- [Excalidraw Element Types](https://github.com/excalidraw/excalidraw/blob/master/src/element/types.ts)
- [Main README](../README.md)
