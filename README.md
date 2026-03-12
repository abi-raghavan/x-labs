# x-labs

A collection of experimental projects and proof-of-concepts for testing different ideas and technologies.

## Projects

### 1. Experimentation Lab (`experimentation_lab/`)

A complete A/B testing experimentation system with statistical analysis.

**Features:**
- Deterministic user assignment with stable hashing
- Traffic simulation with realistic conversion differences  
- Statistical testing (z-test for conversions, t-test for revenue)
- Risk detection (sample ratio mismatch, sample size checks)
- Streamlit UI for experiment management and analysis

**Tech Stack:** Python, Streamlit, SQLite, Pandas, NumPy, SciPy, Plotly

**Run:** 
```bash
cd experimentation_lab
pip install -r requirements.txt
streamlit run app.py
```

**Test:**
```bash
cd experimentation_lab
pytest tests/ -v
```

## Project Structure

```
x-labs/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── experimentation_lab/         # A/B testing system
    ├── app.py                   # Streamlit UI
    ├── assignment.py            # User assignment logic
    ├── simulation.py            # Traffic simulation
    ├── metrics.py               # Metrics calculation
    ├── stats.py                 # Statistical tests
    ├── risk.py                  # Risk detection
    ├── db.py                    # Database functions
    ├── requirements.txt         # Dependencies
    └── tests/                   # Test suite
```

## Adding New Projects

Each new experimental project should be in its own subdirectory with:
- Clear README explaining the project
- Its own requirements.txt if needed
- Proper test coverage
- Following the coding standards in `.cursor/rules/coding-style.mdc`

## Development Guidelines

- Keep projects simple and focused
- No over-engineering
- Follow the coding rules in `.cursor/rules/coding-style.mdc`
- Write tests with fixtures->run->assert pattern
- Use minimal dependencies