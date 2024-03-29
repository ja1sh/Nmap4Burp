# Nmap4Burp - Nmap Scanner for Burp Suite

## Overview

The Nmap Scanner for Burp Suite is a Burp extension that allows you to run Nmap scans directly from the Burp Suite interface. It provides a convenient way to perform network reconnaissance and gather information about target systems.

## Features

- Integration of Nmap scans within Burp Suite.
- Customizable Nmap scan parameters.
- Real-time display of Nmap scan output.

## Requirements

- [Burp Suite](https://portswigger.net/burp)
- [Nmap](https://nmap.org/) (Make sure the path to the 'nmap' binary is correctly configured in the extension)

## Installation

1. Download the `nmap4burp.py` script.
2. Open Burp Suite and go to the "Extender" tab.
3. Click on the "Extensions" tab.
4. Click on the "Add" button.
5. Choose the Python type and select the `nmap4burp.py` script.
6. The extension should now be loaded and accessible from the "Extender" tab.

## Usage

1. Configure the path to the 'nmap' binary in the extension settings.
2. Enter the target IP or domain.
3. Click on the "Run Nmap Scan" button.
4. View real-time Nmap scan output in the extension UI.

Follow this [Medium](https://ja1sharma.medium.com/nmap4burp-burp-extension-5e2d7ca8927f) tutorial for usage samples

## Author

[Jai Sharma](#) - [GitHub](https://github.com/ja1sh/Nmap4Burp)

## Version

1.0.1

## Social Media

- X: [@ja1sharma](https://twitter.com/ja1sharma)

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality or fix any bugs.
