# Papflix

Papflix is a movie organizer software made in Python and Qt. Provides automatic integration of the films, as well as additional information about them (eg poster, cast, rating, etc.). The correct matching of the films in relation to the file name of each film is achieved through two similarity algorithms.


## Screenshots

![App Screenshot](https://media.giphy.com/media/8HtoWZNgiafYko29Tu/giphy.gif)


## Requirements

Papflix requires the following to run:
-OpenSSL


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install papflix.

```bash
pip install papflix-package-kpaparid
```

## Usage

```python
from papflix_package import main

# import movies by giving a path in the function
main.run(path)

# once the Database is filled, the path is no longer needed
main.run()

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
