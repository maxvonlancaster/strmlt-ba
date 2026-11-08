# Business Requirement Ticket Generator 📋

A sophisticated Streamlit application that transforms unstructured business text into structured, analyzable requirement tickets using Natural Language Processing (NLP).

## Overview

This application analyzes plain English text submissions to:
- ✅ Determine if text represents a valid business requirement
- 🏷️ Extract key entities (stakeholder, action, object, priority, quality attributes)
- 🔍 Highlight important keywords and phrases
- 📊 Calculate confidence scores for requirement validity
- 🎫 Generate structured, exportable requirement tickets
- 📈 Visualize analysis results with interactive charts

## Features

### Text Analysis
- **Requirement Classification**: Intelligent heuristic-based classification to determine if text is a business requirement
- **Entity Extraction**: Extracts structured data including:
  - **Stakeholder**: Who needs it (user, admin, customer, organization, etc.)
  - **Action**: What to do (create, update, delete, manage, etc.)
  - **Object**: What to act upon (report, data, user, etc.)
  - **System**: Target system or component
  - **Quality Attributes**: Non-functional requirements (secure, scalable, reliable, etc.)
  - **Priority**: Urgency level (high, medium, low)
  - **Conditions**: When/if clauses
  - **Constraints**: Time and resource constraints

### Visualization & UI
- 🎯 **Confidence Breakdown**: Visual representation of requirement confidence scores
- 🔑 **Keyword Highlighting**: Color-coded highlighting of extracted entities in original text
- 📊 **Metrics Dashboard**: Key statistics about the analysis
- 📈 **Entity Legend**: Clear visual guide for entity types
- 💾 **Export Options**: Download tickets as JSON, CSV, or full analysis data

### Advanced Features
- Dependency parsing for enhanced entity extraction
- Multi-token entity recognition
- Confidence scoring based on entity presence and keyword detection
- Configurable confidence threshold
- Batch entity extraction and analysis
- Session-based state management

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone/download the application**
```bash
cd src/apps
```

2. **Install required dependencies**
```bash
pip install streamlit spacy plotly pandas scikit-learn
```

3. **Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

### Optional Dependencies
For enhanced NLP performance:
```bash
# Download larger spaCy model for better accuracy
python -m spacy download en_core_web_md

# For sentence transformers (if using vector-based classification)
pip install sentence-transformers
```

## Usage

### Running the Application

```bash
streamlit run requirement_ticket.py
```

The application will open in your default browser at `http://localhost:8501`

### Basic Workflow

1. **Enter Text**: Paste or type your business requirement in the input area
2. **Configure Threshold** (Optional): Adjust confidence threshold in the sidebar
3. **Click Analyze**: Press "🚀 Analyze & Generate Ticket"
4. **Review Results**: 
   - Check requirement classification (✅ Valid or ❌ Not Valid)
   - Review extracted entities and confidence scores
   - See highlighted keywords in the text
5. **Export**: Download the ticket in your preferred format

### Configuration

The sidebar allows you to:
- **Adjust Confidence Threshold**: Set minimum confidence (0.0-1.0) for requirement classification
- **View Documentation**: Access the "How it works" guide
- **See Entity Legend**: Reference entity type definitions

## Architecture

### Components

#### `requirement_processor.py`
Core NLP pipeline module providing:
- `RequirementProcessor`: Main class for text processing
  - `extract_entities()`: Extracts structured data from text
  - `is_requirement()`: Classifies text as requirement or not
  - `extract_keywords()`: Identifies requirement-related keywords
  - `highlight_text()`: Generates entity-highlighted text
  - `_extract_dependency_structure()`: Enhanced extraction using syntax

- Helper functions:
  - `create_ticket()`: Converts entities to structured ticket format

#### `requirement_ticket.py`
Streamlit application providing:
- Web-based user interface
- Real-time text analysis
- Interactive visualizations using Plotly
- Export functionality
- Configuration management
- Session state management

### Data Flow

```
User Input Text
	↓
Text Processing (spaCy NLP)
	├─ Tokenization
	├─ Entity Recognition (Pattern & ML)
	└─ Dependency Parsing
	↓
Entity Extraction & Classification
	├─ Extract: Stakeholder, Action, Object, etc.
	├─ Calculate: Confidence Scores
	└─ Classify: Is Requirement? (Yes/No)
	↓
Analysis & Visualization
	├─ Keyword Highlighting
	├─ Confidence Metrics
	└─ Entity Breakdown
	↓
Structured Ticket Generation
	├─ Formatted Output (JSON/CSV)
	├─ Metadata & Timestamps
	└─ Export Ready
```

## Entity Types & Examples

### STAKEHOLDER
Represents who needs the requirement
- Examples: "user", "customer", "admin", "organization", "developer"
- Highlighted in: 🔵 Blue

### ACTION
The operation to perform
- Examples: "create", "update", "delete", "manage", "track", "provide", "ensure"
- Highlighted in: 🟡 Yellow

### OBJECT
What is acted upon
- Examples: "report", "data", "user account", "notification", "dashboard"
- Highlighted in: 🔷 Light Blue

### SYSTEM
Target system or component
- Examples: "application", "platform", "API", "database", "service"
- Highlighted in: 🟣 Purple

### QUALITY
Non-functional requirements
- Examples: "secure", "scalable", "reliable", "user-friendly", "performant"
- Highlighted in: ⚫ Gray

### PRIORITY
Urgency level
- Examples: "high", "medium", "low", "critical", "urgent"
- Highlighted in: 🔴 Red

### CONDITION
When/if clauses
- Examples: "when user logs in", "if data is updated", "after payment"

### CONSTRAINT
Time and resource limits
- Examples: "within 2 seconds", "maximum 1000 users", "at least 99.9% uptime"

## Output Ticket Format

Generated tickets contain:

```json
{
  "ticket_id": "REQ-A1B2C3D4",
  "title": "CREATE - fitness goals tracking",
  "description": "Original user input text...",
  "is_requirement": true,
  "requirement_confidence": 0.85,
  "extraction_confidence": 0.82,
  "stakeholder": "user",
  "action": "create",
  "object": "fitness tracking application",
  "system": "mobile application",
  "priority": "high",
  "quality_attributes": "user-friendly",
  "conditions": null,
  "constraints": "real-time updates",
  "status": "extracted",
  "generated": "2024-01-15 14:23:45"
}
```

## Example Requirements

The application includes several built-in examples:

1. **Mobile App**: "We need a mobile application that allows users to track their fitness goals and progress with real-time notifications"

2. **Integration**: "Ensure that the new software solution has a user-friendly interface and integrates seamlessly with existing systems"

3. **Admin Feature**: "As an administrator, I need the ability to manage user permissions and security roles within the system"

4. **Performance**: "The system should support at least 1000 concurrent users with response times under 2 seconds"

Click any example to automatically fill the input field.

## Confidence Scoring

The application uses two types of confidence scores:

### Requirement Confidence (0-100%)
Determines if text is a business requirement based on:
- Presence of requirement keywords (40% weight): "need", "require", "must", "shall", etc.
- Stakeholder + Action presence (30% weight): Essential entities for a requirement
- Object extraction (15% weight): What is being acted upon
- Quality attributes (15% weight): Non-functional requirements

### Extraction Confidence (0-100%)
Measures quality of entity extraction:
- Base: Number of entities found / 5 (max 1.0)
- Boost: +0.3 if key entities (stakeholder, action, object) all present
- Capped at 1.0 (100%)

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'spacy'"
**Solution**: Install required dependencies
```bash
pip install spacy streamlit plotly
```

### Issue: "Error loading language model"
**Solution**: Download the spaCy model
```bash
python -m spacy download en_core_web_sm
```

### Issue: Very low confidence scores
**Solutions**:
- Use clearer requirement language ("we need...", "shall...", "must...")
- Include more entities (stakeholder, action, object)
- Lower the confidence threshold in sidebar settings
- Provide complete, well-structured sentences

### Issue: Incorrect entity extraction
**Suggestions**:
- Use specific, standard terminology
- Avoid ambiguous pronouns
- Include all relevant entities in single sentence
- Provide context around requirements

## Performance Notes

- First run may take 30-60 seconds while loading spaCy model
- Subsequent runs are cached and fast (< 1 second)
- Streamlit automatically caches the processor with `@st.cache_resource`
- Processing time depends on text length (typically < 100ms per text)

## Extending the Application

### Add Custom Keywords
Edit `REQUIREMENT_KEYWORDS` or `QUALITY_KEYWORDS` in `requirement_processor.py`

### Modify Entity Patterns
Update the patterns in `RequirementProcessor._add_entity_patterns()` method

### Add Classification Model
Replace the heuristic `is_requirement()` with ML model predictions

### Custom Export Formats
Add new export buttons in the "Export Options" section of `requirement_ticket.py`

## Integration with ML Pipeline

The architecture supports integration with the `ba.ipynb` notebook pipeline:

1. **Add pre-trained model**: Load XGBoost/SVC classifier for `is_requirement()`
2. **Use SentenceTransformer**: Replace spaCy vectors with sentence embeddings
3. **Advanced NER**: Use transformer-based NER (en_core_web_trf) for better accuracy
4. **Confidence calibration**: Train confidence scoring on labeled data

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >= 1.0 | Web UI framework |
| spacy | >= 3.0 | NLP pipeline |
| plotly | >= 5.0 | Interactive visualizations |
| pandas | >= 1.0 | Data handling |
| scikit-learn | >= 0.24 | ML utilities |
| plotly-express | >= 5.0 | Quick plotting |

## License

This application is part of the Business Requirement Analysis project.

## Support

For issues or questions:
1. Check the sidebar "How it works" section
2. Review example requirements
3. Consult the troubleshooting section
4. Check spaCy documentation: https://spacy.io/

---

**Last Updated**: 2024
**Version**: 1.0
