
---

# **CI/CD Deployment Process with Jenkins, Docker Compose, GitHub, Webhook, and ngrok**

This guide explains how to set up a CI/CD pipeline using **Jenkins**, **Docker Compose**, **GitHub**, **ngrok**, and how to configure the deployment process for automatic updates.

---

### **1. Install and Set Up Jenkins**

If you haven’t already installed Jenkins, follow these steps:

1. **Install Jenkins on your server** (you can use Ubuntu/Kali Linux as your server):
   ```bash
   sudo apt update
   sudo apt install openjdk-11-jdk
   sudo apt install jenkins
   sudo systemctl start jenkins
   sudo systemctl enable jenkins
   ```

2. **Access Jenkins** on `localhost:8080` or configure it to use your system's IP if accessing from other devices in your network (details are in the initial setup).

3. **Install Required Plugins**:
   - Go to **Manage Jenkins** → **Manage Plugins**.
   - Install the following plugins:
     - Git Plugin
     - Docker Pipeline
     - GitHub Integration Plugin
     - Pipeline Plugin

---

### **2. Install Docker and Docker Compose**

Jenkins needs Docker to build and deploy containers. Install Docker and Docker Compose on your Jenkins server:

1. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

2. **Install Docker Compose**:
   ```bash
   sudo apt install docker-compose
   ```

---

### **3. Set Up GitHub Repository**

1. **Create a GitHub repository** for your project if you haven't already.

2. **Push Your Code to GitHub**.

3. **Generate a GitHub Personal Access Token (PAT)** with `repo` and `admin:repo_hook` permissions (to interact with Jenkins). [Steps to generate PAT](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

4. **Add GitHub credentials to Jenkins**:
   - Go to **Manage Jenkins** → **Manage Credentials** → **Global** → **Add Credentials**.
   - Choose **Kind** as **Username with Password**.
   - Enter **GitHub Username** and **GitHub PAT**.

---

### **4. Configure Jenkins Job for CI/CD Pipeline**

1. **Create a Jenkins Pipeline Job**:
   - Go to **New Item** → **Pipeline** → **Enter the Job Name** and click **OK**.
   
2. **Set GitHub Repository in Jenkins Pipeline**:
   - Under **Pipeline Definition**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git**, and enter your GitHub repository URL.
   - Use the **GitHub credentials** you created earlier.
   
3. **Create a Jenkinsfile in your GitHub repository**:
   - The Jenkinsfile defines the steps for building and deploying your application. Make sure it's present in the root of your repository.


### **4. Set Up Webhook for GitHub to Trigger Jenkins Build**

1. **Create Webhook on GitHub**:
   - Go to your GitHub repository → **Settings** → **Webhooks** → **Add Webhook**.
   - In **Payload URL**, enter:
     ```bash
     http://YOUR_JENKINS_IP:8080/github-webhook/
     ```
     (If Jenkins is local, use **ngrok** to expose the URL, or configure port forwarding if it's hosted on a server).
   - Set **Content type** to `application/json`.
   - Choose the event as **Just the push event**.
   
2. **Test the webhook**: Push a new commit to your GitHub repository and verify that Jenkins triggers a build.

---

### **6. Use ngrok for Exposing Jenkins to GitHub Webhook (Optional for Local Setup)**

If Jenkins is running locally and GitHub can’t directly reach it, use **ngrok** to tunnel the connection:

1. **Install ngrok**:
   ```bash
   sudo apt install ngrok
   ```

2. **Expose Jenkins with ngrok**:
   ```bash
   ngrok http 8080
   ```
add your authentication token of ngrok 
   ngrok will provide a public URL like `https://abcd.ngrok.io`.

3. **Update GitHub Webhook**:
   - Replace the Payload URL in your GitHub webhook with the **ngrok URL**:
     ```bash
     https://abcd.ngrok.io/github-webhook/
     ```

---

### **7. Configure Docker for Deployment on a Server**

To deploy using **Docker Compose**:

2. **Deploy using Docker Compose in Jenkins**:
   - In your Jenkinsfile, use the command `docker-compose up -d` to start the application in detached mode.

---

### **8. Monitor Jenkins Build Logs and Deployment Status**

1. **Access Jenkins Dashboard**: After pushing code or triggering a build manually, you can monitor the build status and logs through the **Jenkins Dashboard**.
   
2. **Troubleshooting**: Check the console output of each Jenkins build for any errors related to the Docker build or deployment process.

---

### **9. Automate the Deployment Process**

Once the pipeline is set up:

- Any **push to GitHub** triggers the webhook and the Jenkins pipeline.
- Jenkins checks the code, builds the Docker image, and deploys it using Docker Compose.

---

### **10. (Optional) Expose Jenkins Publicly for Remote Access**

If you want to access Jenkins from outside your network:

1. **Configure port forwarding** on your router to forward port `8080` to the machine where Jenkins is running.
   
2. **Access Jenkins from public IP**: Use the external IP of your machine:
   ```bash
   http://<public-ip>:8080
   ```

---

### **Summary**

With the above steps:

- **GitHub** is the source repository for your application code.
- **Jenkins** automates the build and deployment pipeline using **Docker Compose**.
- **Webhook** triggers Jenkins builds whenever you push new code to GitHub.
- **ngrok** is used for exposing Jenkins if it's running locally.
- **Docker** is used for deploying the application to the server.

Now, you have a fully automated **CI/CD pipeline** that deploys your code to production using Docker Compose, triggered by code pushes to GitHub.






process flow:
code ----> github---->ngrok-webhook-------jenkins----------docker-contanier--------server
