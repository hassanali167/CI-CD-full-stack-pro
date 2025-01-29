To set up **Jenkins and GitHub** for a **CI/CD pipeline**, follow these steps:  

---

## **1. Install Jenkins and Required Plugins**
Since Jenkins is already running on **localhost:8080**, ensure you have the following plugins installed:  

🔹 **Git plugin**  
🔹 **Pipeline plugin**  
🔹 **GitHub Integration Plugin**  

**To install plugins:**  
1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Plugins**.  
2. Under the **Available** tab, search for:  
   - **Git plugin**  
   - **GitHub Integration Plugin**  
   - **Pipeline**  
3. Install them and restart Jenkins.  

---

## **2. Generate a GitHub Personal Access Token (PAT)**
Jenkins needs access to your **GitHub repository** to pull code.  

🔹 **Step to create a token:**  
1. Go to **GitHub** → **Settings** → **Developer Settings** → **Personal Access Tokens** → **Tokens (classic)**.  
2. Click **Generate new token (classic)**.  
3. Select the following **scopes**:  
   - `repo` (full control over private repositories)  
   - `admin:repo_hook` (to manage webhooks)  
4. Generate and **copy the token** (you won’t see it again).  

---

## **3. Add GitHub Credentials in Jenkins**
1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Manage Credentials**.  
2. Click **(global) → Add Credentials**.  
3. Select **Kind: Username and Password**.  
4. **Username:** Your GitHub username.  
5. **Password:** Paste the **GitHub PAT** you copied.  
6. Click **Save**.  

---

## **4. Create a Jenkins Pipeline for GitHub**
### **Option 1: Use Freestyle Job**
1. Go to **Jenkins Dashboard** → **New Item**.  
2. Select **Freestyle project** and click **OK**.  
3. Under **Source Code Management**, select **Git**.  
4. **Repository URL:** Paste your GitHub repo URL.  
5. **Credentials:** Select the **GitHub PAT** you added earlier.  
6. In **Build Triggers**, check **Poll SCM** and set:  
   ```
   H/5 * * * *
   ```
   (polls GitHub every 5 minutes).  
7. In **Build**, add your shell script or commands (e.g., `docker compose up -d`).  
8. Click **Save & Build Now**.  

---

### **Option 2: Use a Pipeline Job (Recommended)**
1. Go to **Jenkins Dashboard** → **New Item**.  
2. Select **Pipeline**, name it, and click **OK**.  
3. Under **Pipeline Definition**, select **Pipeline script from SCM**.  
4. Choose **Git** and enter your **GitHub repository URL**.  
5. Select the branch (**main** or another branch).  
6. Under **Script Path**, enter:  
   ```
   Jenkinsfile
   ```
   (Ensure your repo has a `Jenkinsfile`).  
7. Click **Save & Build Now**.  

---

## **5. Connect GitHub Webhook to Jenkins (Trigger Builds Automatically)**
Instead of polling, you can set up a **webhook** for faster CI/CD.  

🔹 **Steps to Add a Webhook:**  
1. Go to your **GitHub Repository** → **Settings** → **Webhooks**.  
2. Click **Add Webhook**.  
3. In **Payload URL**, enter:  
   ```
   http://YOUR_JENKINS_IP:8080/github-webhook/
   ```
   (If Jenkins is local, you need to expose it using **ngrok** or deploy it on a server).  
4. **Content type:** `application/json`.  
5. **Select events:** Choose **"Just the push event"**.  
6. Click **Add Webhook**.  

---

## **6. Test the CI/CD Pipeline**
✅ **Push new code to GitHub** and check if Jenkins automatically triggers the build.  
✅ If using polling (`H/5 * * * *`), wait **5 minutes** and check the build logs.  

---

## **🔹 Important Notes**
✔️ If Jenkins is **running locally**, GitHub **can't reach it** directly for webhooks. Use **ngrok**:  
   ```
   ngrok http 8080
   ```
   Then replace the **GitHub Webhook URL** with `http://ngrok.io/github-webhook/`.  
✔️ If Jenkins is **hosted on a server**, use the **public IP** instead.  
✔️ If facing permission issues, **add your SSH key** to GitHub and Jenkins.  

🚀 **Now you have a fully automated CI/CD pipeline between GitHub and Jenkins!** Let me know if you need help! 😃




--------------------------------------------------------------------------------------------------------------------------------------------------

To make Jenkins accessible via **your system's IP address (e.g., `192.168.1.100:8080`)** in **Kali Linux**, follow these steps:

---

### **1. Configure Jenkins to Listen on Your System's IP**
By default, Jenkins listens on **localhost (127.0.0.1:8080)**. You need to change it to your **system IP**.

1. **Open Jenkins configuration file**:  
   ```bash
   sudo nano /etc/default/jenkins
   ```
2. **Find this line**:
   ```bash
   HTTP_HOST=127.0.0.1
   ```
3. **Change it to your system IP** (check with `ip a` command):
   ```bash
   HTTP_HOST=192.168.1.100
   ```
   (Replace `192.168.1.100` with your actual system IP)

4. **Save and exit** (`CTRL + X`, then `Y`, then `Enter`).

---

### **2. Restart Jenkins to Apply Changes**
```bash
sudo systemctl restart jenkins
```
Check if Jenkins is running:
```bash
sudo systemctl status jenkins
```
If it's running correctly, you should see **"Active: running"**.

---
# **4. Find Your System IP**
Run:
```bash
ip a
```
Find your **Wi-Fi (wlan0)** or **Ethernet (eth0)** IP address (e.g., `192.168.1.100`).

---

### **5. Access Jenkins**
Now, open your browser and access Jenkins using:
```
http://192.168.1.100:8080
```
**Instead of `localhost:8080`, it will now be accessible via your system IP.**

---

### **6. (Optional) Make Jenkins Accessible from Outside the Network**
If you want to access Jenkins from another network or the internet:
- **Use Ngrok for temporary access**:
  ```bash
  ngrok http 8080
  ```
  It will provide a public URL like `https://abcd.ngrok.io`.
  
- **Port Forwarding in Router**:  
  - Go to your **router settings**.
  - Forward **port 8080** to your **system's IP**.
  - Find your **public IP** using:
    ```bash
    curl ifconfig.me
    ```
  - Access Jenkins via:
    ```
    http://<PUBLIC_IP>:8080
    ```

---

✅ **Now, Jenkins is accessible using your system IP!** 🚀 Let me know if you need more help. 😊
