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

### Installing Requirements

To install the required packages for SCGrinderAI+, navigate to the project directory and run the following command:

```
pip install -r requirements.txt
```

## Getting Started

1. Sign up for free on [SCGrinderAI+ Registration](https://app.shitcoingrinder.xyz/register) to retrieve your API KEY.
2. Once registered, your API KEY will be visible in the dashboard.
3. Clone the SC

GrinderAI+ repository.
4. Rename the configuration file from <code>settings.ini.example</code> to <code>settings.ini</code>.
5. Start the SCGrinderAI+ client by running the command: `python scgrind.py`

## Configuration

The configuration file looks like that:

<code>
    [Account]
    private_key = <your_private_key>
    auth_token = <your_api_key>

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

## Contact Us

For any inquiries or support, please contact our team at support@shitcoingrinder.xyz

---

© 2023 SCGrinderAI+ | All Rights Reserved.
