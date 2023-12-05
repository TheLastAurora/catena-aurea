# Catena Aurea API

The Catena Aurea API project: a Python-based web crawler and web scraping tool designed to extract commentaries from the Catena Aurea on the [Glossae Scripturae Sacrae-electronicae](https://gloss-e.irht.cnrs.fr/). 

## Table of Contents

- [Catena Aurea API](#catena-aurea-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Next Implementations (TODO)](#next-implementations-todo)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Extensible Web Crawler:** Fetch commentaries from the Catena Aurea on the Vatican website.
- **Specialized Web Scraping:** Utilize Beautiful Soup to parse and extract relevant information from anywhere in the website. The can be done for the Biblia communis, Glossa ordinaria, Summa super Psalterium etc.
  
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/catena-aurea-web-crawler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd catena-aurea
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. If there is no index.json in the outputs folder, run the crawler:

    ```bash
    python crawler.py
    ```
2. The script will fetch the URL references from the Catena Aurea and store the results in json format.

3. Next, you can test its usage by either implementing argparser in ```extract.py``` (I removed it for its just an interface for the in-development interface) or run it in the sandbox notebook. Explore the extracted data and integrate it into your projects as needed.

## Next Implementations (TODO)

Feel free to contribute to the project and add new features. Some ideas for future improvements include:

- **API Integration:** Convert the project into a RESTful API for easy access.
- **BardAPI Integration** Utilizes the BardAPI translation to convert the commentaries into any language. 
- **Data Storage:** Implement a database to store and manage the extracted commentaries.
- **User Interface:** Develop a simple web interface for user-friendly interaction.

## Contributing

Contributions are welcome! To contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push the branch to your fork: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for your purposes.
