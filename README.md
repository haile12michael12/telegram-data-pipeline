# 📊 Telegram Analytical Data Pipeline

An end-to-end data product that extracts, transforms, enriches, and serves analytics from **public Ethiopian medical Telegram channels** using:

- **Telethon** for data scraping  
- **YOLOv8** for image object detection  
- **PostgreSQL + dbt** for data modeling  
- **FastAPI** for analytical APIs  
- **Dagster** for orchestration  
- **Docker** for reproducibility  

---

## 🗺️ Overview

This pipeline collects raw Telegram messages and images from medical-related channels, enriches them with AI (YOLO), transforms them into clean analytical tables with dbt, and exposes insights through a modern API.

---

## 📦 Features

✅ Scrape public Telegram messages & images  
✅ Run YOLOv8 object detection on scraped images  
✅ Transform raw JSON into star-schema data warehouse  
✅ Expose search & reporting APIs via FastAPI  
✅ Orchestrate entire pipeline using Dagster  
✅ Fully containerized with Docker  

---

## 🏗️ Architecture

