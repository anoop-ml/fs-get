# Samples for get record from SageMaker Feature Store

## Prerequisites

Please make sure the role attached to the notebook instance has the below policies. For this sample the role has

- [AmazonSageMakerFullAccess](https://github.com/awsdocs/amazon-sagemaker-developer-guide/blob/master/doc_source/sagemaker-roles.md)
- [AmazonSageMakerFeatureStoreAccess](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-adding-policies.html)
- AmazonS3FullAccess (limit the permissions to specific buckets)


## Sample Notebooks

- [FS Get via Notebook](get_record.ipynb) -  getrecord from notebook
- [FS Get via SM Endpoint](sm_endpoint_get_record.ipynb) - getrecord from within a SageMaker endpoint
- [Inference Pipeline Sample with FS Get](inf_pipeline/sm_endpoint_pipeline.ipynb) - getrecord as pre-processing step in a SageMaker inference pipeline endpoint


### Others
The notebooks where run from a Amazon SageMaker notebook instance. In general below are the best practices. They can be achieved by maintaining a single instance of boto3 FS object as shown in the samples. 

#### Session credentials
---
As a security best practice, requests to the Feature Store are usually signed using temporary session credentials retrieved periodically from the AWS Security Token Service. These temporary credentials expire every 1 - 12 hours. If this is the case for your application, then your applications need to be designed to make background calls to STS before each set of temporary credentials expire.
 
#### Sharing sessions between requests
---
It is very important to reuse these session credentials between requests to the Feature Store. Some client applications have inadvertently started a new session for every request. Because the Security Token Service is not designed for a high rate of requests from each customer, it rejects requests over an excessive request rate threshold for each customer. In other words, a failure to reuse session tokens between requests will result in very high latency, and a very high rate of errors because of throttling performed by the Security Token Service. Feature Store caches some metadata based on your calling application's session credentials, reusing sessions will help avoid cache misses.
 
#### Persistent connections
---
HTTP supports persistent connections, meaning that once a client sends the server an HTTP request and receives a response, the client will reuse the underlying TCP connection for a later request. TCP connection setup involves extra up-front round-trips between the client and the server, and also something called "window sizing" to "warm up" the connection to fully utilize the available bandwidth between the client and the server. Persistent connections eliminate this measurable setup cost for subsequent requests. Failing to reuse HTTP connections between requests results in significantly higher latency, making it very important to configure clients to use persistent connections.
 
#### Connection keep alive
---
HTTP/1.1 Keep-Alive is the feature that implements persistent connections. It is highly recommended to ensure that your underlying HTTP client library is using Keep-Alive.
 
#### Sharing connection pools throughout a program
---
Sets of spare TCP connections that are available for reuse are commonly referred to as a "connection pool". These are typically managed at the client library instance level, and not at a process-wide level. This makes it important to re-use a connection pool across all instances of the client library, or to simply share the same instance of the client library across the application using patterns like a singleton or using dependency injection. For example, applications which create one client instance per request lose all benefits of connection pooling. It is strongly recommended to share one or a very small number of client instances (and therefore connection pools) throughput an application.
 
#### Pre-warming connections
---
Even with persistent connections, your application may encounter the occasional setup cost at the service side. Cache entries on the server side may expire, or persistent connections are dropped. It is recommended to pre-warm your connections to the Feature Store by sending basic requests periodically. This will ensure that requests on the critical path of your application always have ready connection with direct access to your data.
