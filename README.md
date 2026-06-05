# Know Your Stuff

**Know Your Stuff** is an AI-powered Chrome Extension currently in development that helps users make smarter purchasing decisions while shopping online. The extension provides historical price insights, price trend visualizations, and contextual buy-or-wait recommendations directly on e-commerce product pages.

## Features

* 📈 Historical price tracking and visualization
* 💰 Lowest, highest, and current price analysis
* 🤖 AI-powered purchase recommendations
* 🛒 Automatic product detection on supported e-commerce websites
* 📊 Interactive price history graphs
* 🎯 Context-aware insights based on sales events and product launch cycles

## Vision

Most price-tracking tools tell users what happened to a product's price.

**Know Your Stuff** aims to answer a more important question:

> **"Should I buy this product now, or wait?"**

By combining historical pricing data, market events, and AI-generated insights, the goal is to provide users with actionable purchasing guidance in a single click.

---

*Built to simplify online shopping through data-driven decision making.*


## How It Works

When a user visits a product page on an e-commerce website and opens the extension:

1. The extension identifies the product and extracts relevant information.
2. Product data is sent to the backend for analysis.
3. Historical pricing data is retrieved and processed.
4. The recommendation engine evaluates:

   * Historical price trends
   * Upcoming sales events
   * Product age and launch cycles
   * Current market conditions
5. A personalized buying recommendation is generated and displayed.

## Tech Stack

### Frontend

* JavaScript
* HTML5
* CSS3
* Chrome Extensions API (Manifest V3)
* Chart.js

### Backend

* Python
* FastAPI

### Data Collection

* Playwright
* BeautifulSoup

### Database

* PostgreSQL

### AI & Analytics

* LLM APIs
* Custom Recommendation Engine

## Project Status

🚧 **Currently in Development**

The project is under active development. Initial focus areas include:

* Product detection
* Price history tracking
* Data collection pipeline
* Recommendation engine development
