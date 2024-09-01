# AWS SSL Certificate Setup

This repository contains instructions for setting up an SSL certificate for use with AWS services. Follow the steps below to generate your SSL certificate and private key.

## Prerequisites

- Make sure you have `openssl` installed on your system.
- Ensure that you have permissions to execute scripts on your machine.

## Generate SSL Certificate and Key

1. **Make the Script Executable**

   First, you need to make the `ssl.sh` script executable. Run the following command:

   ```bash
   chmod +x ssl.sh
   ```bash
   ./ssl.sh
   ```bash
   openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
