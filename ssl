#!/bin/bash
# Update the package manager and install necessary packages
sudo yum update -y
sudo yum install -y httpd mod_ssl

# Start and enable Apache HTTP server
sudo systemctl start httpd
sudo systemctl enable httpd

# Install Certbot for Let's Encrypt
sudo yum install -y epel-release
sudo yum install -y certbot python2-certbot-apache

# Obtain SSL certificate from Let's Encrypt
# Replace 'your-domain-name.com' with your actual domain
sudo certbot --apache -d your-domain-name.com -n --agree-tos --email your-email@example.com

# Setup auto-renewal for the SSL certificate
(crontab -l 2>/dev/null; echo "0 0,12 * * * /usr/bin/certbot renew --quiet") | crontab -
