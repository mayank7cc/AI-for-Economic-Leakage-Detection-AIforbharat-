# System Design Document

## AI for Economic Leakage Detection
### Ensuring Welfare Benefits Reach the Right Citizens

---

## 1. System Overview

The platform is an AI-powered governance intelligence system that analyzes welfare distribution data to detect anomalies, identify fraud patterns, and predict leakage risks for proactive administrative action.

**Current Implementation**: Modular Python-based system with FastAPI backend, scikit-learn ML models, and CSV-based data processing.

**Vision**: Cloud-native, scalable platform with real-time processing, complaint intelligence, and comprehensive dashboards.

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                             │
│  • Beneficiary Records  • Transactions  • Complaints         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                 │
│  • CSV Files (current)  • Future: S3, DynamoDB               │
│  • data/raw/  • data/processed/                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              DATA PROCESSING LAYER                           │
│  • pipeline.py (orchestrator)                                │
│  • notebooks/preprocess.py                                   │
│  • utils/data_loader.py, validators.py                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              AI INTELLIGENCE LAYER                           │
│  • models/anomaly_detector.py (Isolation Forest)             │
│  • models/duplicate_detector.py (Fuzzy Matching)             │
│  • models/risk_scorer.py (Multi-factor Scoring)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 API & BACKEND LAYER                          │
│  • backend/app.py (FastAPI)                                  │
│  • RESTful endpoints                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            VISUALIZATION & INTERFACE                         │
│  • notebooks/heatmap.py (Folium maps)                        │
│  • Future: React.js dashboard                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Component Design

### 3.1 Data Layer

#### Current Implementation

**Storage Structure**:
```
data/
├── raw/
│   └── beneficiaries.csv          # Source data
└── processed/
    ├── processed.csv              # Feature-engineered data
    ├── anomaly_output.csv         # Anomaly detection results
    └── risk_output.csv            # Final risk scores
```

**Data Schema**:
```python
Beneficiary Record:
- beneficiary_id: int (unique identifier)
- name: str
- phone: str
- address: str
- bank_account: int
- scheme: str (Food Subsidy, Farmer Aid, Scholarship)
- amount: int
- district: str
- date: str

Processed Features:
- same_bank_count: int (shared bank account frequency)
- same_address_count: int (shared address frequency)
- anomaly: int (-1 for anomaly, 1 for normal)
- risk_score: float (calculated risk value)
```

**Module**: `utils/data_loader.py`
- CSV reading with error handling
- Schema validation
- Automatic directory creation
- Logging for all operations

#### Future Enhancements
- **Cloud Storage**: Amazon S3 for scalable file storage
- **Database**: DynamoDB for real-time processed data
- **Streaming**: Kafka/Kinesis for real-time ingestion
- **Multi-format**: JSON, XML, Excel support

---

### 3.2 Data Processing Layer

#### Current Implementation

**Pipeline Orchestrator** (`pipeline.py`):
```python
Sequential execution:
1. Data Preprocessing
2. Anomaly Detection
3. Risk Score Calculation
```

**Preprocessing** (`notebooks/preprocess.py`):
- Load raw beneficiary data
- Validate schema and data quality
- Feature engineering:
  - Group by bank_account → same_bank_count
  - Group by address → same_address_count
- Save processed data

**Utilities** (`utils/`):
- `data_loader.py`: Centralized CSV operations
- `validators.py`: Schema and data validation
- `logger.py`: Structured logging setup

**Configuration** (`config.py`):
- Centralized path management
- Environment variable support
- Model parameter configuration
- API settings

#### Design Patterns
- **Modular Design**: Each processing step is independent
- **Error Handling**: Try-catch blocks with logging
- **Configuration Management**: Environment-based settings
- **Logging**: Structured logs for debugging and monitoring

#### Future Enhancements
- **Serverless Processing**: AWS Lambda for scalable execution
- **Parallel Processing**: Multi-threaded/distributed processing
- **Data Streaming**: Real-time processing pipelines
- **Caching**: Redis for intermediate results

---

### 3.3 AI Intelligence Layer

#### 3.3.1 Duplicate Detection

**Module**: `models/duplicate_detector.py`

**Algorithm**: Fuzzy String Matching
```python
class DuplicateDetector:
    - Uses RapidFuzz library
    - Token sort ratio algorithm
    - Configurable threshold (default: 90%)
    - Batch processing for performance
```

**Process**:
1. Compare all beneficiary name pairs
2. Calculate similarity score (0-100)
3. Flag pairs above threshold
4. Return (id1, id2, similarity_score) tuples

**Configuration**:
```python
DUPLICATE_THRESHOLD = 90  # Adjustable in config.py
```

**Performance**:
- Current: O(n²) with batch processing
- Handles 1000 records in ~50 seconds
- Logs progress every 100 records

**Future Enhancements**:
- DBSCAN clustering for entity resolution
- Multi-field matching (name + phone + address)
- Phonetic matching for regional names
- Graph-based duplicate networks
- Vectorized fuzzy matching for O(n log n) performance

---

#### 3.3.2 Anomaly Detection

**Module**: `models/anomaly_detector.py`

**Algorithm**: Isolation Forest
```python
class AnomalyDetector:
    - Scikit-learn IsolationForest
    - Unsupervised learning
    - Contamination rate: 5% (configurable)
    - Random state: 42 (reproducibility)
```

**Features Used**:
- `amount`: Transaction amount
- `same_bank_count`: Bank account sharing frequency
- `same_address_count`: Address sharing frequency

**Output**:
- `-1`: Anomaly detected
- `1`: Normal record

**Configuration**:
```python
ANOMALY_CONTAMINATION = 0.05  # Expected outlier proportion
```

**Model Training**:
- Unsupervised (no labeled data required)
- Fits on entire dataset
- Identifies outliers based on feature isolation

**Future Enhancements**:
- Time-series anomaly detection
- Autoencoder-based deep learning models
- Ensemble methods (Isolation Forest + LOF + One-Class SVM)
- Transaction spike detection
- Geographic clustering analysis
- Officer approval pattern analysis

---

#### 3.3.3 Risk Scoring

**Module**: `models/risk_scorer.py`

**Algorithm**: Multi-factor Weighted Scoring
```python
class RiskScorer:
    risk_score = (same_bank_count × 2) + 
                 (same_address_count × 2) + 
                 (is_anomaly × 5)
```

**Risk Weights** (configurable):
```python
RISK_WEIGHTS = {
    "same_bank_count": 2,
    "same_address_count": 2,
    "anomaly_multiplier": 5
}
```

**Risk Categories**:
- Low Risk: 0-5
- Medium Risk: 6-10
- High Risk: 11+

**Output**:
- Continuous risk score for each beneficiary
- Sortable for prioritization
- Explainable (weighted sum of factors)

**Future Enhancements**:
- Machine learning-based risk prediction (Random Forest, Gradient Boosting)
- District-level risk aggregation
- Scheme-specific risk models
- Temporal risk trends
- Predictive risk scoring (future fraud likelihood)

---

#### 3.3.4 Complaint Intelligence (Planned)

**Status**: Basic NLP module exists but not integrated

**Planned Components**:
- **Speech-to-Text**: AWS Transcribe or Whisper
- **NLP Pipeline**: Transformers library
- **Sentiment Analysis**: Classify complaint urgency
- **Topic Modeling**: LDA or BERT-based clustering
- **Entity Linking**: Connect complaints to beneficiaries

**Workflow**:
```
Voice Complaint → Transcription → Text Processing → 
Sentiment Analysis → Topic Clustering → Risk Linking
```

---

### 3.4 API & Backend Layer

**Module**: `backend/app.py`

**Framework**: FastAPI (async, high-performance)

**Architecture**:
```python
FastAPI Application
├── Pydantic Models (data validation)
├── RESTful Endpoints
├── Error Handling
├── Logging
└── CORS (future)
```

**Endpoints**:

1. **Health Check**
   ```
   GET /
   Response: {"status": "API running", "version": "1.0.0"}
   ```

2. **Get Anomalies**
   ```
   GET /anomalies?limit=100&min_risk=5
   Parameters:
     - limit: Max results (1-1000)
     - min_risk: Minimum risk score filter
   Response: List[Beneficiary]
   ```

3. **Get High-Risk Beneficiaries**
   ```
   GET /risk?threshold=10&limit=100
   Parameters:
     - threshold: Minimum risk score
     - limit: Max results
   Response: List[Beneficiary] (sorted by risk_score desc)
   ```

4. **Get Beneficiary Details**
   ```
   GET /beneficiary/{beneficiary_id}
   Response: Beneficiary (single record)
   ```

**Data Validation**:
```python
class Beneficiary(BaseModel):
    beneficiary_id: int
    name: str
    phone: str
    address: str
    bank_account: int
    scheme: str
    amount: int
    district: str
    date: str
    anomaly: Optional[int]
    risk_score: Optional[float]
```

**Error Handling**:
- 200: Success
- 404: Beneficiary not found
- 500: Server error (with detailed message)

**Future Enhancements**:
- Authentication & Authorization (OAuth2/JWT)
- Rate limiting
- API key management
- WebSocket for real-time updates
- GraphQL endpoint
- Batch export endpoints
- Pagination with cursor-based navigation

---

### 3.5 Visualization & Interface Layer

#### Current Implementation

**Geographic Visualization** (`notebooks/heatmap.py`):
- Folium library for interactive maps
- Risk score-based circle markers
- HTML output for web viewing
- Centered on India (lat: 20.59, lon: 78.96)

**Features**:
- Interactive map with zoom/pan
- Risk score popups
- Configurable marker size based on risk
- Filters high-risk beneficiaries (risk_score > 5)

#### Future Dashboard Design

**Technology Stack**:
- Frontend: React.js or Vue.js
- Charting: Plotly, D3.js
- Maps: Folium, Leaflet
- Analytics: AWS QuickSight (optional)

**Dashboard Components**:

1. **Overview Panel**
   - Total beneficiaries
   - Anomalies detected
   - High-risk count
   - Leakage estimate

2. **Leakage Heatmap**
   - Geographic distribution
   - District-wise risk scores
   - Drill-down capabilities

3. **Flagged Beneficiaries Table**
   - Sortable columns
   - Risk score highlighting
   - Action buttons (investigate, audit)

4. **Complaint Intelligence**
   - Topic clusters
   - Sentiment distribution
   - Urgency timeline

5. **Trend Analytics**
   - Time-series charts
   - Scheme comparison
   - Officer performance

---

## 4. Data Flow Diagram

```
┌──────────────────┐
│  Data Generator  │ (notebooks/data_generator.py)
└────────┬─────────┘
         │ Generates synthetic data
         ▼
┌──────────────────┐
│ beneficiaries.csv│ (data/raw/)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Preprocessing   │ (notebooks/preprocess.py)
│  • Validation    │
│  • Feature Eng   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  processed.csv   │ (data/processed/)
└────────┬─────────┘
         │
         ├─────────────────────┬─────────────────────┐
         ▼                     ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Anomaly Detector │  │Duplicate Detector│  │   Risk Scorer    │
│ (Isolation Forest│  │ (Fuzzy Matching) │  │ (Weighted Sum)   │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         ▼                     │                     │
┌──────────────────┐           │                     │
│anomaly_output.csv│           │                     │
└────────┬─────────┘           │                     │
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │  risk_output.csv │
                     └────────┬─────────┘
                              │
                              ├─────────────────┬─────────────────┐
                              ▼                 ▼                 ▼
                     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
                     │  FastAPI     │  │   Heatmap    │  │   Reports    │
                     │  Endpoints   │  │  Generator   │  │  (Future)    │
                     └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 5. Security & Privacy Design

### 5.1 Current Implementation

**Configuration Security**:
- Environment variables for sensitive settings
- No hardcoded credentials
- `.env.example` for template (actual `.env` in `.gitignore`)

**Logging Security**:
- No PII in log messages
- Structured logging with levels
- Error messages sanitized

**Data Handling**:
- Local file system (development)
- No external data transmission

### 5.2 Production Security Requirements

**Authentication & Authorization**:
- IAM-based role access control
- OAuth2/JWT for API authentication
- Role-based permissions (admin, auditor, viewer)

**Data Protection**:
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- PII anonymization/masking
- Data retention policies

**API Security**:
- Rate limiting (per user/IP)
- API key management
- CORS configuration
- Input validation & sanitization

**Audit & Compliance**:
- Audit logs for all data access
- Immutable log storage
- Compliance with IT Act 2000
- GDPR-style data protection

**Network Security**:
- VPC isolation (AWS)
- Security groups & NACLs
- DDoS protection (CloudFront/WAF)
- Intrusion detection

---

## 6. Scalability & Performance Design

### 6.1 Current Performance

**Metrics**:
- 1000 records processed in < 2 seconds
- API response time: < 1 second
- Duplicate detection: ~50 seconds for 1000 records
- Memory usage: < 500 MB

**Bottlenecks**:
- Duplicate detection: O(n²) algorithm
- Single-threaded processing
- CSV file I/O

### 6.2 Scalability Strategy

**Horizontal Scaling**:
- Containerization (Docker)
- Kubernetes orchestration
- Load balancing (ALB/NLB)
- Auto-scaling based on CPU/memory

**Vertical Scaling**:
- Optimized algorithms (vectorization)
- Batch processing
- Caching (Redis)
- Database indexing

**Cloud-Native Architecture**:
- Serverless processing (AWS Lambda)
- Managed services (SageMaker, Comprehend)
- Elastic storage (S3, DynamoDB)
- CDN for static assets (CloudFront)

**Performance Targets**:
- Process 1M records in < 5 minutes
- API response time: < 100ms (p95)
- Support 1000 concurrent users
- 99.9% uptime

---

## 7. Technology Stack

### 7.1 Current Stack

**Backend**:
- Python 3.13+
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)

**AI/ML**:
- scikit-learn (Isolation Forest)
- RapidFuzz (fuzzy matching)
- Transformers (NLP, planned)
- PyTorch (deep learning, planned)

**Data Processing**:
- pandas (data manipulation)
- numpy (numerical computing)

**Visualization**:
- Folium (geographic maps)
- Plotly (interactive charts, planned)
- Seaborn (statistical plots)
- Matplotlib (basic plotting)

**Utilities**:
- Faker (synthetic data generation)
- pathlib (file path management)
- logging (structured logging)

### 7.2 Future Stack

**Cloud Infrastructure**:
- AWS S3 (object storage)
- AWS Lambda (serverless compute)
- AWS SageMaker (ML model hosting)
- AWS DynamoDB (NoSQL database)
- AWS Comprehend (NLP service)
- AWS Transcribe (speech-to-text)
- AWS QuickSight (analytics dashboard)

**Frontend**:
- React.js (UI framework)
- Redux (state management)
- Axios (API client)
- Chart.js / D3.js (visualization)

**DevOps**:
- Docker (containerization)
- Kubernetes (orchestration)
- GitHub Actions (CI/CD)
- Terraform (infrastructure as code)

**Monitoring**:
- CloudWatch (AWS monitoring)
- Prometheus + Grafana (metrics)
- ELK Stack (log aggregation)
- Sentry (error tracking)

---

## 8. Deployment Strategy

### 8.1 Current Deployment

**Environment**:
- Local development
- Python virtual environment
- Manual execution

**Configuration**:
- `.env` file for settings
- `config.py` for centralized management

### 8.2 Production Deployment

**Containerization**:
```dockerfile
# Dockerfile (planned)
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**CI/CD Pipeline** (GitHub Actions):
```yaml
1. Code push to GitHub
2. Run tests (unit, integration)
3. Build Docker image
4. Push to container registry (ECR)
5. Deploy to Kubernetes/ECS
6. Run smoke tests
7. Monitor deployment
```

**Infrastructure as Code** (Terraform):
- VPC & networking
- ECS/EKS cluster
- RDS/DynamoDB
- S3 buckets
- IAM roles & policies
- CloudWatch alarms

**Deployment Stages**:
1. Development (local)
2. Staging (AWS dev account)
3. Production (AWS prod account)

---

## 9. Monitoring & Observability

### 9.1 Current Monitoring

**Logging**:
- Structured logs with timestamps
- Log levels (INFO, WARNING, ERROR)
- Console output

### 9.2 Production Monitoring

**Application Monitoring**:
- Request/response times
- Error rates
- Throughput (requests/sec)
- Resource usage (CPU, memory)

**ML Model Monitoring**:
- Prediction accuracy
- Model drift detection
- Feature distribution changes
- Inference latency

**Business Metrics**:
- Anomalies detected per day
- High-risk beneficiaries
- API usage by endpoint
- User activity

**Alerting**:
- Error rate > threshold
- API latency > 1 second
- Model accuracy drop
- System downtime

**Tools**:
- CloudWatch (AWS)
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Sentry (error tracking)

---

## 10. Responsible AI & Ethics

### 10.1 Explainability

**Current**:
- Risk scores are weighted sums (fully explainable)
- Anomaly detection provides binary flags

**Future**:
- SHAP values for feature importance
- Reason codes for each alert
- Audit trail for model decisions
- Human-in-the-loop for high-stakes decisions

### 10.2 Fairness & Bias

**Monitoring**:
- Demographic parity checks
- Equal opportunity metrics
- Disparate impact analysis
- Regular bias audits

**Mitigation**:
- Diverse training data
- Fairness constraints in models
- Regular model retraining
- Bias detection in production

### 10.3 Privacy

**Data Minimization**:
- Collect only necessary data
- Anonymize PII where possible
- Aggregate data for analytics

**Consent & Transparency**:
- Clear data usage policies
- Citizen consent mechanisms
- Right to explanation
- Data deletion requests

### 10.4 Accountability

**Audit Logs**:
- All data access logged
- Model predictions recorded
- Administrative actions tracked
- Immutable log storage

**Governance**:
- Model review board
- Ethics committee
- Regular audits
- Incident response plan

---

## 11. Future Enhancements

### Phase 1 (Current) ✓
- ✓ Core duplicate detection
- ✓ Anomaly detection
- ✓ Risk scoring
- ✓ Basic API

### Phase 2 (Next 3-6 months)
- [ ] Complaint intelligence integration
- [ ] React.js dashboard
- [ ] Authentication & authorization
- [ ] PostgreSQL/DynamoDB integration
- [ ] Docker containerization
- [ ] AWS deployment

### Phase 3 (6-12 months)
- [ ] Real-time streaming analytics
- [ ] Predictive risk modeling
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Advanced visualization
- [ ] ML model improvements

### Phase 4 (12+ months)
- [ ] Blockchain for transparency
- [ ] AI-powered investigation assistant
- [ ] Cross-scheme analysis
- [ ] National-level integration
- [ ] Fraud network graph analysis
- [ ] Policy intelligence dashboard

---

## 12. System Constraints & Assumptions

### 12.1 Current Constraints

**Data**:
- CSV-based storage (not scalable)
- Synthetic data (not real-world patterns)
- No historical data
- No geographic coordinates

**Processing**:
- Single-threaded execution
- Batch processing only
- No real-time capabilities

**Infrastructure**:
- Local development only
- No cloud deployment
- No redundancy/failover

### 12.2 Assumptions

**Data Quality**:
- Beneficiary data is reasonably clean
- Unique IDs are truly unique
- Dates are in consistent format

**Usage**:
- Government users have technical literacy
- Internet connectivity available
- English language sufficient (for now)

**Scale**:
- < 1M beneficiaries per state
- < 10K transactions per day
- < 100 concurrent API users

---

## 13. Risk Analysis

### 13.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data quality issues | High | Validation layer, data profiling |
| Model accuracy degradation | High | Monitoring, retraining pipeline |
| System downtime | Medium | Redundancy, auto-scaling |
| Security breach | High | Encryption, access control, audits |
| Performance bottlenecks | Medium | Load testing, optimization |

### 13.2 Operational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| False positives | High | Human review, threshold tuning |
| User adoption | Medium | Training, documentation, support |
| Data privacy violations | High | Compliance checks, anonymization |
| Integration failures | Medium | API versioning, backward compatibility |

---

## 14. Success Criteria

### 14.1 Technical Metrics

- ✓ System uptime: 99.9%
- ✓ API response time: < 100ms (p95)
- ✓ Fraud detection accuracy: > 95%
- ✓ False positive rate: < 5%
- ✓ Process 1M records in < 5 minutes

### 14.2 Business Metrics

- Reduction in welfare leakage: 30-50%
- Audit response time: 70% reduction
- Genuine beneficiary inclusion: 95%+
- Transparency score improvement: 40%+
- Cost savings: Measurable ROI

---

## 15. Conclusion

This design document outlines the current implementation and future vision for the AI-powered economic leakage detection system. The modular architecture enables incremental development while maintaining production-ready code quality.

**Current Status**: Functional prototype with core fraud detection capabilities

**Next Steps**: Cloud deployment, dashboard development, complaint intelligence integration

**Long-term Vision**: Comprehensive, real-time governance intelligence platform

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Maintained By**: Development Team  
**Review Cycle**: Quarterly
