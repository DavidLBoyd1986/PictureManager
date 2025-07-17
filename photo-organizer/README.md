# Photo Organizer

Photo Organizer is a TypeScript application designed to help users organize their photos in a specified directory. The application provides options to sort photos based on various criteria, making it easier to manage and locate images.

## Features

- Organize photos by date
- Organize photos by location
- Organize photos by type

## Project Structure

```
photo-organizer
├── src
│   ├── main.ts          # Entry point of the application
│   ├── organizer.ts     # Contains the Organizer class with organizing methods
│   ├── options.ts       # Defines the options interface for organizing photos
│   └── utils
│       └── fileHelpers.ts # Utility functions for file operations
├── package.json         # npm configuration file
├── tsconfig.json        # TypeScript configuration file
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/microsoft/WPF-Samples.git
   cd photo-organizer
   ```

2. Install the dependencies:
   ```
   npm install
   ```

## Usage

1. Run the application:
   ```
   npm start
   ```

2. Follow the prompts to enter the directory path and select your organizing options.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.