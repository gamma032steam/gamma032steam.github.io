---
title: "Google Cloud Professional Cloud Developer Study Guide Notes"
date: 2021-11-24T16:28:15+10:00
draft: false
---

The Professional Cloud Developer exam covers a large, possibly unbounded, amount of content. These notes seek to encapsulate, or at least link out to, everything examinable. 

The notes have a grey background, and each correspond to one of the ninity-one dot-points in the [GCP Professional Cloud Developer Study Guide](https://cloud.google.com/certification/guides/cloud-developer).

Everything's been sourced from [A Cloud Guru](https://acloudguru.com/), [Google Cloud Training on Coursera](https://www.coursera.org/learn/gcp-fundamentals) or the [Google Cloud Docs](https://cloud.google.com/docs) themselves.

## Table of contents

- [Section 1: Designing highly scalable, available, and reliable cloud-native applications](#section-1-designing-highly-scalable-available-and-reliable-cloud-native-applications)
- [Section 2: Building and testing applications](#section-2-building-and-testing-applications)
- [Section 3: Deploying applications](#section-3-deploying-applications)
- [Section 4: Integrating Google Cloud services](#section-4-integrating-google-cloud-services)
- [Section 5: Managing application performance monitoring](#section-5-managing-application-performance-monitoring)

## Section 1: Designing highly scalable, available, and reliable cloud-native applications

1.1 Designing high-performing applications and APIs. Considerations include:

-   Microservices
	-   [_Microservices_](https://cloud.google.com/appengine/docs/standard/python/microservices-on-app-engine) refers to an architectural style for developing applications. Microservices allow a large application to be decomposed into independent constituent parts, with each part having its own realm of responsibility.
	-   Benefits
		- Smaller, more modular codebase and deployments. A/B releases, independent development cycles for each service.
		- Simplifies tangled dependencies.
		- Stronger contracts between services.
		- Easier to split up testing, cost accounting, logging and monitoring.
	- On App Engine, deploy a service per microservice.
-   Scaling velocity characteristics/trade-offs of IaaS (infrastructure as a service) vs. CaaS (container as a service) vs. PaaS (platform as a service)
	-   Tradeoffs
		-   IaaS (Compute Engine)
		-   PaaS (App Engine / GKE)
		-   CaaS (Cloud Run)
		-   FaaS (Cloud Functions)
	-   Scalability
		-   Serverless applications can scale quickly and you only pay for what you use (e.g. Cloud Run, Cloud Functions, App Engine).
		-   Aim for stateless microservices.
		-   You want to [minimize start-up time for scalability](https://cloud.google.com/architecture/scalable-and-resilient-apps#minimize_startup_time). Create images, use containers or improve the app.
		-   With containers, use smaller base images (Alpine) and the builder pattern to minimize their size.
		-   See 5.2 GKE Autoscaling.
		-   GCE can [autoscale managed instance groups](https://cloud.google.com/compute/docs/autoscaler).
		-   App Engine Flexible vs Standard: Standard spins up instances quicker and can have zero instances running. Flexible always has one running. Prefered standard for spiky or low traffic.
-   Geographic distribution of Google Cloud services (e.g., latency, regional services, zonal services)
	-   Regions have three or more zones. Those zones have high-bandwidth, low-latency connections.
	-   Deploy to multiple zones for high-availability and fault-tolerance.
	-   Zonal services: VM instances, GKE Regional clusters.
	-   Regional services: Most serverless tech (Cloud Functions, Cloud Run) Static IPs, GKE Zonal clusters.
	-   Persistent Disks & Cloud SQL are zonal, but can sychronously replicate and become regional.
	-   [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones).
-   Defining a key structure for high-write applications using Cloud Storage, Cloud Bigtable, Cloud Spanner, or Cloud SQL
	-   Cloud Storage: don't name objects similarly.
	-   Cloud Bigtable: one key per table. You can put multiple keys into this one key and seperate them with hashes for more distributed reads.
	-   Cloud Spanner: Create second indexes and interleave related records for faster lookups.
	-   CloudSQL: Create secondary indexes or clustered indexes.
-   User session management
	-  Authentication
		-  Integrate Google Sign-in with OAuth 2.0 / OpenID.
		-  Better to use a third-party provider.
-   Caching solutions
	-   Memorystore: managed in-memory caching. Redis & memcached, so you can read and write from your application code.
	-   Cloud CDN: Reduce latency by caching at the edge.
-   Deploying and securing API services
	-   Secure images
		-   Keep images up-to-date.
		-   Consider who you're trusting.
		-   Can do this in CI.
	-   CI
		-   Build, create artifacts, test, run securty checks, deploy.
	-   Design
		-   Use an API schema.
		-   Cloud Endpoints / API Gateway: logging, monitoring, API keys, authentication.
		-   Cloud Endpoints: runs in Cloud Run, works for most GCP services.
		-   API Gateway: managed serverless gateway, simpler to set up.
-   Loosely coupled asynchronous applications (e.g., Apache Kafka, Pub/Sub)
	-   Decouples application dependency. Great if components fail, you need multiple consumers of data, or an async workflow.
	-   Many-to-many, one-to-many, many-to-one patterns.
	-   Pull (default): subscriber makes a request to check for new messages.
	-   Push: topic hits a HTTP endpoint.
	-   Pub/Sub gives you implicit at-least-once delivery per subscription.
	-   Use Cloud Tasks for more explicit notification, with retries & scheduling.
-   Graceful shutdown on platform termination
	-   Flush logs.
	-   Close file descriptors and database connections.
	-   GKE: on graceful shutdown, calls a preStop hook -> a SIGTERM is recieved -> grace period -> SIGKILL.
	-   Cloud functions: delete any temporary files, as these are stored in memory and can be carried over between runs.
	-   [Cloud Tech Video: Terminating with Grace (Kubernetes)](https://youtu.be/Z_l_kE1MDTc).
	-   [Docs: Graceful Shutdown on Cloud Run](https://cloud.google.com/blog/topics/developers-practitioners/graceful-shutdowns-cloud-run-deep-dive).
-   Google-recommended practices and documentation
	-   [Docs: Patterns for scalable and resilient apps](https://cloud.google.com/architecture/scalable-and-resilient-apps).

1.2 Designing secure applications. Considerations include:

-   Implementing requirements that are relevant for applicable regulations (e.g., data wipeout)
	-   Per-industry regulations on data storage regions, encryption and PII.
	-   Cloud Data Loss Prevention: discovers and protects sensitive data.
-   Security mechanisms that protect services and resources
	-   IAM: Divide into folders per-team and a projects per-environment. One project per application per environment. Assign least privilege.
	-   VPC Firewall Rules: Direction (ingress/egress), priority (lower number is higher), action (allow/deny), status, target, source, protocol/port.
		-   Helps define what traffic reaches your resources.
	-   VPC Service Controls: Controls ingress and egress for an entire service perimiter, which houses the resources in a project.
-   Security mechanisms that secure/scan application binaries and manifests
	-   Cloud Web Security Scanner: crawls a site for vulnerabilities.
	-   [Container Scanning](https://cloud.google.com/container-analysis/docs/container-scanning-overview): available on-demand or as part of container registry.
-   Storing and rotating application secrets and keys (e.g., Cloud KMS, HashiCorp Vault)
	-   Cloud KMS: Integrated with GCP services. Can run cryptographic operations but not actually use the keys.
	-   Cloud Secret Manager: Store API keys and credentials you need to download at runtime here.
	-   Both do key rotation (limits exposure, shut down keys if they're exposed).
-   Authenticating to Google services (e.g., application default credentials, JSON Web Token (JWT), OAuth 2.0)
	-   Application default credentials: credentials from the service account you attached to the service.
	-   JWT: alternative to OAuth 2.0 for some GCP APIs.
	-   OAuth 2.0: See 4.2.
-   IAM roles for users/groups/service accounts
	-  Use predefined roles or create custom roles with the permissions you choose.
	-  Easily combine roles into a new one from the Cloud Console.
	-  Prefer to apply roles to Google groups.
-   Securing service-to-service communications (e.g., service mesh, Kubernetes Network Policies, and Kubernetes namespaces)
	-   Service mesh: add a sidecar container to pods. Controlls ingress & egress. Security, load-balancing, traffic control, metrics and more.
	-   [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/): object that controls ingress and egress from a pod. Specify allowed IP ranges, namespaces and pods. 
-   Running services with least privileged access (e.g., Workload Identity)
	-   Create GCP service accounts to use instead of the Default Compute Service Account. Assign it access to only the services and scope it needs.
	-   See 4.2 workload identity.
-   Certificate-based authentication (e.g., SSL, mTLS)
	-   mTLS
		-   A two-way authentication protocol (mutual TLS).
		-   Possible to use mTLS as opposed to service account keys.
		-   Automatically done by Istio between GKE pods.
	- SSL
		- An encryption protocol required for HTTP(S) and SSL load balancers. Can be Google or self-managed.
		- [Docs: SSL certificates overview](https://cloud.google.com/load-balancing/docs/ssl-certificates).
-   Google-recommended practices and documentation
	-   [Docs: Best pratices for enterprise organizations](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations).
	-  [Whitepaper: Google Cloud security foundations guide](https://services.google.com/fh/files/misc/google-cloud-security-foundations-guide.pdf).

1.3 Managing application data. Considerations include:

-   Defining database schemas for Google-managed databases (e.g., Firestore, Cloud Spanner, Cloud Bigtable, Cloud SQL)
	-   Firestore: schemaless.
		-   'Collections' are a group of related 'Documents', which should be kept lightweight.
		-   To do this you can define hierarchical subcollections, which are collections associated with a document.
		-   [Docs: Firestore Data Model](https://firebase.google.com/docs/firestore/data-model).
	-   Datastore:
		-   Entities have a unique key. An entity group is an entity and its descendants.
		-   Generally, Firestore (Firestore in native mode) is preferred over Datastore (Firestore in datastore mode).
	-   Cloud SQL: standard DDL.
	-   Cloud Spanner: extended DDL, with some extra features including table interleaving.
		-   [Docs: Spanner Schema and Data Model](https://cloud.google.com/spanner/docs/schema-and-data-mode)
	-   Bigtable: NoSQL (wide, data fields are optional). Broken into column families.
		-   [Docs: Bigtable Scema Design](https://cloud.google.com/spanner/docs/schema-and-data-mode).
	-  Also see 1.1 choosing a key structure.
-   Choosing data storage options based on use case considerations, such as:
    -   Time-limited access to objects
		- [Signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls): GCS URLs that provide temporary acccess.
    -   Data retention requirements
		-   Use the GCS storage tiers and Object Lifecycle Management rules to move between them automatically.
		-   Object holds (for retention) and policy locks (that can't be removed).
		-   Unmodified BigQuery partitions get a 50% discount after 90 days.
    -   Structured vs. unstructured data
		-   Use GCS for unstructured data.
    -   Strong vs. eventual consistency
		-   Spanner, Firestore for strong consistency.
    -   Data volume
    		-   Switch off CloudSQL above the tens of TB mark.
    -   Frequency of data access in Cloud Storage
		-   Nearline: 30 days, Coldline: 90 days, Archive: 365 days
		-   Storage price goes down, retrieval price goes up.
-   Google-recommended practices and documentation
	-   [Blog: Choosing the right compute option in GCP: a decision tree](https://cloud.google.com/blog/products/compute/choosing-the-right-compute-option-in-gcp-a-decision-tree).

1.4 Application modernization. Considerations include:

-   Using managed services
	-   App engine standard: predefined runtimes.
	-   App engine flex: any runtime or container.
	-   Cloud functions: even-driven model.
	-   Cloud run: runs a stateless container.
-   Refactoring a monolith to microservices
	-   Strangler pattern: abstract and replace component-by-component.
-   Designing stateless, horizontally scalable services
	-   Split services into a clean seperation of those that are stateless and stateful. Stateless services are easier to scale.
-   Google-recommended practices and documentation
	-   [GCP Application Modernisation](https://cloud.google.com/solutions/application-modernization)
	-  [DevOps tech: Architecture](https://cloud.google.com/architecture/devops/devops-tech-architecture)
	-  [Aim for statelessness](https://cloud.google.com/architecture/scalable-and-resilient-apps#aim_for_statelessness)

## Section 2: Building and testing applications

2.1 Setting up your local development environment. Considerations include:

-   Emulating Google Cloud services for local application development
	-   Use the [GCP beta emulators](https://cloud.google.com/sdk/gcloud/reference/beta/emulators) on your local machine for BigTable, Datastore, Firestore, Pub/Sub and Spanner.
-   Creating Google Cloud projects
	-   Create a Project optionally under a folder, which are optionally under an Organisation Node.
	-  Project name: You choose it. Can change it.
	-  Project ID: You choose it. Can't change it.
	-  Project number: GCP chooses it. Can't change it.
-   Using the command-line interface (CLI), Google Cloud Console, and Cloud Shell tools
	-   CLI: gcloud, gsutil (Cloud Storage), bq (BigQuery), cbt (BigTable) command-line tools.
	-   Cloud shell: browser-based CLI and editor.
-   Using developer tooling (e.g., Cloud Code, Skaffold)
	-   Cloud Code (Skaffold): IDE extension for GCP development (easy deployments to GKE/Cloud Run for example).

2.2 Writing efficient code. Considerations include:

-   Algorithm design
	-   Minimise time complexity.
	-   Knowledge of basic data structures (linked lists, hash tables, arrays, search trees) and their advantages.
-   Modern application patterns
	- [12 Factor App](https://12factor.net/)
-   Software development methodologies
	-   Agile > waterfall.
	-   Prefer faster deployments and iterations.
	-   Test-driven development: write tests before code.
	-   Infrastructure as code: define Cloud resource with code.
-   Debugging and profiling code
	-   See 5.3, Cloud Trace and Cloud Debugger

2.3 Testing. Considerations include:

-   Unit testing
	-   Test a component in isolation
	-   Find easy-to-spot errors
	-   Automate your tests!
-   Integration testing
	-   Group components together, include dependencies
-   Performance testing
	-   Measure latency
-   Load testing
	-   Place under heavy load, maybe for a long period and test scalability

2.4 Building. Considerations include:

-   Source control management
	-   Store code with git in Cloud Source Repositories. You can set up Cloud Build triggers to run when changes are pushed to certain branches.
-   Creating secure container images from code
	-   Add security scanning the CI process. You can add this as a Cloud Build step and call Container Registry on-demand, check the severity level and fail if it's too high.
	-   Use Google's managed base images, and build on top of those.
	-   [Jib](https://github.com/GoogleContainerTools/jib): creates optimized Docker images from Java applications
-   Developing a continuous integration pipeline using services (e.g., Cloud Build, Container Registry) that construct deployment artifacts
	- Cloud Build: fully managed, serverless container building. Can deploy to GCP, can create triggers, configured in YAML.
		- Each Cloud Build step in a pipeline is a Docker container.
		- [Pass data between steps](https://cloud.google.com/build/docs/configuring-builds/pass-data-between-steps) by writing to the `/workspace` directory.
	- Spinnaker: CD for compute, containers, multi-cloud. E.g. set up a process for canary deployments.
	- Tekton: CI/CD for k8s.
	- Anthos Config Manager: matches the k8s environment to the config in a repo.
	- Jenkins: Older kitchen sink.
-   Reviewing and improving continuous integration pipeline efficiency
	-   See [DevOps tech: Continious Integration](https://cloud.google.com/architecture/devops/devops-tech-continuous-integration).
	-   Metrics include: proportion of commits that trigger a build, test pass rate, build fix time, availability of feedback.
	-   Improvements include: increasing velocity of deployments/merges, automation, build duration (< 10 minutes), broken builds/tests, pulling in code outside the repo.

## Section 3: Deploying applications

3.1 Recommend appropriate deployment strategies using the appropriate tools (e.g., Cloud Build, Spinnaker, Tekton, Anthos Configuration Manager) for the target compute environment (e.g., Compute Engine, Google Kubernetes Engine). Considerations include:

-   Blue/green deployments
	-   Run two deployments at once. Switch the load balancer to the new version. Really easy to switch back if there's an issue.
	-   GKE: Create a new deployment, test, then update the service selector. See [Deployment Strategies on GKE](https://cloud.google.com/architecture/implementing-deployment-and-testing-strategies-on-gke).
-   Traffic-splitting deployments
	-   Useful for A/B testing.
	-   Can be done in the console for App Engine.
	-   GKE: Use Istio, or deploy some of the pods with the new version. May need session affinity.
-   Rolling deployments
	-  GCE: Can roll out new instance templates in a MIG.
	-  GKE: Apply an updated deployment. Pods will be recreated. Can set a rollingUpdate strategy with a maxUnavailable, and maxSurge (extra pods) to minimise distruption.
-   Canary deployments
	-   For features that are best tested in prod.
	-   GKE: Same as traffic-splitting.


3.2 Deploying applications and services on Compute Engine. Considerations include:

-   Installing an application into a virtual machine (VM)
	-   SSH in and install, or use a startup script.
-   Managing service accounts for VMs
	-   By default, uses the Compute Engine Default Service Account.
		-   Not recommended in pratice: it gives too broad of a permission set (project editor).
	-   Best to create a custom service account.
-   Bootstrapping applications
	-  Provide a startup & shutdown script.
		-   Can pass a startup script as a `startup-script-url` metadata tag, or add it directly.
-   Exporting application logs and metrics
	-   Install the Cloud Logging agent (Stackdriver). It collects logs from a few standard places, including syslog, by default. The logging standard is fluentd.
	-   System metrics (CPU util, networking), are reported to Cloud Monitoring automatically.  You can also make your own metrics based on logs.
-   Managing Compute Engine VM images and binaries
	-   Can create an image based on a VM's persistent disk, and then re-use it.
		-  You can query the metadata server inside the VM to use as environment variables.
	-  Managed instance groups: create an instance 'template' off an image. Autoscales, autoheals and can be used with a load balancer.
		- Option for stateless/stateful (preserves data)/unmanaged.
		- Can autoheal based on a health check.

3.3 Deploying applications and services to Google Kubernetes Engine (GKE). Considerations include:

-   Deploying a containerized application to GKE
	-   Create a deployment based off an image in Container Registry.
-   Managing Kubernetes RBAC and Google Cloud IAM relationships.
	-   [RBAC](https://cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control): A role can perform operations on specific resources.
	-   Grant roles to GCP accounts or service accounts. Define a k8s Role object then a RoleBinding one to attach it to the user.
	-   Service-to-service IAM
		-  See 4.2 Workload Identity.
-   Configuring Kubernetes namespaces
	-   Runs in the default namespace by default.
	-   Create new ones for environments/teams.
-   Defining workload specifications (e.g., resource requirements)
	- Requests: what the container will get (minimum). K8s will only schedule the pod if it can assign enough resources.
		- If the resource request is larger than what is available on the nodes, the pod will never be scheduled.
	- Limits: how much resources a container consume before being restricted (maximum).
		- Memory limits stop the pod with an out of memory error if you run out.
		- CPU limits throttle the pod if you hit the limit.
	- ResourceQuotas: Maximum combined requests & limits from a namespace. A common pattern is to have an unbounded resources in prod, and bounded in non-prod. 
	- LimitRange: Set the minimum and maximum container limits. Prevents having pods that are too small or too large.
	- [Cloud Tech Video: Resource Requests & Limits](https://www.youtube.com/watch?v=xjpHggHKm78)
	- If persistent disks are needed, use a `StatefulSet`.
-   Building a container image using Cloud Build
	-   Have the Cloud Build YAML build and publish the container to Container Registry.
-   Configuring application accessibility to user traffic and other services
	-   Check VPC firewall rules, resource region and IAM permissions.
	-   [Docs: Troubleshooting common networking issues](https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-networking).
-   Managing container life cycle
	-   Pod state: Pending (being created, waiting for resources) -> Running -> Succeeded/Failed.
	-   Can set a restart policy to recreate if it fails with exponential backoff.
	-   Container state: Waiting -> Running -> Terminated.
	-   You can rollback deployments.
	-   Probes
		-   LivenessProbe: lets k8s know if the pod is alive or dead. Great at solving deadlocks.
		-   ReadinessProbe: probe must pass before traffic is sent to a container.
		-   These can be HTTP, TCP or commands that run in the pod.
		-   [Cloud Tech Video: Kubernetes Health Checks with Readiness and Liveness Probes](https://www.youtube.com/watch?v=mxEvAPQRwhw&)
-   Define Kubernetes resources and configurations
	-   Prefer the declarative method: use YAML files and `kubectl apply -f`. 

3.4 Deploying a Cloud Function. Considerations include:

-   Cloud Functions that are triggered via an event from Google Cloud services (e.g., Pub/Sub, Cloud Storage objects)
	-   Pub/sub messages, cloud storage uploads, firestore updates are all predefined triggers. Called 'background functions'.
	-   Respond to some data in a context. What's sent through depends on the event.
-   Cloud Functions that are invoked via HTTP.
	-   Use the function as a webhook. Easy to integrate with other services (Slack, GitHub).
	-   Supports the basic HTTP verbs.
	-   [Docs: HTTP Functions (Cloud Functions)](https://cloud.google.com/functions/docs/writing/http).
-   Securing Cloud Functions
	-   Perefer IAM. You can assign invoker permissions per-function. You can then send through an OAuth token in the header.
	-   If not, use OAuth 2.0.
	-   For HTTP functions, consider requiring HTTPS and restricting CORS.
	-   VPC: By default allows ingress and egress from the project and internet. You could restrict this.
	-   [Cloud Functions: Handling CORS Requests](https://cloud.google.com/functions/docs/writing/http#preflight_request)
	-   [Securing Cloud Functions (docs)](https://cloud.google.com/functions/docs/securing)

3.5 Using service accounts. Considerations include:

-   Creating a service account according to the principle of least privilege
	-   See 1.2 Running services with least privilege access.
-   Downloading and using a service account private key file
	-   Download the JSON key file, but don't commit it to code (prefer KMS).

## Section 4: Integrating Google Cloud services

4.1 Integrating an application with data and storage services. Considerations include:

-   Read/write data to/from various databases (e.g., SQL)
	-   [Bigquery SQL syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax).
-   Connecting to a data store (e.g., Cloud SQL, Cloud Spanner, Firestore, Cloud Bigtable)
	-   Cloud SQL: use the [Cloud SQL proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy) to authenticate yourself with IAM. In GKE, run it in a seperate conatiner in the pod.
		-   You can also use a private IP (available to all services in the VPC) and public IP (whitelist allowed clients).
	-   Firestore: client libraries will update live by default and send diffs. Doesn't use much power. [Video: To Realtime or Not?](https://www.youtube.com/watch?v=3aoxOtMM2rc)
	-   Use the client libraries. In some environments you can just pick up the service account permissions automatically. Otherwise download the service account credentials (json) and pass them through.
-   Writing an application that publishes/consumes data asynchronously (e.g., from Pub/Sub)
	-   See 1.1 Loosley Coupled Applications.
-   Storing and retrieving objects from Cloud Storage
	-    [GCS optimisation](https://cloud.google.com/blog/products/gcp/optimizing-your-cloud-storage-performance-google-cloud-performance-atlas): batch uploads with `-m`,  object-compose large files, don't name files similarly, do large reads.
	-    Signed URL uploads: request a signed URL to HTTP PUT to. Good for file upload APIs exposed to users.
	-    Also see 1.1 Defining a key structure and 1.3.

4.2 Integrating an application with compute services. Considerations include:

-   Implementing service discovery in GKE and Compute Engine
	-   GCE: Either use the metadata server, or hit a DNS name from a load balancer.
	-   GKE
		-   Endpoints
			-   Connect to an IP via a connection string, as opposed to hard-coding the IP.
			-   If it's a DNS name, use an `ExternalName` service.
		-   Kubernetes Services
			1. `ClusterIP`: Expose an IP to the cluster.
			2. `NodePort`: Expose an IP of each node at a specific port.
			3. `LoadBalancer`: Expose externally with a cloud LB.
	- In GCP, this is a regional network LB. Use an ingress object for a global LB.
	-   [Cloud Tech Video: Mapping External Services (Kubernetes)](https://youtu.be/fvpq4jqtuZ8).
-   Reading instance metadata to obtain application configuration
	-   You can hit the metadata server with HTTP and recieve key-value pairs.
	-   Pass metadata value into start-up scripts to avoid brittle designs.
-   Authenticating users by using OAuth2.0 Web Flow and Identity-Aware Proxy
	-   [Identity-Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview): auth (Google sign-in) + authorization (IAM) for GCP services.
	-   [Oauth 2.0 Flow](https://developers.google.com/identity/protocols/oauth2): request a token or authorization code (that can later be used to request a token) from Google. The user sees a prompt for consent. If they accept, you get a token you can send in the auth header of API calls.
-   Authenticating to Cloud APIs with Workload Identity
	-   A GKE concept to link Kubernetes service accounts with Google ones.
	-   [Setup steps](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity): create the service accounts, apply the roles and a policy binding to the Google one, annotate the Kubernetes one.

4.3 Integrating Cloud APIs with applications. Considerations include:

-   Enabling a Cloud API
	-   `gcloud services enable` or via the Console.
-   Making API calls using supported options (e.g., Cloud Client Library, REST API or gRPC, APIs Explorer) taking into consideration:
    -   Batching requests
		-   Pub/Sub, GCS, DataFlow and more support batch ingestion.
    -   Restricting return data
		-   Use an API schema.
    -   Paginating results
		-   User asks for a page in the request. Design APIs with this from the beginning.
		-   [Docs: API Design Patterns](https://cloud.google.com/apis/design/design_patterns#list_pagination).
    -   Caching results
		-   See 1.1 Caching Solutions.
    -   Error handling (e.g., exponential backoff)
		-   Exponential backoff: limit to a point. Only retry on transient errors (too many requests, timeouts), not errors that won't change between runs (authentication issues).
		-   The client APIs automatically backoff exponentially.
		-   [Docs: Retry Strategy](https://cloud.google.com/storage/docs/retry-strategy).
-   Using service accounts to make Cloud API calls
	-   See 1.2 Running services with least privlidged access.

## Section 5: Managing application performance monitoring

5.1 Managing Compute Engine VMs. Considerations include:

-   Debugging a custom VM image using the serial port
	-   Serial port logs are useful for crashes, failed boots, startup issues, or shutdown issues.
	-   You can set an instance metadata flag to send these logs to Cloud Logging.
-   Diagnosing a failed Compute Engine VM startup
	-   Common problems: invalid startup script, insufficent access to start up script (e.g. GCS permissions), network tags.
	-   Common MIG problems: invalid templates (image does not exist), assigning a disk to multiple VMs to write, failing health-check (network tags).
-   Sending logs from a VM to Cloud Logging
	-   See 3.2.
-   Viewing and analyzing logs
	-   See 3.2.
-   Inspecting resource utilization over time
	-   See 3.2.

5.2 Managing Google Kubernetes Engine workloads. Considerations include:

-   Configuring logging and monitoring
	- System and app logs are sent by default.
	- [Prometheus](https://cloud.google.com/stackdriver/docs/solutions/gke/prometheus) is a monitoring agent for Kubernetes that runs as a sidecar pod.
-   Analyzing container life cycle events (e.g., CrashLoopBackOff, ImagePullErr)
	-   ErrImagePull: Couldn't get the container image from the registry (doesn't exist, invalid tag).
	-   ImagePullBackOff: Didn't have permission to get the container image.
	-   CrashLoopBackOff: Pod failed to create even after the restart policy (container or configuration bug).
-   Viewing and analyzing logs
	-   Full support for the entire operations suite (Logging, Monitoring, Trace, etc).
-   Writing and exporting custom metrics
	- Install the Custom Metrics Adapter to the cluster. Modify app code to export a metric.
	- You can also set up uptime checks and process health checks from within Cloud Monitoring.
-   Using external metrics and corresponding alerts
	-   Can autoscale on metrics from other GCP services.
-   Configuring workload autoscaling
	-  Set up a `HorizontalPodAutoscaler` object based on a metric (existing, custom or external). Changes the number of pods running the workload.
	-  Vertical Pod Autoscaler. Changes the resources given to pods.
	-  If you want to use both, use Multidimensional Pod Autoscaling.
	-  Cluster autoscaling
		-   [Cluster autoscaler](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler). Changes the number of nodes in the cluster.
		-   Node Auto Provisioner. Changes the resources given to nodes.
	-   [Cloud Tech Video: Introduction to GKE Autoscaling](https://www.youtube.com/watch?v=cFhch7hozRg).

5.3 Troubleshooting application performance. Considerations include:

-   Creating a monitoring dashboard
	-   GCE/GKE dashboard by default.
	-   Can create your own dashboard with metrics.
-   Writing custom metrics and creating log-based metrics
	-   Custom metrics: set up the descriptor then write it to the logging agent.
	-   Logs-based metrics: set up in Cloud Logging.
-   Using Cloud Debugger
	-   Injects snapshots (breakpoints) and log points (to Cloud Logging, without updating app code) into long-running applications.
-   Reviewing stack traces for error analysis
	-   Error Reporting: holds error logs and groups them up per-issue. 
-   Exporting logs from Google Cloud
	-  Log sinks: sends to the default logs bucket, and can be configured to send to other sinks (BigQuery, Pub/Sub, other buckets).
-   Viewing logs in the Google Cloud Console
	-   Types of logs
		-   Platform logs.
		-   User logs (e.g. GCE logging agent logs).
		-   Security logs, includes audit logs (system logs, admin activities) and access transparency logs (GCP staff working on your project). Kept for 400 days.
		-   Multi-cloud logs (e.g. AWS logs).
	-   Logs explorer (in the console): build a query, visualise.
-   Reviewing application performance (e.g., Cloud Trace, Prometheus, OpenTelemetry)
	-   Open Telemetry/Open Census/GCP Client libraries send telemetry to Cloud Trace.
	-   Helps you track round-trip-time around the entire tech stack, visualised in spans.
	-   Can evaluate responsiveness, identify bottlenecks.
-   Monitoring and profiling a running application
	-   Cloud Monitoring workspace runs in a host project.
	-   Resources have default metrics.
	-   Alerting: notifications based on metrics.
	-   Cloud Monitoring uptime checks: hit an endpoint, verify certificate, can do auth.
-   Using documentation, forums, and Google Cloud support
	-   [GCP quotas](https://cloud.google.com/compute/quotas) are increased by raising a request with GCP. For example, quotas apply to VM numbers and the CPUs/GPUs/Disks that are attached to them.
