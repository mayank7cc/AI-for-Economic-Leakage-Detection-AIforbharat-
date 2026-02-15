# Requirements Specification

## AI for Economic Leakage Detection
### Ensuring Welfare Benefits Reach the Right Citizens

---

## 1. Project Overview

### 1.1 Objective
Develop an AI-powered governance intelligence platform that detects, predicts, and prevents leakage in welfare distribution systems, ensuring benefits reach legitimate beneficiaries while improving transparency and accountability.

### 1.2 Problem Statement
Welfare systems face significant leakage due to:
- Duplicate or ghost beneficiaries
- Fraudulent fund diversion
- Abnormal approval patterns
- Unstructured and ignored complaints
- Delayed corruption detection

This leads to financial loss, exclusion of genuine beneficiaries, and reduced public trust.

---

## 2. Stakeholders

### 2.1 Primary Users
- Government welfare departments
- Audit & compliance officers
- Policy makers

### 2.2 Secondary Users
- Citizens & beneficiaries
- NGOs & transparency bodies

---

## 3. System Architecture

### 3.1 Current Implementation

```
economic-leakage-ai/
├── backend/          # FastAPI REST API
├── models/           # ML models for fraud detection
├── notebooks/        # Data processing scripts
├── utils/            # Shared utilities
├── data/             # Data storage
├── config.py         # Configuration management
└── pipeline.py       # Main orchestrator
```

### 3.2 Technology Stack
- **Backend**: FastAPI, Uvicorn
- **ML/AI**: scikit-learn, transformers, torch
- **Data Processing**: pandas, numpy
- **Visualization**: folium, plotly, seaborn
- **Fuzzy Matching**: rapidfuzz
- **Data Generation**: faker

---

## 4. Functional Requirements

### 4.1 Data Ingestion ✓ IMPLEMENTED

**Module**: `notebooks/data_generator.py`, `utils/data_loader.py`

**Features**:
- ✓ Import beneficiary & household records (CSV format)
- ✓ Generate synthetic welfare data for testing
- ✓ Data validation and schema checking
- ✓ Error handling for missing/corrupt files

**Data Fields**:
- beneficiary_id
- name, phone, address
- bank_account
- scheme (Food Subsidy, Farmer Aid, Scholarship)
- amount, district, date

**Future Enhancements**:
- [ ] Real-time data streaming
- [ ] Multi-format support (JSON, XML, Excel)
- [ ] Database integration
- [ ] Geo-location data integration

---

### 4.2 Duplicate Beneficiary Detection ✓ IMPLEMENTED

**Module**: `models/duplicate_detector.py`, `notebooks/find_duplicates.py`

**Features**:
- ✓ Fuzzy name matching using token sort ratio
- ✓ Configurable similarity threshold (default: 90%)
- ✓ Batch processing for performance
- ✓ Duplicate pair identification with similarity scores

**Algorithm**:
- Uses RapidFuzz library for efficient string matching
- Compares all beneficiary name pairs
- Returns tuples of (id1, id2, similarity_score)

**Configuration**:
```python
DUPLICATE_THRESHOLD = 90  # Adjustable in config.py
```

**Future Enhancements**:
- [ ] Detect shared bank accounts across beneficiaries
- [ ] Detect shared addresses and phone numbers
- [ ] Multi-field matching (name + address + phone)
- [ ] Clustering of suspicious beneficiary groups
- [ ] Phonetic matching for regional name variations

---

### 4.3 Fund Distribution Monitoring ✓ PARTIALLY IMPLEMENTED

**Module**: `models/anomaly_detector.py`, `notebooks/detect_anomalies.py`

**Features**:
- ✓ Isolation Forest anomaly detection
- ✓ Multi-feature analysis (amount, bank count, address count)
- ✓ Configurable contamination rate (default: 5%)
- ✓ Anomaly flagging (-1 for anomalies, 1 for normal)

**Monitored Features**:
- Transaction amounts
- Same bank account frequency
- Same address frequency

**Configuration**:
```python
ANOMALY_CONTAMINATION = 0.05  # Expected outlier proportion
```

**Future Enhancements**:
- [ ] Time-series analysis for approval spikes
- [ ] Geographic clustering of suspicious transactions
- [ ] Scheme-specific anomaly patterns
- [ ] Officer-level approval pattern analysis
- [ ] Seasonal trend detection

---

### 4.4 Risk Scoring & Alerts ✓ IMPLEMENTED

**Module**: `models/risk_scorer.py`, `notebooks/calculate_risk.py`

**Features**:
- ✓ Multi-factor risk score calculation
- ✓ Configurable risk weights
- ✓ High-risk beneficiary identification
- ✓ Risk score statistics and reporting

**Risk Calculation Formula**:
```python
risk_score = (same_bank_count × 2) + 
             (same_address_count × 2) + 
             (is_anomaly × 5)
```

**Risk Weights** (configurable in `config.py`):
```python
RISK_WEIGHTS = {
    "same_bank_count": 2,
    "same_address_count": 2,
    "anomaly_multiplier": 5
}
```

**Future Enhancements**:
- [ ] District-level risk indices
- [ ] Scheme-level risk aggregation
- [ ] Real-time alert system (email/SMS)
- [ ] Risk trend analysis over time
- [ ] Predictive risk modeling

---

### 4.5 Complaint Intelligence ⚠️ PLANNED

**Status**: Basic NLP module exists but not integrated

**Planned Features**:
- [ ] Voice-to-text conversion
- [ ] Sentiment analysis on complaints
- [ ] Urgency classification
- [ ] Topic clustering
- [ ] Corruption hotspot detection
- [ ] Complaint-beneficiary linking

**Technology**:
- Transformers library for NLP
- Sentiment analysis pipeline
- Topic modeling (LDA/BERT)

---

### 4.6 API & Data Access ✓ IMPLEMENTED

**Module**: `backend/app.py`

**Endpoints**:

1. **Health Check**
   ```
   GET /
   Returns: {"status": "API running", "version": "1.0.0"}
   ```

2. **Get Anomalies**
   ```
   GET /anomalies?limit=100&min_risk=5
   Returns: List of anomalous beneficiaries
   ```

3. **Get High-Risk Beneficiaries**
   ```
   GET /risk?threshold=10&limit=100
   Returns: List of high-risk beneficiaries sorted by risk score
   ```

4. **Get Beneficiary Details**
   ```
   GET /beneficiary/{beneficiary_id}
   Returns: Complete beneficiary record with risk data
   ```

**Features**:
- ✓ RESTful API design
- ✓ Query parameter validation
- ✓ Pagination support
- ✓ Error handling with proper HTTP status codes
- ✓ Pydantic models for data validation
- ✓ Structured logging

**Future Enhancements**:
- [ ] Authentication & authorization
- [ ] Rate limiting
- [ ] API key management
- [ ] Batch export endpoints
- [ ] Real-time WebSocket updates

---

### 4.7 Dashboard & Visualization ✓ PARTIALLY IMPLEMENTED

**Module**: `notebooks/heatmap.py`

**Current Features**:
- ✓ Geographic heatmap generation (Folium)
- ✓ Risk score visualization
- ✓ Interactive HTML maps

**Future Enhancements**:
- [ ] Real-time dashboard (React/Vue frontend)
- [ ] Leakage trend charts
- [ ] Flagged beneficiaries table
- [ ] Complaint clustering insights
- [ ] District-wise comparison
- [ ] Scheme performance metrics
- [ ] Drill-down capabilities

---

### 4.8 Administrative Action Support ⚠️ PLANNED

**Planned Features**:
- [ ] Audit trigger recommendations
- [ ] Case investigation workflow
- [ ] Case status tracking
- [ ] Resolution logs
- [ ] Evidence collection interface
- [ ] Report generation

---

## 5. Non-Functional Requirements

### 5.1 Performance ✓ IMPLEMENTED

**Current**:
- ✓ Processes 1000 records in < 1 second
- ✓ Batch processing for duplicate detection
- ✓ Efficient CSV operations
- ✓ Optimized anomaly detection

**Targets**:
- [ ] Real-time anomaly detection (< 100ms per record)
- [ ] Scalable to millions of records
- [ ] Parallel processing support
- [ ] Database indexing for fast queries

---

### 5.2 Security & Privacy ⚠️ PARTIALLY IMPLEMENTED

**Current**:
- ✓ Environment-based configuration
- ✓ No hardcoded credentials
- ✓ Structured logging (no PII in logs)

**Required**:
- [ ] Role-based access control (RBAC)
- [ ] Data encryption at rest and in transit
- [ ] PII anonymization/masking
- [ ] Audit trail for all data access
- [ ] Secure API authentication (OAuth2/JWT)
- [ ] GDPR/data protection compliance

---

### 5.3 Accessibility & Inclusion ⚠️ PLANNED

**Required**:
- [ ] Mobile-friendly interface
- [ ] Local language support (Hindi, regional languages)
- [ ] Voice input support
- [ ] Low-bandwidth optimization
- [ ] Screen reader compatibility
- [ ] Offline mode for field officers

---

### 5.4 Reliability & Availability ⚠️ PLANNED

**Targets**:
- [ ] 99.9% system availability
- [ ] Fault-tolerant architecture
- [ ] Automated backups
- [ ] Disaster recovery plan
- [ ] Health monitoring & alerting
- [ ] Graceful degradation

---

### 5.5 Maintainability ✓ IMPLEMENTED

**Current**:
- ✓ Modular architecture
- ✓ Comprehensive logging
- ✓ Configuration management
- ✓ Error handling
- ✓ Code documentation
- ✓ Reusable components

---

## 6. Data Requirements

### 6.1 Input Data ✓ IMPLEMENTED

**Beneficiary Records**:
- beneficiary_id (unique identifier)
- name, phone, address
- bank_account
- scheme, amount, district, date

**Data Format**: CSV (extensible to JSON, database)

**Data Volume**: Currently 1000 records (scalable to millions)

---

### 6.2 Processed Data ✓ IMPLEMENTED

**Feature Engineering**:
- same_bank_count: Number of beneficiaries sharing bank account
- same_address_count: Number of beneficiaries sharing address

**Model Outputs**:
- anomaly: -1 (anomaly) or 1 (normal)
- risk_score: Calculated risk value

---

### 6.3 Future Data Requirements

- [ ] Transaction history & timestamps
- [ ] Officer approval logs
- [ ] Complaint text & audio data
- [ ] Geographic coordinates (lat/lon)
- [ ] Scheme-specific metadata
- [ ] Historical audit results

---

## 7. Testing Requirements

### 7.1 Implemented Tests ✓

**Current Testing**:
- ✓ Module import validation
- ✓ Pipeline end-to-end execution
- ✓ API endpoint testing
- ✓ Data validation checks
- ✓ Error handling verification

---

### 7.2 Required Tests

**Unit Tests**:
- [ ] Duplicate detection accuracy (precision/recall)
- [ ] Anomaly detection validation
- [ ] Risk score calculation correctness
- [ ] Data loader edge cases
- [ ] API endpoint responses

**Integration Tests**:
- [ ] Complete pipeline execution
- [ ] API-database integration
- [ ] Multi-module workflows

**Performance Tests**:
- [ ] Load testing (1M+ records)
- [ ] API response time benchmarks
- [ ] Concurrent user handling
- [ ] Memory usage profiling

**Accuracy Tests**:
- [ ] Duplicate detection precision/recall
- [ ] Anomaly detection F1 score
- [ ] False positive rate analysis
- [ ] NLP classification accuracy

---

## 8. Success Metrics

### 8.1 Technical Metrics

**Current Capabilities**:
- ✓ Duplicate detection: 90%+ similarity threshold
- ✓ Anomaly detection: 5% contamination rate
- ✓ API response time: < 1 second
- ✓ Pipeline execution: < 2 seconds for 1000 records

**Target Metrics**:
- [ ] Fraud detection accuracy: > 95%
- [ ] False positive rate: < 5%
- [ ] System uptime: 99.9%
- [ ] API response time: < 100ms
- [ ] Complaint resolution efficiency: 50% improvement

---

### 8.2 Business Metrics

**Target Outcomes**:
- [ ] Reduction in welfare leakage: 30-50%
- [ ] Audit response time: 70% reduction
- [ ] Genuine beneficiary inclusion: 95%+
- [ ] Transparency score improvement: 40%+
- [ ] Cost savings: ₹X crores annually

---

## 9. Deployment Requirements

### 9.1 Current Setup ✓

**Local Development**:
- ✓ Python 3.13+ environment
- ✓ Virtual environment (venv)
- ✓ Configuration via environment variables
- ✓ Command-line execution

---

### 9.2 Production Requirements

**Infrastructure**:
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Container orchestration (Docker/Kubernetes)
- [ ] Load balancing
- [ ] Auto-scaling
- [ ] CDN for static assets

**Monitoring**:
- [ ] Application performance monitoring (APM)
- [ ] Log aggregation (ELK stack)
- [ ] Error tracking (Sentry)
- [ ] Uptime monitoring
- [ ] Cost monitoring

---

## 10. Compliance & Governance

### 10.1 Data Governance

**Required**:
- [ ] Data retention policies
- [ ] Data access audit logs
- [ ] PII handling procedures
- [ ] Data quality standards
- [ ] Backup & recovery procedures

---

### 10.2 Regulatory Compliance

**Required**:
- [ ] IT Act 2000 compliance
- [ ] Aadhaar data protection
- [ ] RTI Act transparency
- [ ] State-specific welfare regulations

---

## 11. Future Roadmap

### Phase 1 (Current) ✓
- ✓ Core duplicate detection
- ✓ Anomaly detection
- ✓ Risk scoring
- ✓ Basic API

### Phase 2 (Next 3 months)
- [ ] Complaint intelligence integration
- [ ] Enhanced dashboard
- [ ] Authentication & authorization
- [ ] Database integration
- [ ] Production deployment

### Phase 3 (6-12 months)
- [ ] Predictive analytics
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Advanced visualization
- [ ] ML model improvements

### Phase 4 (12+ months)
- [ ] Real-time streaming analytics
- [ ] Blockchain integration for transparency
- [ ] AI-powered investigation assistant
- [ ] Cross-scheme analysis
- [ ] National-level integration

---

## 12. Dependencies

### 12.1 Python Packages (requirements.txt)

```
pandas              # Data manipulation
numpy               # Numerical computing
scikit-learn        # Machine learning
matplotlib          # Plotting
seaborn             # Statistical visualization
rapidfuzz           # Fuzzy string matching
faker               # Synthetic data generation
fastapi             # Web framework
uvicorn             # ASGI server
python-multipart    # Form data parsing
pydantic            # Data validation
transformers        # NLP models
torch               # Deep learning
folium              # Geographic visualization
plotly              # Interactive plots
boto3               # AWS integration (future)
```

---

## 13. Configuration

### 13.1 Environment Variables

```bash
# Model Parameters
ANOMALY_CONTAMINATION=0.05
DUPLICATE_THRESHOLD=90

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

See `.env.example` for complete configuration template.

---

## 14. Contact & Support

**Project Repository**: https://github.com/mayank7cc/AI-for-Economic-Leakage-Detection-AIforbharat-
**Documentation**: See README.md
**Technical Support**: mayankparab2006@gmail.com

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Living Document - Updated as features are implemented
