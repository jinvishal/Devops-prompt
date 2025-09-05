# 50 Daily DevOps Prompts

Here is a list of 50 practical, real-world daily prompts for DevOps engineers, focusing on Docker, Terraform, AWS, Kubernetes, CI/CD, GitOps, monitoring, and security.

### Docker & Containerization

**1. Dockerfile Optimization**
*   **Scenario:** The development team has complained that the Docker image for the new Python web service is over 800MB, causing slow build times and high storage costs. Your task is to optimize it.
*   **Task:** Optimize the provided Python application's Dockerfile using multi-stage builds to significantly reduce the final image size.
*   **Acceptance Criteria:**
    *   The final Docker image size is reduced by at least 30%.
    *   The new Dockerfile uses at least two stages (e.g., a `builder` stage and a `final` stage).
    *   The application remains fully functional after the changes.
    *   The final image uses a slim base image (e.g., `python:3.9-slim`).

**2. Local Development with Docker Compose**
*   **Scenario:** A new developer is joining the team and needs to get the project's microservices stack running on their local machine quickly. The stack consists of a web frontend, a backend API, a database, and a cache.
*   **Task:** Write a `docker-compose.yml` file to spin up a local development environment with four services: a Node.js web app, a Python API, a PostgreSQL database, and a Redis cache.
*   **Acceptance Criteria:**
    *   Running `docker-compose up` successfully starts all four containers.
    *   The web app container can communicate with the API container.
    *   The API container can communicate with the database and cache containers.
    *   Data in the PostgreSQL database is persisted across restarts using a volume.

**3. Container Debugging**
*   **Scenario:** After a recent deployment, the `user-authentication` service container fails to start, exiting immediately with code 1. The CI/CD pipeline is blocked, and developers cannot test their new features.
*   **Task:** A container is exiting immediately upon startup. Investigate the container's logs and metadata to find the root cause and fix the issue.
*   **Acceptance Criteria:**
    *   The root cause of the container exit is identified and documented.
    *   The issue (e.g., a faulty command, a missing config file) is resolved.
    *   The container starts successfully and remains in a running state.
    *   The command `docker logs <container_name>` was used to find the error message.

**4. Implementing Health Checks**
*   **Scenario:** The container orchestrator is restarting the `order-processing` service even when the application inside is just temporarily busy or initializing. This is causing cascading failures. You need to provide a more accurate health signal.
*   **Task:** Implement a `HEALTHCHECK` instruction in the Dockerfile for a Java web service to ensure the application inside is fully responsive before the orchestrator marks it as "healthy."
*   **Acceptance Criteria:**
    *   The `HEALTHCHECK` instruction is added to the service's Dockerfile.
    *   The health check command targets a specific health endpoint (e.g., `curl -f http://localhost:8080/health || exit 1`).
    *   The `interval`, `timeout`, and `retries` for the health check are appropriately configured.
    *   When the application is running, `docker inspect` shows the container's health status as "healthy."

**5. Container Vulnerability Scanning in CI/CD**
*   **Scenario:** As part of a new security initiative, all container images must be scanned for known vulnerabilities before being deployed to production. Your task is to integrate this scanning into the CI/CD process.
*   **Task:** Integrate Trivy into a CI/CD pipeline script to scan a container image for vulnerabilities. The pipeline must fail if any critical issues are found.
*   **Acceptance Criteria:**
    *   A new stage/step is added to the CI pipeline that runs `trivy image <your-image-name>`.
    *   The script is configured to fail the build (`exit 1`) if Trivy finds any `HIGH` or `CRITICAL` severity vulnerabilities.
    *   The pipeline successfully passes if no critical vulnerabilities are found.
    *   A report of the scan results is generated as a build artifact.

**6. Graceful Startup with an Entrypoint Script**
*   **Scenario:** The `api-server` container often fails to start because it attempts to connect to the PostgreSQL database before the database container is fully initialized and ready to accept connections.
*   **Task:** Create a custom `entrypoint.sh` script that waits for the PostgreSQL database to be ready before starting the main application process.
*   **Acceptance Criteria:**
    *   An `entrypoint.sh` script is created.
    *   The script uses a tool like `pg_isready` or a simple loop with `nc` to check the database connection.
    *   The Dockerfile is updated to use this new entrypoint script (`ENTRYPOINT ["/app/entrypoint.sh"]`).
    *   The application container now waits successfully for the database container to become healthy before starting.

### Terraform & Infrastructure as Code (IaC)

**7. Provision a Secure S3 Bucket**
*   **Scenario:** The security team requires that all new S3 buckets used for storing application logs must adhere to strict security and compliance standards from day one.
*   **Task:** Write a Terraform script to provision a secure S3 bucket specifically for storing logs. The bucket must have versioning, server-side encryption, and access logging enabled.
*   **Acceptance Criteria:**
    *   The Terraform script successfully creates an S3 bucket when `terraform apply` is run.
    *   The created bucket has versioning enabled.
    *   The bucket is configured with default server-side encryption (SSE-S3).
    *   Access logging is enabled, targeting another S3 bucket for log storage.
    *   All public access to the bucket is blocked.

**8. Refactor Monolithic Terraform to Modules**
*   **Scenario:** Your team's main Terraform project has become a single, massive `main.tf` file that is difficult to manage, reuse, and review. Your goal is to improve its structure.
*   **Task:** Refactor the monolithic Terraform configuration into separate, reusable modules. At a minimum, create modules for the VPC, EC2 instances, and security groups.
*   **Acceptance Criteria:**
    *   The root `main.tf` is significantly smaller and calls the new modules.
    *   A `modules/` directory is created containing subdirectories for `vpc`, `ec2`, and `sg`.
    *   The `terraform plan` output shows no changes in the infrastructure after refactoring.
    *   The modules use variables for inputs and expose outputs where necessary.

**9. Implement Remote State Management**
*   **Scenario:** Your team is growing, and multiple engineers are now making changes to the infrastructure with Terraform from their local machines. This has led to state file conflicts and drift. You need to implement a centralized, safe way to manage state.
*   **Task:** Configure your Terraform project to use a remote backend for state management. Use an AWS S3 bucket for storing the `terraform.tfstate` file and a DynamoDB table for state locking.
*   **Acceptance Criteria:**
    *   A `backend "s3" {}` block is added to the Terraform configuration.
    *   The configuration includes a `dynamodb_table` attribute for locking.
    *   After running `terraform init`, the state file is successfully migrated to the S3 bucket.
    *   A test confirms that state locking prevents concurrent `apply` operations.

**10. Import Existing Infrastructure into Terraform**
*   **Scenario:** A critical S3 bucket was created manually via the AWS Console for an urgent task. It now needs to be managed via IaC to prevent configuration drift and ensure it's part of the standard deployment process.
*   **Task:** Use the `terraform import` command to bring the existing, manually-created S3 bucket under Terraform's management without disrupting its current state.
*   **Acceptance Criteria:**
    *   A Terraform resource block (`resource "aws_s3_bucket" "..."`) matching the bucket's configuration is written.
    *   The `terraform import aws_s3_bucket.your_resource_name bucket-name` command is run successfully.
    *   Running `terraform plan` immediately after the import shows the message "No changes. Your infrastructure matches the configuration."

**11. Manage Environments with Workspaces**
*   **Scenario:** The team needs to manage infrastructure for `dev`, `staging`, and `prod` environments. Currently, this is done by copying and pasting code, which is error-prone. You need to implement a better system using native Terraform features.
*   **Task:** Use Terraform workspaces to manage the three separate environments (`dev`, `staging`, `prod`) from a single set of configuration files.
*   **Acceptance Criteria:**
    *   Three workspaces (`dev`, `staging`, `prod`) are created using `terraform workspace new`.
    *   The configuration uses `terraform.workspace` to dynamically set environment-specific variables (e.g., instance sizes, tags).
    *   Deploying to the `dev` workspace creates resources with `dev` tags/names.
    *   Switching to the `prod` workspace and running `plan` targets the production state file and configuration.

**12. Create a Custom Reusable Module**
*   **Scenario:** Your organization frequently deploys basic EC2 web servers for testing small applications. To speed up this process and ensure consistency, you need to create a standardized, reusable component.
*   **Task:** Create a custom, reusable Terraform module that provisions a standard EC2 instance. The module should allow customization of the instance type and the SSH key, and it must create a security group that only allows SSH access from a specified IP address.
*   **Acceptance Criteria:**
    *   A new directory `modules/web-server` is created containing `.tf` files for the module.
    *   The module defines variables for `instance_type`, `ami`, `ssh_key_name`, and `allowed_ssh_cidr`.
    *   The module has an `output` for the instance's public IP address.
    *   The root `main.tf` can call this module to create a web server instance with just a few lines of code.

### AWS & Cloud Infrastructure

**13. Automated EBS Snapshots**
*   **Scenario:** The company's disaster recovery policy requires daily backups of all production database volumes. Doing this manually is tedious and unreliable. You need to automate this process.
*   **Task:** Write a script using AWS CLI or Boto3 (Python) that creates snapshots of all EBS volumes tagged with `Environment=Production`. The script must also handle retention by deleting snapshots of these volumes that are older than 14 days.
*   **Acceptance Criteria:**
    *   The script runs without errors and is designed to be run from an AWS Lambda function.
    *   When run, it successfully creates snapshots for all EBS volumes with the `Environment=Production` tag.
    *   Each new snapshot is tagged with a `CreationDate` and `SourceVolumeID`.
    *   The script correctly identifies and deletes snapshots older than 14 days that were created by this process.

**14. Configure an Auto Scaling Group**
*   **Scenario:** The company's main web application experiences traffic spikes during marketing campaigns, causing performance degradation. You need to ensure the application can handle the load by scaling automatically.
*   **Task:** Configure an AWS Auto Scaling Group (ASG) for the web application's EC2 instances. The ASG should scale out when average CPU utilization exceeds 75% for 5 consecutive minutes and scale in when it drops below 25%.
*   **Acceptance Criteria:**
    *   An ASG is created with a desired capacity of 2, a minimum of 2, and a maximum of 6 instances.
    *   A "scale-out" policy (target tracking or step scaling) is created based on the specified CPU utilization metric.
    *   A corresponding "scale-in" policy is also created.
    *   The ASG is configured to use an Application Load Balancer for health checks and traffic distribution.
    *   During a load test, the ASG successfully adds and later removes an instance.

**15. Create a Least Privilege IAM Role for EC2**
*   **Scenario:** An application running on an EC2 instance needs to read objects from a specific S3 bucket. To adhere to security best practices, you must avoid using static IAM user credentials and provide the minimum required permissions.
*   **Task:** Create an IAM Role that grants an EC2 instance read-only access to a single, specific S3 bucket (`my-app-config-bucket`). Attach this role to the EC2 instance via an instance profile.
*   **Acceptance Criteria:**
    *   An IAM role is created with a trust policy that allows the EC2 service (`ec2.amazonaws.com`) to assume it.
    *   A new IAM policy is created that grants `s3:GetObject` and `s3:ListBucket` permissions ONLY on the specified bucket and its objects.
    *   The policy is attached to the role.
    *   From the EC2 instance, the AWS CLI command `aws s3 ls s3://my-app-config-bucket` succeeds, but `aws s3 ls s3://another-bucket` is denied.

**16. Establish VPC Peering for Shared Services**
*   **Scenario:** The `development` VPC needs to access a shared database that resides in the `shared-services` VPC. For security reasons, the database cannot be exposed to the public internet.
*   **Task:** Establish and configure a VPC peering connection between the `development` VPC and the `shared-services` VPC to allow private communication between them.
*   **Acceptance Criteria:**
    *   A VPC peering connection is requested from the `development` VPC and accepted by the `shared-services` VPC.
    *   The route tables for the relevant subnets in both VPCs are updated to direct traffic for the peer VPC's CIDR block to the peering connection.
    *   Security groups are configured to allow traffic from the peer VPC's security group on the required ports (e.g., PostgreSQL port 5432).
    *   An EC2 instance in the `development` VPC can successfully connect to the database instance in the `shared-services` VPC using its private IP address.

**17. Implement AWS Cost Anomaly Detection**
*   **Scenario:** Last month, a misconfigured script led to a surprise $5,000 increase in the AWS bill. Management has tasked you with implementing a system to detect and alert on such cost anomalies immediately.
*   **Task:** Set up AWS Cost Anomaly Detection to monitor your AWS account's spending. Configure it to send an immediate alert for any significant unexpected spend and a daily summary of detected anomalies.
*   **Acceptance Criteria:**
    *   AWS Cost Anomaly Detection is enabled in the AWS Cost Management console.
    *   An alert subscription is created.
    *   The subscription is configured to send individual alerts to an SNS topic (which could be linked to email or Slack).
    *   The subscription is also configured to send daily summaries.
    *   You can demonstrate where to view historical anomalies on the dashboard.

**18. Automate Patch Management with AWS Systems Manager**
*   **Scenario:** Your fleet of 50+ EC2 instances running Amazon Linux 2 must be patched regularly for security compliance. Manually SSH-ing into each one is not a viable option.
*   **Task:** Use AWS Systems Manager Patch Manager to automate the process of patching a fleet of EC2 instances. Define a patch baseline and a maintenance window to apply critical security updates.
*   **Acceptance Criteria:**
    *   All target EC2 instances have the SSM Agent installed and are correctly reporting to Systems Manager.
    *   A custom patch baseline is created that approves all `Critical` severity patches for Amazon Linux 2 with a 7-day delay.
    *   A maintenance window is configured to run every Saturday at 2 AM.
    *   A "Scan and Install" task is registered with the maintenance window, targeting the instances via a specific tag (e.g., `PatchGroup=WebApp-Prod`).
    *   After the maintenance window runs, the patch compliance report shows the targeted instances are compliant.

### Kubernetes & Orchestration

**19. Write a Kubernetes Deployment Manifest**
*   **Scenario:** The development team has delivered a new stateless microservice for image processing. You need to deploy it to the Kubernetes cluster and ensure it is resilient and has the necessary resources to run effectively.
*   **Task:** Write a Kubernetes `Deployment` manifest for the image processing microservice. The deployment must be configured with 3 replicas and have appropriate CPU and memory resource requests and limits.
*   **Acceptance Criteria:**
    *   A `deployment.yaml` file is created.
    *   The manifest specifies `replicas: 3`.
    *   The pod spec includes a `resources` section with `requests` (e.g., `cpu: "100m"`, `memory: "128Mi"`) and `limits` (e.g., `cpu: "500m"`, `memory: "256Mi"`).
    *   Applying the manifest with `kubectl apply -f deployment.yaml` successfully creates a Deployment and 3 running pods.

**20. Debug a CrashLoopBackOff Pod**
*   **Scenario:** The `api-gateway` service was just deployed, but it's failing to stay running. Users are reporting that the application is down. `kubectl get pods` shows the pod is in a `CrashLoopBackOff` state.
*   **Task:** A critical pod is stuck in a `CrashLoopBackOff` state. Your task is to investigate the issue using standard `kubectl` commands to find the root cause and fix it.
*   **Acceptance Criteria:**
    *   The root cause of the crash loop is identified (e.g., a misconfigured environment variable, a database connection error).
    *   The `kubectl logs <pod-name>`, `kubectl describe pod <pod-name>`, and `kubectl events` commands are used to gather evidence.
    *   The issue is resolved (e.g., by correcting a ConfigMap or the Deployment manifest).
    *   The pod restarts successfully and enters a `Running` state.

**21. Expose a Deployment with a LoadBalancer Service**
*   **Scenario:** You have successfully deployed a new `weather-forecast` web application to the cluster. Now, you need to make it accessible to users outside of the Kubernetes cluster.
*   **Task:** Create a Kubernetes `Service` of type `LoadBalancer` to expose the `weather-forecast` deployment to external traffic.
*   **Acceptance Criteria:**
    *   A `service.yaml` file is created with `spec.type: LoadBalancer`.
    *   The service's `spec.selector` correctly targets the pods of the `weather-forecast` deployment.
    *   Applying the manifest provisions a cloud load balancer.
    *   The service receives an external IP address, which can be seen with `kubectl get svc`.
    *   You can access the application from your browser using the external IP address.

**22. Implement Readiness and Liveness Probes**
*   **Scenario:** The `shopping-cart` service sometimes gets into a broken state where it stops responding but doesn't crash. This leads to user-facing errors because Kubernetes keeps sending traffic to the broken pod. You need to improve its resilience.
*   **Task:** Implement both readiness and liveness probes for the `shopping-cart` service to help Kubernetes manage its health more effectively.
*   **Acceptance Criteria:**
    *   A `livenessProbe` is added to the Deployment manifest to restart the container if it becomes unresponsive.
    *   A `readinessProbe` is added to ensure the pod only receives traffic when it is fully initialized.
    *   The probes are configured with appropriate `initialDelaySeconds`, `periodSeconds`, and `failureThreshold`.
    *   During a simulated failure, the liveness probe triggers a container restart, and the readiness probe stops traffic from being sent to it.

**23. Secure Pods with a NetworkPolicy**
*   **Scenario:** For compliance reasons, the `customer-database` pod must be isolated. It should only accept incoming connections from the `backend-api` pods and nothing else within the cluster.
*   **Task:** Write a Kubernetes `NetworkPolicy` that restricts ingress traffic to the `customer-database` pods. The policy should only allow traffic from pods with the label `app=backend-api` on the database connection port.
*   **Acceptance Criteria:**
    *   A `network-policy.yaml` file is created.
    *   The policy's `podSelector` targets the database pods (e.g., `app=customer-db`).
    *   The `ingress` rule specifies a `podSelector` that matches the `backend-api` pods and the correct `port`.
    *   After applying the policy, connection attempts from the `backend-api` pod succeed, while attempts from any other pod are blocked.

**24. Configure Horizontal Pod Autoscaling (HPA)**
*   **Scenario:** The `data-processing` service experiences variable load. You need to configure it to automatically scale the number of pods up or down based on its CPU usage to save costs and maintain performance.
*   **Task:** Configure a Horizontal Pod Autoscaler (HPA) to automatically scale the `data-processing` deployment. The HPA should target an average CPU utilization of 60%.
*   **Acceptance Criteria:**
    *   The pods in the target Deployment have CPU resource `requests` defined.
    *   An `HPA` manifest is created or the `kubectl autoscale` command is used.
    *   The HPA is configured with a `minReplicas` (e.g., 2), `maxReplicas` (e.g., 10), and a target CPU utilization of 60%.
    *   Under a load test, `kubectl get hpa` shows the number of replicas increasing, and after the load is removed, it scales back down.

**25. Enforce Namespace Resource Quotas**
*   **Scenario:** The `test` namespace is being used by several teams for experiments. Last week, a single runaway pod consumed all available CPU on a node, impacting other services. You need to prevent this from happening again.
*   **Task:** Define a `ResourceQuota` for the `test` namespace to limit the total amount of CPU and memory that can be consumed by all pods within it.
*   **Acceptance Criteria:**
    *   A `resource-quota.yaml` file is created.
    *   The quota sets a hard limit on `requests.cpu`, `requests.memory`, `limits.cpu`, and `limits.memory`.
    *   After applying the quota, `kubectl describe quota -n test` shows the defined limits.
    *   Attempting to create a new pod that would exceed the quota fails with a "forbidden" error message.

### CI/CD & Automation

**26. Create a Basic CI/CD Pipeline**
*   **Scenario:** The development team for a new Node.js microservice is currently building and testing their application manually. You need to create a foundational CI/CD pipeline to automate this workflow.
*   **Task:** Create a basic CI/CD pipeline using either GitHub Actions or GitLab CI. The pipeline should trigger on every push to the `main` branch and perform the following steps: build a Docker image, run unit tests, and push the tagged image to a container registry (like Docker Hub or ECR).
*   **Acceptance Criteria:**
    *   A pipeline configuration file (`.github/workflows/ci.yml` or `.gitlab-ci.yml`) is created.
    *   The pipeline has distinct stages/jobs for `build`, `test`, and `push`.
    *   The `test` stage successfully runs the application's unit tests (e.g., `npm test`).
    *   The `push` stage successfully tags the Docker image with the Git commit SHA and pushes it to the container registry.
    *   The pipeline completes successfully on a push to `main`.

**27. Add a Manual Approval Gate for Production**
*   **Scenario:** To reduce the risk of accidental deployments, the release manager requires that all deployments to the `production` environment must be manually approved by a team lead.
*   **Task:** Add a manual approval gate to your existing deployment pipeline. This gate should pause the pipeline just before the `deploy-to-prod` job runs, waiting for explicit approval before proceeding.
*   **Acceptance Criteria:**
    *   The CI/CD pipeline configuration is updated.
    *   In GitLab CI, this is implemented using `when: manual`. In GitHub Actions, this uses an `environment` with a required reviewer.
    *   When a pipeline targeting production is run, it pauses at the approval step.
    *   The deployment job only runs after a user with the correct permissions clicks the "approve" button in the UI.

**28. Implement Pipeline Caching for Dependencies**
*   **Scenario:** The CI pipeline for the main frontend application is taking over 15 minutes to run, primarily because it downloads hundreds of megabytes of `node_modules` on every execution. This is slowing down development feedback loops.
*   **Task:** Implement a caching mechanism in your CI pipeline to cache project dependencies (e.g., `node_modules` for Node.js, `.m2` for Maven, or `pip` cache for Python) between pipeline runs.
*   **Acceptance Criteria:**
    *   The pipeline configuration is updated with a `cache` key (GitLab CI) or the `actions/cache` action (GitHub Actions).
    *   The cache is correctly keyed to the project's dependency lock file (e.g., `package-lock.json`, `pom.xml`).
    *   The first pipeline run after the change creates and stores the cache.
    *   Subsequent pipeline runs are significantly faster (e.g., build time reduced by >50%) because dependencies are restored from the cache.

**29. Integrate a Code Quality Scan**
*   **Scenario:** Management wants to improve overall code quality and maintainability. You have been tasked with integrating a static analysis tool into the CI process to catch bugs and code smells early.
*   **Task:** Integrate SonarQube scanning into your CI pipeline. Configure it to analyze the code on every pull request and fail the pipeline if the project's quality gate conditions (e.g., "new bugs > 0") are not met.
*   **Acceptance Criteria:**
    *   A new `code-quality` stage is added to the CI pipeline.
    *   The stage is configured with the SonarQube server URL and an authentication token (stored as a secure CI/CD variable).
    *   The SonarScanner is run against the codebase.
    *   The pipeline correctly fails if the SonarQube quality gate reports a "FAILED" status.
    *   A link to the SonarQube analysis report is available in the pull request.

**30. Implement Secure Secret Management**
*   **Scenario:** Currently, the CI/CD pipeline has a database password stored as a plain-text variable, which is a major security risk. You need to implement a secure way to provide secrets to the pipeline at runtime.
*   **Task:** Modify the CI/CD pipeline to fetch secrets (like API keys or database passwords) dynamically from a secure vault, such as HashiCorp Vault or AWS Secrets Manager, instead of using plain-text CI/CD variables.
*   **Acceptance Criteria:**
    *   The plain-text secret is removed from the CI/CD variables.
    *   The pipeline includes a step to authenticate with the vault (e.g., using a JWT or IAM role).
    *   The secret is fetched from the vault and injected into the environment for the subsequent steps that need it.
    *   The secret value is masked in the CI/CD job logs.

**31. Create a Reusable CI/CD Workflow**
*   **Scenario:** Your company has over 20 microservices, and each has a nearly identical CI/CD pipeline configuration. When you need to make a change (e.g., update a scanner), you have to do it in 20 different places. You need to centralize this logic.
*   **Task:** Create a reusable CI/CD workflow/template that encapsulates the common build, test, and deploy logic. Refactor at least two microservice pipelines to use this new reusable workflow.
*   **Acceptance Criteria:**
    *   A central, reusable workflow is created (e.g., a "Composite Action" in GitHub Actions or a `include:template` file in GitLab CI).
    *   The reusable workflow accepts parameters/inputs to handle minor differences between services (e.g., application port).
    *   The `.gitlab-ci.yml` or GitHub Actions workflow file in the individual service repositories is simplified to just a few lines that call the reusable workflow.
    *   The pipelines for the refactored services continue to run successfully.

### GitOps

**32. Set Up a GitOps Controller**
*   **Scenario:** Your organization is adopting GitOps as the standard for managing Kubernetes deployments. Your first task is to set up a GitOps controller in the cluster and connect it to a configuration repository.
*   **Task:** Install either Argo CD or Flux into your Kubernetes cluster. Configure it to monitor a dedicated Git repository that contains Kubernetes manifests. Create a simple Nginx deployment manifest in the Git repository and ensure the GitOps tool deploys it to the cluster automatically.
*   **Acceptance Criteria:**
    *   The GitOps tool (Argo CD or Flux) is successfully installed in its own namespace in the cluster.
    *   An `Application` (Argo CD) or `Kustomization` (Flux) resource is created that points to your Git repository.
    *   Pushing an Nginx deployment manifest to the repository results in the Nginx pods being created in the cluster.
    *   The GitOps tool's UI or CLI shows the application state as `Synced` and `Healthy`.

**33. Manage Environments with Kustomize**
*   **Scenario:** Your team manages `dev`, `staging`, and `prod` environments. You need a structured way to promote application changes through these environments using GitOps, avoiding simple copy-pasting of manifests.
*   **Task:** Structure a GitOps repository to manage three environments (`dev`, `staging`, `prod`) using Kustomize. Create a common `base` configuration and then environment-specific `overlays` that patch the base for each environment (e.g., changing the replica count or ConfigMap values).
*   **Acceptance Criteria:**
    *   The repository has a directory structure like `/apps/my-app/base` and `/apps/my-app/overlays/dev`, `/staging`, `/prod`.
    *   The `dev` overlay changes the replica count to 1, while the `prod` overlay sets it to 5.
    *   A change made in the `base` (e.g., updating a container image tag) is reflected in all environments after their respective GitOps controllers sync.
    *   Promoting a change involves updating the image tag in the `staging` overlay, and then later in the `prod` overlay.

**34. Demonstrate Drift Detection and Remediation**
*   **Scenario:** A developer, trying to quickly debug an issue, used `kubectl scale deployment my-app --replicas=0` directly in the `production` cluster, causing an outage. You need to ensure such manual changes are automatically detected and reverted.
*   **Task:** Demonstrate the drift detection and auto-remediation capabilities of your GitOps tool. Manually change a resource in the cluster (e.g., scale a deployment using `kubectl`). Configure your GitOps tool to detect this drift from the state defined in Git and automatically revert the change.
*   **Acceptance Criteria:**
    *   The Argo CD Application or Flux Kustomization is configured with an automated sync policy or self-healing enabled.
    *   After you manually scale a deployment in the cluster, the GitOps tool's UI/CLI shows the application status as `OutOfSync`.
    *   Within a few minutes, the tool automatically triggers a sync.
    *   The deployment is scaled back to the number of replicas defined in the Git repository, resolving the drift.

**35. Perform a Git-based Rollback**
*   **Scenario:** A new version of the `checkout-service` was just deployed to production via a Git commit. Moments later, users report that the checkout page is broken. You need to perform a fast and safe rollback.
*   **Task:** Roll back a faulty deployment by reverting the problematic commit in your GitOps configuration repository.
*   **Acceptance Criteria:**
    *   The last commit (which deployed the faulty version) is identified using `git log`.
    *   The `git revert <commit-sha>` command is used to create a new commit that undoes the changes.
    *   The new revert commit is pushed to the `main` branch of the configuration repository.
    *   The GitOps tool detects the new commit and automatically syncs the cluster, redeploying the previous, stable version of the application.

**36. Implement Advanced Health Assessment with Argo CD**
*   **Scenario:** A recent deployment of the `payment-service` was marked as "Synced" by Argo CD, but the application was internally unhealthy and failing to process payments. The default health check (pod readiness) was not enough.
*   **Task:** Configure an Argo CD Application to use a custom health check for a service. Write a simple Lua script that makes a request to the application's `/health` endpoint and checks if the response body contains `"status": "ok"`.
*   **Acceptance Criteria:**
    *   The `argocd-cm` ConfigMap is updated with a custom health check definition for your resource type.
    *   The health check uses a Lua script to define the health logic.
    *   When the application is deployed and its `/health` endpoint returns a valid response, Argo CD shows the resource as `Healthy`.
    *   When the endpoint returns an error or incorrect body, Argo CD marks the resource as `Degraded`, even if the pod is still `Running`.

### Monitoring & Logging

**37. Set Up Kubernetes Cluster Monitoring**
*   **Scenario:** The operations team has no visibility into the health and performance of the Kubernetes cluster nodes. They need a dashboard to monitor fundamental metrics like CPU, memory, and disk usage.
*   **Task:** Set up Prometheus and Grafana to monitor your Kubernetes cluster. Use the `kube-prometheus-stack` Helm chart to deploy them. Configure a Grafana dashboard to visualize key cluster-level metrics.
*   **Acceptance Criteria:**
    *   Prometheus and Grafana are deployed successfully to the cluster via Helm.
    *   Prometheus is correctly scraping metrics from cluster components (e.g., nodes, kubelets).
    *   A pre-built Grafana dashboard (like the "Kubernetes Cluster Health" dashboard) is imported and correctly displays node CPU, memory, and disk I/O metrics.
    *   You can access the Grafana UI via a port-forward or Ingress.

**38. Create an Application Metrics Dashboard**
*   **Scenario:** While cluster monitoring is in place, developers have no insight into how their specific application is performing. They need a dashboard to see key application-level metrics like request latency and error rates.
*   **Task:** The application exposes Prometheus metrics on a `/metrics` endpoint. Create a new, custom Grafana dashboard to visualize these application-specific metrics. Focus on displaying HTTP request latency (p95, p99), total request count, and a breakdown of HTTP status codes (2xx, 4xx, 5xx).
*   **Acceptance Criteria:**
    *   A new Grafana dashboard is created.
    *   The dashboard has panels for visualizing the application's key metrics using PromQL queries.
    *   There is a graph showing the 95th and 99th percentile request latency over time.
    *   A pie chart or stat panel shows the ratio of 5xx errors to total requests.
    *   The dashboard can be filtered by pod or service instance.

**39. Implement Centralized Logging**
*   **Scenario:** When a pod crashes, developers have to manually use `kubectl logs` to find the error message before the pod is deleted. This is inefficient and sometimes impossible. You need to implement a centralized logging solution.
*   **Task:** Configure a logging agent like Fluentd or Promtail as a DaemonSet on your Kubernetes cluster. Configure the agent to collect logs from all running containers and forward them to a centralized logging backend like Loki or Elasticsearch.
*   **Acceptance Criteria:**
    *   The logging agent is running as a DaemonSet on every node in the cluster.
    *   The agent is configured to automatically discover and tail logs from all pods.
    *   Logs are correctly parsed and enriched with Kubernetes metadata (e.g., pod name, namespace, labels).
    *   You can successfully search for and view logs from any pod using the logging backend's UI (e.g., Grafana Explore with Loki, or Kibana).

**40. Configure Alerting on High Error Rate**
*   **Scenario:** The `login-service` has been experiencing intermittent failures, but the on-call team only finds out when customers complain. You need to set up proactive alerting to notify the team as soon as a problem occurs.
*   **Task:** Set up an alert using Prometheus Alertmanager. The alert should fire if the rate of HTTP 5xx errors for the `login-service` is greater than 1% over a 5-minute period. Configure the alert to send a notification to a Slack channel.
*   **Acceptance Criteria:**
    *   A new alerting rule is added to Prometheus's configuration.
    *   The PromQL query correctly calculates the rate of 5xx errors for the target service.
    *   Alertmanager is configured with a receiver for Slack notifications.
    *   When the error rate threshold is breached during a test, a "FIRING" alert appears in Alertmanager and a notification is posted to the configured Slack channel.

**41. Implement Distributed Tracing**
*   **Scenario:** A customer reports that adding an item to their shopping cart is taking over 5 seconds, but it involves calls to three different microservices (`frontend`, `cart-api`, `inventory-service`). It's unclear which service is causing the slowdown.
*   **Task:** Instrument a microservice with OpenTelemetry to generate and export traces. Set up Jaeger as a tracing backend to receive and visualize these traces. Your goal is to be able to visualize the entire lifecycle of a request as it flows through the different services.
*   **Acceptance Criteria:**
    *   The application code is updated with the OpenTelemetry SDK to create spans for key operations.
    *   The application is configured to export traces to a Jaeger collector.
    *   Jaeger is deployed to the Kubernetes cluster.
    *   When you perform an action in the application, a complete trace appears in the Jaeger UI, showing the parent-child relationships between spans across the different services.
    *   You can identify the slowest span in the trace to pinpoint the source of latency.

**42. Perform an Advanced Log Query**
*   **Scenario:** The support team needs to find all failed login attempts for a specific user (`user-123`) from the last 7 days to investigate a potential security issue.
*   **Task:** Write an advanced log query using either LogQL (for Loki) or KQL (for Elasticsearch) to find all log entries that meet the following criteria: from the `auth-service`, contain the string "failed login", have a log level of `WARN`, and include the username `user-123`. The query should cover the last 7 days.
*   **Acceptance Criteria:**
    *   The query is written using the correct syntax for your logging backend.
    *   The query correctly filters by service (`{app="auth-service"}`).
    *   The query filters the log message content (`|= "failed login"` in LogQL).
    *   The query filters by other metadata like log level.
    *   Executing the query returns the correct set of log lines and no false positives.

### Security & Compliance

**43. Integrate SAST into a CI Pipeline**
*   **Scenario:** To shift security left, the security team requires that all code be scanned for potential vulnerabilities before a pull request can be merged.
*   **Task:** Integrate a Static Application Security Testing (SAST) tool, such as Snyk or Checkmarx, into your CI pipeline. The scan should run on every pull request and post the results back to the PR for review.
*   **Acceptance Criteria:**
    *   A SAST tool is configured to run automatically on pull requests.
    *   The pipeline fails if the SAST tool discovers any new 'High' or 'Critical' severity vulnerabilities.
    *   A summary of the scan results is available as a comment or check on the pull request.
    *   The pipeline passes for a pull request that introduces no new vulnerabilities.

**44. Perform a Zero-Downtime IAM Key Rotation**
*   **Scenario:** An audit has found that the access keys for a critical IAM user, used by a legacy application, have not been rotated in over a year. You must rotate them immediately without causing application downtime.
*   **Task:** Perform a zero-downtime rotation of the AWS access keys for a critical IAM user.
*   **Acceptance Criteria:**
    *   A new access key is created for the IAM user in the AWS console.
    *   The application's configuration is updated with the new access key ID and secret access key.
    *   The application is redeployed or restarted to pick up the new credentials, and its functionality is verified.
    *   The old, inactive access key is deactivated (but not immediately deleted) in IAM.
    *   The application continues to function correctly throughout the entire process.

**45. Audit a Kubernetes Cluster with Kube-Bench**
*   **Scenario:** Your Kubernetes cluster must be audited against industry-standard security benchmarks. You need to identify and remediate any critical misconfigurations.
*   **Task:** Use `kube-bench` to audit your Kubernetes cluster nodes against the CIS (Center for Internet Security) benchmarks. Analyze the report and remediate at least three of the identified `[FAIL]` items.
*   **Acceptance Criteria:**
    *   `kube-bench` is run successfully against the cluster's master and worker nodes.
    *   The generated report is saved and analyzed.
    *   At least three failing checks are chosen for remediation (e.g., insecure etcd permissions, anonymous auth enabled).
    *   The necessary configuration changes are applied to the cluster.
    *   Running `kube-bench` again shows the remediated items as `[PASS]`.

**46. Enforce Least Privilege with Security Groups**
*   **Scenario:** A security review of your three-tier web application (web, API, database) revealed that the security groups are too permissive. For example, the database security group allows traffic from `0.0.0.0/0`.
*   **Task:** Review and refactor the AWS Security Group rules for the three-tier application to enforce the principle of least privilege.
*   **Acceptance Criteria:**
    *   The web-tier security group only allows inbound traffic from the internet on ports 80/443.
    *   The API-tier security group only allows inbound traffic from the web-tier security group on the application port.
    *   The database-tier security group only allows inbound traffic from the API-tier security group on the database port.
    *   All outbound rules are restricted to only what is necessary.
    *   The application remains fully functional after the changes.

**47. Respond to an AWS GuardDuty Finding**
*   **Scenario:** You receive a high-priority alert from AWS GuardDuty: `UnauthorizedAccess:EC2/MaliciousDomainRequest.B`. It indicates an EC2 instance in your production account is communicating with a known malicious domain.
*   **Task:** Investigate and contain the threat identified by the GuardDuty finding.
*   **Acceptance Criteria:**
    *   The specific EC2 instance and the malicious domain are identified from the GuardDuty finding details.
    *   The instance is immediately isolated from the network by attaching a "quarantine" security group that denies all traffic.
    *   An EBS snapshot of the instance's root volume is taken for later forensic analysis.
    *   The source of the malicious activity is investigated (e.g., by analyzing logs or the snapshot).
    *   A plan is created to terminate the compromised instance and replace it with a clean one.

**48. Audit for Publicly Accessible S3 Buckets**
*   **Scenario:** To prevent accidental data exposure, you need to implement a continuous check to ensure no S3 buckets in your AWS account are publicly accessible.
*   **Task:** Write a script (using AWS CLI, Boto3, or another tool) that audits all S3 buckets in an account. The script should identify and report any buckets that allow public `read` or `write` access via their ACLs or bucket policies.
*   **Acceptance Criteria:**
    *   The script iterates through all S3 buckets in the account.
    *   It correctly identifies buckets with public access permissions.
    *   The script generates a clear report listing the names of the non-compliant buckets and the reason they are flagged.
    *   The script can be scheduled to run periodically (e.g., as a daily Lambda function).

**49. Enforce Pod Security Standards**
*   **Scenario:** To harden the security of your Kubernetes cluster, you need to prevent pods from running with privileged access, which could be exploited in a container breakout attack.
*   **Task:** Implement the `baseline` Pod Security Standard on a specific namespace. This will prevent new pods that violate the baseline policy from being created in that namespace.
*   **Acceptance Criteria:**
    *   The target namespace is labeled appropriately (e.g., `pod-security.kubernetes.io/enforce=baseline`).
    *   Attempting to create a pod with `hostNetwork: true` in that namespace is blocked by the admission controller.
    *   Attempting to create a pod that runs as the root user (without `runAsNonRoot: true` in the security context) is blocked.
    *   Existing, compliant pods in the namespace continue to run without issue.

**50. Implement Dynamic Database Credentials with Vault**
*   **Scenario:** Your application currently stores its database credentials as long-lived secrets in a Kubernetes Secret. This is a security risk if the secret is compromised. You need to switch to a system of short-lived, dynamically generated credentials.
*   **Task:** Configure your application to fetch database credentials dynamically from HashiCorp Vault at startup. This involves setting up a Vault database secrets engine and modifying the application's startup logic.
*   **Acceptance Criteria:**
    *   A Vault database secrets engine is configured and connected to your database.
    *   A Vault role is created that defines the SQL statements to create and revoke users.
    *   The application authenticates to Vault (e.g., using the Kubernetes Auth Method).
    *   At startup, the application requests new database credentials from Vault.
    *   The application successfully connects to the database using the dynamically generated, short-lived credentials.
    *   The static Kubernetes secret containing the old credentials is deleted.
