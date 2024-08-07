# Research Data Lifecycle Visualization

This project provides an interactive visualization of the Research Data Lifecycle, implemented using Flask and D3.js. It's designed to match the styling of the Research Data Alliance (RDA) website.

## Features

- Interactive D3.js visualization of research data lifecycle stages
- API endpoints for retrieving lifecycle data, substages, and tools
- SQLAlchemy models for storing lifecycle information
- RDA-styled user interface

## Project Structure

```text
project_root/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── static/
│       ├── css/
│       │   └── rda_styles.css
│       ├── js/
│       │   └── lifecycle_visualization.js
│       └── images/
│           └── RDA_Logotype_CMYK.png
├── templates/
│   └── index.html
├── config.py
├── app.py
├── requirements.txt
└── updates.txt
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/research-data-lifecycle.git
   cd research-data-lifecycle
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   flask db upgrade
   ```

5. Run the development server:

   ```bash
   flask run
   ```

6. Open a web browser and navigate to `http://localhost:5000` to view the application.

## Development

- The main application logic is in `app.py`
- Database models are defined in `app/models.py`
- Routes are defined in `app/routes.py`
- The D3.js visualization code is in `app/static/js/lifecycle_visualization.js`
- Styling is managed in `app/static/css/rda_styles.css`

To make changes:

1. Modify the relevant files
2. Update `updates.txt` with a description of your changes
3. Commit your changes with a descriptive commit message

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Authors

- Your Name <your.email@example.com>

## Acknowledgments

- Research Data Alliance (RDA) for inspiration and styling
- Flask and D3.js communities for their excellent tools and documentation
