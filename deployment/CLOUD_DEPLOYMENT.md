# Cloud Deployment Guide

This guide provides step-by-step instructions for deploying the Threat Intelligence Classifier to either Google Cloud Platform (GCP) or Microsoft Azure.

## Prerequisites

- OpenAI API key
- Elasticsearch instance (Cloud or Self-hosted)
- GCP or Azure account with necessary permissions

## Google Cloud Platform (GCP) Deployment

### 1. Initial Setup

```bash
# Install Google Cloud SDK
# Set up environment
gcloud init
gcloud config set project your-project-id
```

### 2. Secret Management

```bash
# Create secrets
gcloud secrets create OPENAI_API_KEY --data-file=- <<< "your-api-key"
gcloud secrets create ELASTICSEARCH_PASSWORD --data-file=- <<< "your-es-password"

# Grant access
gcloud secrets add-iam-policy-binding OPENAI_API_KEY \
    --member="serviceAccount:your-service-account@your-project.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 3. Elasticsearch Setup

1. Create a Cloud Memorystore instance or use Elastic Cloud
2. Note down the connection details

### 4. Deploy to Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project-id/threat-classifier
gcloud run deploy threat-classifier \
    --image gcr.io/your-project-id/threat-classifier \
    --platform managed \
    --region us-central1 \
    --set-env-vars="ELASTICSEARCH_HOST=your-es-host" \
    --set-secrets="OPENAI_API_KEY=OPENAI_API_KEY:latest,ELASTICSEARCH_PASSWORD=ELASTICSEARCH_PASSWORD:latest"
```

### 5. Set Up Cloud Monitoring

1. Enable Cloud Monitoring API
2. Create custom dashboard for:
   - API latency
   - Request volume
   - Error rates
   - LLM API usage

## Microsoft Azure Deployment

### 1. Initial Setup

```bash
# Install Azure CLI
az login
az account set --subscription your-subscription-id
```

### 2. Create Resource Group

```bash
az group create --name threat-classifier-rg --location eastus
```

### 3. Set Up Azure Key Vault

```bash
# Create Key Vault
az keyvault create --name threat-classifier-kv --resource-group threat-classifier-rg

# Store secrets
az keyvault secret set --vault-name threat-classifier-kv --name OPENAI_API_KEY --value "your-api-key"
az keyvault secret set --vault-name threat-classifier-kv --name ELASTICSEARCH_PASSWORD --value "your-es-password"
```

### 4. Deploy Application

1. Set up Azure DevOps pipeline using provided `azure-deploy.yaml`
2. Configure environment variables in Azure App Service:
   ```bash
   az webapp config appsettings set --resource-group threat-classifier-rg \
       --name threat-classifier \
       --settings OPENAI_API_KEY="@Microsoft.KeyVault(SecretUri=...)" \
       ELASTICSEARCH_HOST="your-es-host"
   ```

### 5. Set Up Application Insights

1. Create Application Insights resource
2. Add instrumentation key to app settings
3. Configure custom metrics for:
   - Classification latency
   - Threat level distribution
   - API usage patterns

## Scaling Considerations

### GCP
- Configure Cloud Run auto-scaling:
  ```bash
  gcloud run services update threat-classifier \
      --min-instances=2 \
      --max-instances=10 \
      --concurrency=80
  ```

### Azure
- Configure App Service scaling rules:
  ```bash
  az monitor autoscale create \
      --resource-group threat-classifier-rg \
      --name threat-classifier-autoscale \
      --min-count 2 \
      --max-count 10 \
      --count 2
  ```

## Monitoring and Alerts

### GCP Monitoring Setup
1. Create uptime checks
2. Set up alert policies:
   - High latency (>2s)
   - Error rate >1%
   - Instance count near max

### Azure Monitoring Setup
1. Configure Application Insights alerts
2. Set up Azure Monitor:
   - Performance metrics
   - Availability tests
   - Custom dashboards

## Backup and Disaster Recovery

### GCP
1. Enable Cloud Storage backups
2. Set up cross-region replication
3. Configure automated backups

### Azure
1. Enable Azure Backup
2. Configure geo-replication
3. Set up automated recovery tests

## Security Considerations

1. Enable HTTPS only
2. Configure network security rules
3. Set up WAF (Web Application Firewall)
4. Implement rate limiting
5. Enable audit logging

## Cost Optimization

1. Configure auto-scaling thresholds
2. Monitor API usage
3. Set up budget alerts
4. Use reserved instances where applicable
5. Implement caching strategies

## Troubleshooting Guide

### Common Issues

1. Deployment Failures
   - Check build logs
   - Verify secret access
   - Validate environment variables

2. Performance Issues
   - Monitor CPU/Memory usage
   - Check Elasticsearch performance
   - Verify LLM API response times

3. Scaling Problems
   - Review auto-scaling logs
   - Check resource quotas
   - Monitor cold start times

### Health Checks

#### GCP
```bash
# Check service health
gcloud run services describe threat-classifier
# View logs
gcloud logging read "resource.type=cloud_run_revision"
```

#### Azure
```bash
# Check app health
az webapp show -g threat-classifier-rg -n threat-classifier
# View logs
az webapp log tail -g threat-classifier-rg -n threat-classifier
```