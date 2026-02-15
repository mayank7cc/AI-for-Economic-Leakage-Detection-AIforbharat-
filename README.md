# AI for Economic Leakage Detection
## Ensuring Welfare Benefits Reach the Right Citizens

An AI-powered governance intelligence platform that detects fraud, predicts leakage risks, and strengthens transparency in welfare distribution.

---

## Overview

Economic leakage in welfare systems prevents benefits from reaching rightful citizens due to fraud, duplicate beneficiaries, abnormal fund distribution, and delayed corruption detection.

This project builds an AI-powered governance intelligence system that detects anomalies, identifies fraud patterns, and predicts leakage risks to enable proactive administrative action.

---

## Problem Statement

Welfare distribution systems face critical challenges:

- Duplicate or ghost beneficiaries  
- Fraudulent fund diversion  
- Abnormally approved transactions  
- Ignored or unstructured citizen complaints  
- Delayed corruption detection  

### Impact

- Genuine citizens lose access to benefits  
- Government funds are misused  
- Public trust in governance declines  

Traditional rule-based systems cannot detect evolving fraud patterns at scale.

---

## Solution

We propose an AI-driven governance platform that:

- Detects duplicate and ghost beneficiaries  
- Identifies abnormal fund distribution patterns  
- Analyzes complaints using NLP and voice processing  
- Generates predictive leakage risk scores  
- Visualizes high-risk zones using geo-spatial heatmaps  
- Enables proactive audit and prevention actions  

---

## Key Features

### Duplicate Beneficiary Detection
- Fuzzy matching and similarity detection  
- Shared bank account and address detection  
- Suspicious identity clustering  

### Anomaly Detection
- Isolation Forest outlier detection  
- Abnormally high fund approvals  
- Suspicious transaction patterns  

### Risk Scoring Engine
- Multi-factor weighted risk scoring  
- Beneficiary and district risk indices  
- Prioritized audit recommendations  

### Complaint Intelligence (Planned)
- Voice-to-text complaint capture  
- Sentiment and urgency detection  
- Topic clustering and corruption hotspot detection  

### Geo-Spatial Visualization
- District-level leakage heatmaps  
- Risk hotspot identification  
- Trend analytics  

### Governance Decision Support
- Audit triggers  
- Investigation prioritization  
- Case tracking and reporting  

---

## System Architecture

Data Sources → Processing → AI Models → Risk Sc​​oring → API → Dashboard

**Inputs**
- Beneficiary records  
- Transactions  
- Citizen complaints  

**AI Intelligence**
- Duplicate detection  
- An​​omaly detection  
- Risk scoring  

**Outputs**
- Risk alerts  
- Heatmaps  
- Investigation insights  

See **design.md** for detailed architecture.

---

## Technology Stack

### Backend
- FastAPI  
- Python  
- Uvicorn  

### AI & Machine Learning
- scikit-learn (Isolation Forest)  
- RapidFuzz (duplicate detection)  
- Transformers (planned NLP)  
- PyTorch (future deep learning)  

### Data Processing
- pandas  
- numpy  

### Visualization
- Folium  
- Plotly  
- Seaborn  

### Cloud (Planned Deployment)
- AWS S3  
- AWS Lambda  
- AWS SageMaker  
- AWS Comprehend and Transcribe  
- AWS QuickSight  

---

## Project Structure

```
economic-leakage-ai/
├── backend/              # FastAPI backend
├── models/               # ML detection modules
├── notebooks/            # data processing and analysis
├── utils/                # loaders, validators, logging
├── data/
│   ├── raw/
│   └── processed/
├── pipeline.py           # processing pipeline
├── config.py             # configuration settings
├── requirements.md       # system requirements
├── design.md             # system design
└── README.md
```

---

## Workflow

1. Ingest welfare data  
2. Preprocess and engineer features  
3. Detect duplicates and anomalies  
4. Calculate risk scores  
5. Serve insights via API and visualizations  
6. Enable administrative action  

---

## Getting Started

### Clone Repository

```bash
git clone https://github.com/mayank7cc/AI-for-Economic-Leakage-Detection-AIforbharat-
cd AI-for-Economic-Leakage-Detection-AIforbharat-
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows
```bash
venv\Scripts\activate
```

Mac/Linux
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Generate Sample Data

```bash
python notebooks/data_generator.py
```

### Run Processing Pipeline

```bash
python pipeline.py
```

### Start API Server

```bash
uvicorn backend.app:app --reload
```

Open API docs:

http://127.0.0.1:8000/docs

---

## API Endpoints

| Endpoint | Description |
|----------|------------|
| `/` | Health check |
| `/anomalies` | Get anomalous beneficiaries |
| `/risk` | Get high-risk beneficiaries |
| `/beneficiary/{id}` | Get beneficiary details |

---

## Impact and Benefits

- Ensures benefits reach rightful citizens  
- Reduces financial leakage  
- Enables preventive governance  
- Improves transparency and accountability  
- Strengthens public trust  

Even a 5 percent leakage reduction can save crores annually.

---

## Responsible AI and Ethics

- Explainable risk scoring  
- Privacy and data protection safeguards  
- Bias monitoring and fairness checks  
- Transparent audit logs  

---

## Future Roadmap

- Complaint intelligence integration  
- Real-time dashboard and analytics  
- Cloud deployment on AWS  
- Predictive fraud risk modeling  
- Mobile citizen reporting application  
- National-scale integration  

---

## Hackathon Alignment

- AI for public systems and governance  
- Impro​​ves welfare access  
- Enhances transparency and accountability  
- Scalable and socially impactful  

---

## Contributors

ESaral Tech Team - Mayank Parab , Nipun Alwala , Aditya Dhuri 

---

## Contact

mayankparab2006@gmail.com

---

## One-Line Pitch

AI-powered predictive governance to detect and prevent welfare fund leakage before it happens.


