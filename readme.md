# ShitCoinGrinderAI+

<div style="background-color: rgba(0,0,0); text-align: center; margin-bottom: 20px">
    <img src="assets/logo.png" alt="SCGrinderAI+ Logo" style="width: 200px; height: auto;">
</div>

SCGrinderAI+ is an innovative software that leverages advanced AI technology to revolutionize your approach to the shitcoin market. With its powerful AI model trained on billions of data points, SCGrinderAI+ identifies high-potential tokens and applies the lucrative black swan strategy for maximum profitability.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Python3 Installation](#python3-installation)
  - [Pip Installation](#pip-installation)
  - [Installing Requirements](#installing-requirements)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Black Swan Strategy](#black-swan-strategy)
- [Early Access](#early-access)
- [License](#license)

## Introduction

SCGrinderAI+ is a groundbreaking software that automates the analysis of countless tokens deployed on the Ethereum and Binance Smart Chain (BSC) networks. By harnessing the power of AI and real-time data analysis, it identifies high-potential tokens that have the potential to skyrocket in value. With SCGrinderAI+, you can stay ahead of the curve, maximize your investment returns, and navigate the volatile shitcoin market with confidence.

## Features

- **Token Scanning and Analysis**: SCGrinderAI+ scans and analyzes tokens deployed on Ethereum and BSC, leveraging its AI model trained on billions of data points.
- **Real-time Insights**: Stay informed with real-time insights on emerging tokens with high growth potential.
- **Optimal Entry Points**: Identify the best entry points for your trades, eliminating the guesswork of "buying the dip" and "selling the top."
- **Scam Token Detection**: SCGrinderAI+ filters out scam tokens, helping you avoid potential losses and focus on legitimate tokens.
- **Automatic Wallet Rebalancing**: Automate the management and rebalancing of your crypto portfolio based on predefined strategies and market conditions.
- **Effortless Asset Monitoring**: Track your assets and receive alerts for take-profit or stop-loss opportunities, eliminating the need for constant manual monitoring.

## Installation

### Python3 Installation

- **macOS**:
  - Open a terminal.
  - Run the command: `brew install python3`
- **Windows**:
  - Download the Python3 installer from the official website: [Python Downloads](https://www.python.org/downloads/)
  - Run the installer and follow the instructions.

### Pip Installation

- **macOS**:
  - Open a terminal.
  - Run the following command to download the `get-pip.py` script:
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ```
  - Once the script is downloaded, run the command: `python3 get-pip.py`
- **Windows**:
  - Download the `get-pip.py` script from this link: [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
  - Save the script to a folder on your computer.
  - Open a command prompt, navigate to the folder where you saved the script, and run the command: `python get-pip.py`


## Getting Started

1. Clone the SCGrinderAI+ repository: <code>git clone https://github.com/JediKunnow/ShitcoinGrinderAI</code>
2. Rename the configuration file from <code>settings.ini.example</code> to <code>settings.ini</code>.
3. Paste private key and api key in the configuration file (see [Configuration](#configuration)).
4. Install requirements (see [Installing requirements](#installing-requirements))
5. Start the client with <code>python3 client.py</code>

### Installing requirements

To install the required packages for SCGrinderAI+, navigate to the project directory and run the following command:

```
pip install -r requirements.txt
```

### Configuration

The configuration file looks like that:

<code>
    [Account]
    private_key = 'your_private_key'
    auth_token = 'your_api_key'

    [Source]
    host = app.shitcoingrinder.xyz
    port = 8081

    [Network]
    # BSC=56 | ETH=1
    id = 56
    rpc = https://bsc-dataseed1.binance.org/

    [Trading]
    # this is your max trade size expressed in percentage.
    # Eg: 30 = 30% of the USDT in your wallet.
    max_trade_size = 30
    # Max lifetime of an open position, expressed in days.
    position_max_lifetime = 30
    # Take profit in %
    take_profit = 200
    # Position check interval, in minutes
    check_interval = 5
</code>

Let's describe further some parameters:
- <code>private_key</code>: your wallet private key. It's stored on your computer and it won't be sent to anyone.
- <code>auth_token</code>: it's your apikey. You can find it in the [dashboard](https://app.shitcoingrinder.xyz/dashboard) 
- <code>max_trade_size</code>: The maximum size of a trade your are intended to do, expressed in percentage of the total amount of USDT in your wallet. If you have 1000 USDT in your wallet and this parameter is set to 10, the maximum trade size for you will be 100 USDT. We advice to keep this value between 5 and 30%.
- <code>take_profit</code>: Everytime you'll recieve a signal you'll open a position. This parameter means when to close the position and take the profit. If set to 200 it means a 2x.
- <code>position_max_lifetime</code>: If a position doesn't hit the tp treeshold it will expire instead of remaing open forever. Set this value here expressed in days. If this parameter is set to 30, positions will be automatically closed after 30 days if the tp isn't reached before.
- <code>check_interval</code>: The position status is checked periodically, default is every 5 minutes. Here you can set a custom value for that, but we strongly advice to don't set a value lower than 5 minutes, or the RPC might get overloaded.

## Architecture

SCGrinderAI+ follows a client-server architecture with the addition of a source component.

- **Server**: The server is where clients connect. Clients wait for signals from the server and execute them.
- **Client**: The client is an open-source component, and contributions from the community are welcome.
- **Source**: The source is a proprietary service that analyzes every transaction on the ETH and BSC blockchains to find high-potential tokens. It continuously monitors their behavior and sends signals to the server when a token shows significant potential.

## Black Swan Strategy

The black swan strategy is a powerful investment approach employed by SCGrinderAI+. It suggests investing a small percentage of your portfolio in high-risk investments, such as shitcoins. By buying a wide range of tokens recognized by the AI model, the strategy aims to capture the significant growth potential of a few tokens, which can outweigh any previous losses.

## License

The SCGrinderAI+ software is released under the [SCGrinderAI+ License](LICENSE). The client component is open-source and subject to the terms of the [Open Source License](LICENSE.client).
## Get the Early Access

To get early access to SCGrinderAI+, follow these simple steps:

1. Visit [https://app.shitcoingrinder.xyz/register](https://app.shitcoingrinder.xyz/register) to sign up for free.
2. Fill in the required information, including your name, email, and password.
3. Complete the registration process.
4. Once registered, log in to your account.
5. In the dashboard, you will find your unique API KEY.
6. Copy the API KEY and keep it safe.

By signing up and obtaining an API KEY, you gain access to the early version of SCGrinderAI+ and all its powerful features. Don't miss out on the opportunity to revolutionize your shitcoin investments.

Please note that only the minimum required information (name, email, and password) is needed for the sign-up process. We value your privacy and ensure that your personal information is handled securely.

Join the early access program today and unleash the full potential of SCGrinderAI+!

## Installation on VPS

# SCGrinderAI+ - Installation and Setup Guide

## Introduction

This guide will walk you through the process of installing, configuring, and using SCGrinderAI+ on a VPS (Virtual Private Server). SCGrinderAI+ is an innovative software that leverages advanced AI technology to revolutionize your approach to the shitcoin market. By following the steps outlined in this guide, you'll be able to set up SCGrinderAI+ on both Linux and Windows VPS environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation on Linux VPS](#installation-on-linux-vps)
  - [Step 1: Connect to your Linux VPS](#step-1-connect-to-your-linux-vps)
  - [Step 2: Update System Packages](#step-2-update-system-packages)
  - [Step 3: Install Python and Pip](#step-3-install-python-and-pip)
  - [Step 4: Clone the SCGrinderAI+ Repository](#step-4-clone-the-scgrinderai-repository)
  - [Step 5: Install Required Packages](#step-5-install-required-packages)
  - [Step 6: Configure SCGrinderAI+](#step-6-configure-scgrinderai)
  - [Step 7: Start SCGrinderAI+](#step-7-start-scgrinderai)
- [Installation on Windows VPS](#installation-on-windows-vps)
  - [Step 1: Connect to your Windows VPS](#step-1-connect-to-your-windows-vps)
  - [Step 2: Install Python and Pip](#step-2-install-python-and-pip)
  - [Step 3: Clone the SCGrinderAI+ Repository](#step-3-clone-the-scgrinderai-repository)
  - [Step 4: Install Required Packages](#step-4-install-required-packages)
  - [Step 5: Configure SCGrinderAI+](#step-5-configure-scgrinderai)
  - [Step 6: Start SCGrinderAI+](#step-6-start-scgrinderai)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- A VPS with Linux or Windows operating system.
- SSH access to your VPS for Linux installations.
- Remote desktop access to your VPS for Windows installations.
- Python 3 installed on your VPS.

## Installation on Linux VPS

### Step 1: Connect to your Linux VPS

Use SSH to connect to your Linux VPS. You can use tools like PuTTY (Windows) or the terminal (macOS/Linux) to establish the SSH connection.

```bash
ssh user@your_server_ip
```

### Step 2: Update System Packages

Before installing any software, it's recommended to update your system packages to the latest versions.

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 3: Install Python and Pip

Install Python 3 and Pip package manager on your Linux VPS.

```bash
sudo apt install python3 python3-pip -y
```

### Step 4: Clone the SCGrinderAI+ Repository

Clone the SCGrinderAI+ repository to your VPS.

```bash
git clone https://github.com/your_username/SCGrinderAI.git
```

### Step 5: Install Required Packages

Navigate to the project directory and install the required packages.

```bash
cd SCGrinderAI
pip3 install -r requirements.txt
```

### Step 6: Configure SCGrinderAI+

Edit the configuration file to provide your API key.

```bash
nano settings.ini
```

Replace `your api key` with your actual API key.
Replace `private key` with your actual private key.

### Step 7: Start SCGrinderAI+

Start SCGrinderAI+ by running the following command.

```bash
python3 client.py
```

SCGrinderAI+ should now be up and running on your Linux VPS.

## Installation on Windows VPS

### Step 1: Connect to your Windows VPS

Use remote desktop access to connect to your Windows VPS.

### Step 2: Install Python and Pip

Download and install the latest version of Python 3 from the official Python website: https://www.python.org/downloads/

During the installation process, make sure to check the option to add Python to the system PATH.

### Step 3: Clone the SCGrinderAI+ Repository

Open a command prompt on your Windows VPS and clone the SCGrinderAI+ repository.

```bash
git clone https://github.com/your_username/SCGrinderAI.git
```

### Step 4: Install Required Packages

Navigate to the project directory and install the required packages.

```bash
cd SCGrinderAI
pip install -r requirements.txt
```

### Step 5: Configure SCGrinderAI+

Edit the configuration file (`config.ini`) to provide your API key.

### Step 6: Start SCGrinderAI+

Launch the SCGrinderAI+ client by running the following command.

```bash
python client.py
```

SCGrinderAI+ should now be up and running on your Windows VPS.


## Contact Us

For any inquiries or support, please contact our team at support@shitcoingrinder.xyz

---

© 2023 SCGrinderAI+ | All Rights Reserved.
