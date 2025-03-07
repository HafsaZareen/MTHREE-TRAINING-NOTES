#!/bin/bash

# ===============================================================================
# JENKINS ZERO TO HERO INSTALLATION AND SETUP SCRIPT
# ===============================================================================
# This script performs a complete Jenkins setup on WSL Ubuntu, including:
# - Environment verification (WSL Ubuntu)
# - Jenkins installation and configuration
# - Java installation (required for Jenkins)
# - Creation of a sample Python script for Jenkins integration
# - Setup of a complete Jenkins pipeline example
# - Detailed explanations of Jenkins concepts
# ===============================================================================

# Text formatting for better readability
BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BOLD}${BLUE}==== $1 ====${NC}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to check if we're running in WSL Ubuntu
check_wsl_ubuntu() {
    print_section "CHECKING ENVIRONMENT"
    
    # Check if running in WSL
    if ! grep -q Microsoft /proc/version && ! grep -q microsoft /proc/version; then
        print_error "This script is designed to run on WSL (Windows Subsystem for Linux)"
        print_error "Current environment: $(uname -a)"
        exit 1
    else
        print_success "Running in WSL: $(uname -a)"
    fi
    
    # Check if running Ubuntu
    if [ -f /etc/lsb-release ]; then
        source /etc/lsb-release
        if [[ $DISTRIB_ID == "Ubuntu" ]]; then
            print_success "Running Ubuntu $DISTRIB_RELEASE"
        else
            print_warning "This script is optimized for Ubuntu, but you're running $DISTRIB_ID"
            read -p "Do you want to continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_warning "Cannot confirm Ubuntu distribution"
        read -p "Do you want to continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to check and install Java (required for Jenkins)
install_java() {
    print_section "CHECKING/INSTALLING JAVA"
    
    # Check if Java is already installed
    if command -v java &> /dev/null; then
        java_version=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
        print_success "Java is already installed (version: $java_version)"
    else
        print_warning "Java is not installed. Installing OpenJDK 11..."
        sudo apt-get update
        sudo apt-get install -y openjdk-11-jdk
        
        # Verify installation
        if command -v java &> /dev/null; then
            java_version=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
            print_success "Java installed successfully (version: $java_version)"
        else
            print_error "Failed to install Java. Please install it manually."
            exit 1
        fi
    fi
    
    # Set JAVA_HOME environment variable
    echo -e "\n# Setting up JAVA_HOME"
    JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
    echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
    print_success "JAVA_HOME set to $JAVA_HOME"
}

# Function to check and install Jenkins
install_jenkins() {
    print_section "CHECKING/INSTALLING JENKINS"
    
    # First, check if Jenkins service is already installed and running
    if systemctl is-active --quiet jenkins 2>/dev/null; then
        jenkins_version=$(java -jar /usr/share/jenkins/jenkins.war --version 2>/dev/null)
        print_success "Jenkins is already installed and running (version: $jenkins_version)"
        print_warning "Skipping Jenkins installation"
        return 0
    fi
    
    # Check if jenkins.war exists in common locations
    if [ -f /usr/share/jenkins/jenkins.war ]; then
        print_warning "Jenkins WAR file exists but service may not be running"
        print_warning "Will attempt to start/configure Jenkins"
    else
        print_warning "Jenkins not detected. Installing Jenkins..."
        
        # Import Jenkins repository key
        echo "Importing Jenkins repository key..."
        wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
        
        # Add Jenkins repository
        echo "Adding Jenkins repository..."
        sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
        
        # Update package lists
        sudo apt-get update
        
        # Install Jenkins
        echo "Installing Jenkins..."
        sudo apt-get install -y jenkins
        
        # Start Jenkins service
        sudo systemctl start jenkins
        
        # Enable Jenkins to start on boot
        sudo systemctl enable jenkins
        
        # Verify installation
        if systemctl is-active --quiet jenkins; then
            jenkins_version=$(java -jar /usr/share/jenkins/jenkins.war --version 2>/dev/null)
            print_success "Jenkins installed successfully (version: $jenkins_version)"
        else
            print_error "Failed to install or start Jenkins. Please check logs."
            print_warning "You can check logs with: sudo journalctl -u jenkins"
            exit 1
        fi
    fi
    
    # Wait for Jenkins to start up fully
    echo "Waiting for Jenkins to start up fully (this may take a minute)..."
    max_attempts=30
    attempts=0
    while [ $attempts -lt $max_attempts ]; do
        if [ -f /var/lib/jenkins/secrets/initialAdminPassword ]; then
            break
        fi
        attempts=$((attempts+1))
        echo -n "."
        sleep 2
    done
    echo
    
    if [ -f /var/lib/jenkins/secrets/initialAdminPassword ]; then
        admin_password=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)
        print_success "Jenkins is ready!"
        echo -e "${YELLOW}Initial admin password: ${BOLD}$admin_password${NC}"
        echo -e "${YELLOW}Access Jenkins at: ${BOLD}http://localhost:8080${NC}"
    else
        print_warning "Jenkins setup may not be complete. Please check manually."
    fi
}

# Function to create a sample Python script
create_python_script() {
    print_section "CREATING SAMPLE PYTHON SCRIPT"
    
    mkdir -p ~/jenkins-demo/scripts
    cat > ~/jenkins-demo/scripts/jenkins_api_example.py << 'EOF'
#!/usr/bin/env python3
"""
Jenkins API Interaction Example Script

This script demonstrates how to interact with the Jenkins API using Python.
It can:
1. Get information about Jenkins jobs
2. Trigger builds
3. Check build status

Requirements:
- Python 3.6+
- python-jenkins library (pip install python-jenkins)
"""

import jenkins
import time
import argparse
import sys
import os

class JenkinsApiClient:
    """
    Client for interacting with Jenkins API
    
    Jenkins concepts demonstrated:
    - Authentication: Using username/token for API access
    - Jobs: Core concept in Jenkins representing a task or pipeline
    - Builds: Instances of job executions
    """
    
    def __init__(self, url, username=None, password=None):
        """
        Initialize Jenkins API client
        
        Args:
            url (str): Jenkins server URL
            username (str): Jenkins username
            password (str): Jenkins API token or password
        """
        self.server = jenkins.Jenkins(url, username=username, password=password)
        try:
            self.user = self.server.get_whoami()
            self.version = self.server.get_version()
            print(f"Connected to Jenkins {self.version}")
            print(f"Logged in as: {self.user['fullName']}")
        except jenkins.JenkinsException as e:
            print(f"Error connecting to Jenkins: {e}")
            sys.exit(1)
    
    def get_jobs(self):
        """Get all Jenkins jobs"""
        jobs = self.server.get_jobs()
        if not jobs:
            print("No jobs found in Jenkins")
            return []
        
        print(f"Found {len(jobs)} jobs:")
        for job in jobs:
            print(f"  - {job['name']} ({job['url']})")
        return jobs
    
    def get_job_info(self, job_name):
        """
        Get detailed information about a specific job
        
        Args:
            job_name (str): Name of the Jenkins job
        """
        try:
            job_info = self.server.get_job_info(job_name)
            print(f"Job: {job_name}")
            print(f"  Description: {job_info.get('description', 'No description')}")
            print(f"  URL: {job_info['url']}")
            print(f"  Buildable: {job_info['buildable']}")
            print(f"  Last build: #{job_info.get('lastBuild', {}).get('number', 'None')}")
            return job_info
        except jenkins.NotFoundException:
            print(f"Job '{job_name}' not found")
            return None
    
    def build_job(self, job_name, parameters=None):
        """
        Trigger a build for a job
        
        Args:
            job_name (str): Name of the Jenkins job
            parameters (dict): Build parameters (for parameterized jobs)
        
        Returns:
            int: Queue item number
        """
        try:
            # Check if job exists
            self.server.get_job_info(job_name)
            
            # Trigger build
            if parameters:
                queue_id = self.server.build_job(job_name, parameters=parameters)
                print(f"Triggered build for '{job_name}' with parameters: {parameters}")
            else:
                queue_id = self.server.build_job(job_name)
                print(f"Triggered build for '{job_name}'")
            
            print(f"Build added to queue (ID: {queue_id})")
            
            # Wait for build to start
            build_number = None
            attempts = 0
            while attempts < 10 and build_number is None:
                try:
                    build_info = self.server.get_queue_item(queue_id)
                    if 'executable' in build_info and build_info['executable']:
                        build_number = build_info['executable']['number']
                    else:
                        time.sleep(2)
                        attempts += 1
                except jenkins.NotFoundException:
                    time.sleep(2)
                    attempts += 1
            
            if build_number:
                print(f"Build #{build_number} started")
                return build_number
            else:
                print("Build not started after waiting, check Jenkins UI")
                return None
        except jenkins.NotFoundException:
            print(f"Job '{job_name}' not found")
            return None
    
    def wait_for_build(self, job_name, build_number, timeout=60):
        """
        Wait for a build to complete
        
        Args:
            job_name (str): Name of the Jenkins job
            build_number (int): Build number to wait for
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            dict: Build information
        """
        if build_number is None:
            return None
            
        print(f"Waiting for build #{build_number} to complete...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                build_info = self.server.get_build_info(job_name, build_number)
                if not build_info['building']:
                    result = build_info['result']
                    duration = build_info['duration'] / 1000  # Convert ms to s
                    print(f"Build #{build_number} completed: {result} (took: {duration:.2f}s)")
                    return build_info
                time.sleep(5)
            except jenkins.NotFoundException:
                print(f"Build #{build_number} not found")
                return None
        
        print(f"Timeout waiting for build #{build_number} to complete")
        return None

def main():
    """Main function demonstrating Jenkins API usage"""
    parser = argparse.ArgumentParser(description='Jenkins API Interaction Example')
    parser.add_argument('--url', default=os.environ.get('JENKINS_URL', 'http://localhost:8080'),
                        help='Jenkins server URL')
    parser.add_argument('--username', default=os.environ.get('JENKINS_USER', None),
                        help='Jenkins username')
    parser.add_argument('--api-token', default=os.environ.get('JENKINS_TOKEN', None),
                        help='Jenkins API token')
    parser.add_argument('--job', help='Job name to operate on')
    parser.add_argument('--build', action='store_true', help='Trigger a build for the specified job')
    parser.add_argument('--wait', action='store_true', help='Wait for build to complete')
    
    args = parser.parse_args()
    
    # Create Jenkins client
    client = JenkinsApiClient(args.url, args.username, args.api_token)
    
    # List all jobs if no specific job is provided
    if not args.job:
        client.get_jobs()
        return
    
    # Get job info
    job_info = client.get_job_info(args.job)
    if not job_info:
        return
    
    # Trigger build if requested
    if args.build:
        build_number = client.build_job(args.job)
        if build_number and args.wait:
            client.wait_for_build(args.job, build_number)

if __name__ == "__main__":
    main()
EOF

    chmod +x ~/jenkins-demo/scripts/jenkins_api_example.py
    print_success "Created Python script at: ~/jenkins-demo/scripts/jenkins_api_example.py"
    echo "This script demonstrates how to interact with Jenkins using the Python API."
    echo "It requires the python-jenkins package. Install it with:"
    echo -e "${BOLD}pip install python-jenkins${NC}"
}

# Function to create a Jenkinsfile example
create_jenkinsfile() {
    print_section "CREATING JENKINSFILE EXAMPLE"
    
    mkdir -p ~/jenkins-demo/pipeline-example
    cat > ~/jenkins-demo/pipeline-example/Jenkinsfile << 'EOF'
// Jenkins Pipeline Example
// =======================
//
// JENKINS CONCEPTS:
// ----------------
// Pipeline: A user-defined model of a CD pipeline, typically checked into source control
// Jenkinsfile: A text file that defines a Jenkins Pipeline using a DSL based on Groovy
// Stage: A logical grouping of steps that performs a specific part of the pipeline
// Step: A single task that tells Jenkins what to do at a particular point in time
// Node: A machine that is part of the Jenkins environment and capable of executing a Pipeline
// Agent: Instructs Jenkins to allocate an executor and workspace for the Pipeline

// This Jenkinsfile uses Declarative Pipeline syntax, which is more structured and easier to learn

pipeline {
    // Agent specifies where the pipeline will execute
    // 'any' means it can run on any available agent
    agent any
    
    // Environment variables available throughout the pipeline
    environment {
        // These variables will be available to all stages
        APP_NAME = 'jenkins-demo-app'
        VERSION = '1.0.0'
    }
    
    // Pipeline options
    options {
        // Keep only the last 5 builds
        buildDiscarder(logRotator(numToKeepStr: '5'))
        
        // Timeout for the entire pipeline (1 hour)
        timeout(time: 60, unit: 'MINUTES')
        
        // Don't run concurrent builds of the same branch
        disableConcurrentBuilds()
        
        // Add timestamps to console output
        timestamps()
    }
    
    // Tools configured in Jenkins
    tools {
        // Use the Maven installation named 'Default'
        // This requires Maven to be configured in Jenkins Global Tool Configuration
        maven 'Default'
        
        // Use JDK installation
        jdk 'JDK11'
    }
    
    // The stages of the pipeline
    stages {
        // Stage 1: Checkout code from source control
        stage('Checkout') {
            steps {
                // CONCEPT: Steps - individual actions within a stage
                echo 'Checking out code from source control...'
                
                // This would normally check out from your SCM
                // For demo, we'll just create a test file
                sh 'mkdir -p src/main/java'
                sh 'echo "public class HelloWorld { public static void main(String[] args) { System.out.println(\\"Hello from Jenkins!\\"); } }" > src/main/java/HelloWorld.java'
                
                // Print current directory and list files
                sh 'pwd && ls -la'
            }
        }
        
        // Stage 2: Build the application
        stage('Build') {
            steps {
                echo "Building ${env.APP_NAME} version ${env.VERSION}..."
                
                // Create a simple pom.xml file for Maven
                sh '''
                cat > pom.xml << 'EOL'
                <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
                  <modelVersion>4.0.0</modelVersion>
                  <groupId>com.example</groupId>
                  <artifactId>jenkins-demo</artifactId>
                  <packaging>jar</packaging>
                  <version>1.0-SNAPSHOT</version>
                  <name>jenkins-demo</name>
                  <url>http://maven.apache.org</url>
                  <properties>
                    <maven.compiler.source>11</maven.compiler.source>
                    <maven.compiler.target>11</maven.compiler.target>
                  </properties>
                </project>
                EOL
                '''
                
                // Build with Maven
                sh 'mvn clean package'
            }
            
            // CONCEPT: Post actions - actions to perform after the stage
            post {
                success {
                    echo 'Build successful! Archiving artifacts...'
                    // Archive the JAR file
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
                failure {
                    echo 'Build failed! Check the logs for details.'
                }
            }
        }
        
        // Stage 3: Run tests
        stage('Test') {
            steps {
                echo 'Running tests...'
                
                // Create a test file
                sh '''
                mkdir -p src/test/java
                cat > src/test/java/HelloWorldTest.java << 'EOL'
                public class HelloWorldTest {
                    public void testMain() {
                        // Pretend test
                        System.out.println("Tests passed!");
                    }
                }
                EOL
                '''
                
                // Run tests with Maven
                sh 'mvn test'
                
                // CONCEPT: JUnit test reporting
                // In a real project you'd use:
                // junit 'target/surefire-reports/*.xml'
            }
        }
        
        // Stage 4: Code quality analysis
        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                
                // CONCEPT: Parallel execution - run multiple tasks simultaneously
                parallel(
                    "Static Analysis": {
                        echo "Running static code analysis..."
                        // In a real project you'd use something like:
                        // sh 'mvn checkstyle:checkstyle'
                        sleep 2
                    },
                    "Security Scan": {
                        echo "Running security scan..."
                        // In a real project you'd use something like:
                        // sh 'mvn dependency-check:check'
                        sleep 3
                    }
                )
            }
        }
        
        // Stage 5: Deploy to staging
        stage('Deploy to Staging') {
            // CONCEPT: When condition - only run this stage on certain conditions
            when {
                expression { 
                    // Only deploy to staging if not a PR and on main branch
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' 
                }
            }
            
            // CONCEPT: Environment variables specific to a stage
            environment {
                DEPLOY_ENV = 'staging'
            }
            
            steps {
                echo "Deploying to ${DEPLOY_ENV}..."
                
                // In a real project you might use something like:
                // sh './deploy.sh staging'
                sleep 5
            }
        }
        
        // Stage 6: Approve production deployment
        stage('Approve Production Deployment') {
            // Only run on main/master branch
            when {
                expression { 
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' 
                }
            }
            
            // CONCEPT: Input step - pause for human approval
            steps {
                // This will pause the pipeline and wait for approval
                input message: 'Deploy to production?', ok: 'Deploy'
            }
        }
        
        // Stage 7: Deploy to production
        stage('Deploy to Production') {
            // Only run on main/master branch and after approval
            when {
                expression { 
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' 
                }
            }
            
            environment {
                DEPLOY_ENV = 'production'
            }
            
            steps {
                echo "Deploying to ${DEPLOY_ENV}..."
                
                // In a real project you might use something like:
                // sh './deploy.sh production'
                sleep 5
            }
            
            // CONCEPT: Post actions for the entire stage
            post {
                success {
                    // Send success notification
                    echo "Production deployment successful!"
                }
                failure {
                    // Send failure notification
                    echo "Production deployment failed!"
                }
            }
        }
    }
    
    // CONCEPT: Post-build actions for the entire pipeline
    post {
        always {
            echo "Pipeline completed, cleaning up workspace..."
            deleteDir() // Clean up workspace
        }
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
        unstable {
            echo "Pipeline is unstable!"
        }
        changed {
            echo "Pipeline state has changed since the last run!"
        }
    }
}
EOF

    print_success "Created Jenkinsfile at: ~/jenkins-demo/pipeline-example/Jenkinsfile"
    echo "This Jenkinsfile demonstrates a complete CI/CD pipeline with multiple stages."
}

# Function to create a Jenkins job configuration XML
create_jenkins_job_xml() {
    print_section "CREATING JENKINS JOB XML EXAMPLE"
    
    mkdir -p ~/jenkins-demo/job-configs
    cat > ~/jenkins-demo/job-configs/freestyle-job.xml << 'EOF'
<?xml version='1.1' encoding='UTF-8'?>
<!-- 
JENKINS CONCEPTS:
- Freestyle Project: The simplest job type in Jenkins
- XML Configuration: Jenkins stores job configurations as XML
- Build Steps: Individual actions to be performed during the build
- Build Triggers: Conditions that cause the build to start
- Post-build Actions: Actions to be performed after the build completes
-->
<project>
  <description>Example Freestyle Jenkins Job</description>
  
  <!-- Source Code Management -->
  <scm class="hudson.scm.NullSCM"/>
  
  <!-- Quiet period - wait this many seconds before starting build -->
  <quietPeriod>5</quietPeriod>
  
  <!-- Build Triggers -->
  <triggers>
    <!-- Poll SCM every hour -->
    <hudson.triggers.SCMTrigger>
      <spec>H * * * *</spec>
      <ignorePostCommitHooks>false</ignorePostCommitHooks>
    </hudson.triggers.SCMTrigger>
  </triggers>
  
  <!-- Build Environment -->
  <builders>
    <!-- Shell Build Step -->
    <hudson.tasks.Shell>
      <command>#!/bin/bash
echo "Hello from Jenkins Freestyle Job!"
echo "Current date: $(date)"
echo "Running as user: $(whoami)"
echo "Working directory: $(pwd)"
echo "Creating a test file..."
echo "Test content" > test-output.txt
      </command>
    </hudson.tasks.Shell>
  </builders>
  
  <!-- Post-build Actions -->
  <publishers>
    <!-- Archive Artifacts -->
    <hudson.tasks.ArtifactArchiver>
      <artifacts>*.txt</artifacts>
      <allowEmptyArchive>false</allowEmptyArchive>
      <onlyIfSuccessful>true</onlyIfSuccessful>
      <fingerprint>false</fingerprint>
    </hudson.tasks.ArtifactArchiver>
    
    <!-- Email Notification -->
    <hudson.tasks.Mailer plugin="mailer">
      <recipients>admin@example.com</recipients>
      <dontNotifyEveryUnstableBuild>false</dontNotifyEveryUnstableBuild>
      <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>
  </publishers>
  
  <!-- Job Properties -->
  <buildWrappers>
    <!-- Timeout if build takes more than 5 minutes -->
    <hudson.plugins.build__timeout.BuildTimeoutWrapper plugin="build-timeout">
      <strategy class="hudson.plugins.build_timeout.impl.AbsoluteTimeOutStrategy">
        <timeoutMinutes>5</timeoutMinutes>
      </strategy>
      <operationList>
        <hudson.plugins.build__timeout.operations.FailOperation/>
      </operationList>
    </hudson.plugins.build__timeout.BuildTimeoutWrapper>
  </buildWrappers>
</project>
EOF

    print_success "Created Jenkins job XML at: ~/jenkins-demo/job-configs/freestyle-job.xml"
    echo "This XML file demonstrates a complete Freestyle job configuration."
}

# Function to install Python and required packages
install_python_packages() {
    print_section "INSTALLING PYTHON AND REQUIRED PACKAGES"
    
    # Check if Python is installed
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        print_success "Python is already installed: $python_version"
    else
        print_warning "Python 3 is not installed. Installing Python 3..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
        
        # Verify installation
        if command -v python3 &> /dev/null; then
            python_version=$(python3 --version)
            print_success "Python installed successfully: $python_version"
        else
            print_error "Failed to install Python. Please install it manually."
            exit 1
        fi
    fi
    
    # Install required Python packages
    print_warning "Installing required Python packages..."
    pip3 install --user python-jenkins
    
    print_success "Python packages installed successfully"
}

# Function to create a README file
create_readme() {
    print_section "CREATING README"
    
    cat > ~/jenkins-demo/README.md << 'EOF'
# Jenkins Zero to Hero Demo

This directory contains examples and scripts for learning Jenkins, created by an automated setup script.

## Directory Structure

- `scripts/`: Contains Python scripts for interacting with Jenkins API
  - `jenkins_api_example.py`: Example script demonstrating Jenkins API usage
- `pipeline-example/`: Contains Jenkinsfile example
  - `Jenkinsfile`: Complete pipeline example with multiple stages
- `job-configs/`: Contains Jenkins job configuration XML examples
  - `freestyle-job.xml`: Example freestyle job configuration

## Key Jenkins Concepts

### Jenkins Architecture
- **Master**: The main Jenkins server that coordinates builds and manages the Jenkins environment
- **Agent/Node**: A machine connected to the master that can execute jobs
- **Executor**: A slot for execution on a node (a node can have multiple executors)

### Job Types
- **Freestyle**: Simple, single-task jobs
- **Pipeline**: Complex, multi-stage workflows defined in a Jenkinsfile
- **Multibranch Pipeline**: Pipeline that automatically creates sub-jobs for branches in source control
- **Folder**: Organizes jobs into folders

### Pipeline Concepts
- **Declarative Pipeline**: Structured way to define pipelines (begins with `pipeline { }`)
- **Scripted Pipeline**: Flexible, Groovy-based syntax for defining pipelines
- **Stage**: Logical grouping of steps (e.g., Build, Test, Deploy)
- **Step**: Individual task within a stage
- **Agent**: Specifies where the pipeline should execute
- **Post**: Actions to perform after a stage or the entire pipeline

### Triggers
- **SCM Polling**: Periodically check source control for changes
- **Webhooks**: Trigger builds in response to external events
- **Timer**: Schedule builds to run at specific times
- **Upstream/Downstream**: Trigger builds after another job completes

### Security
- **Authentication**: Verifying user identity
- **Authorization**: Controlling what users can do
- **Matrix-based security**: Fine-grained access control
- **Role-based security**: Assigning permissions via roles

### Advanced Features
- **Shared Libraries**: Reusable code for pipelines
- **Parameterized Builds**: Builds that accept parameters
- **Artifacts**: Files generated during builds that can be archived
- **Plugins**: Extend Jenkins functionality (there are thousands available)

## Using the Examples

1. **Jenkins API Script**:
   ```
   cd ~/jenkins-demo/scripts
   python3 jenkins_api_example.py --url http://localhost:8080 --username admin --api-token YOUR_API_TOKEN
   ```

2. **Creating a Pipeline Job**:
   - In Jenkins, create a new Pipeline job
   - Configure it to use SCM for the pipeline definition
   - Point it to a repository containing the provided Jenkinsfile

3. **Creating a Freestyle Job**:
   - In Jenkins, install the "Job Import Plugin"
   - Use it to import the XML job configuration from `job-configs/freestyle-job.xml`

## Further Learning Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Guided Tour](https://www.jenkins.io/doc/pipeline/tour/getting-started/)
- [Jenkins YouTube Channel](https://www.youtube.com/c/jenkinscicd)
EOF

    print_success "Created README at: ~/jenkins-demo/README.md"
}

# Function to display Jenkins setup instructions
display_jenkins_instructions() {
    print_section "JENKINS SETUP INSTRUCTIONS"
    
    echo -e "${BOLD}Accessing Jenkins:${NC}"
    echo -e "  1. Open your browser and navigate to ${BOLD}http://localhost:8080${NC}"
    echo -e "  2. For the initial setup, use the admin password shown earlier"
    echo -e "     (You can retrieve it again with: ${BOLD}sudo cat /var/lib/jenkins/secrets/initialAdminPassword${NC})"
    
    echo -e "\n${BOLD}Initial Jenkins Setup:${NC}"
    echo -e "  1. Install suggested plugins (or select specific plugins)"
    echo -e "  2. Create an admin user when prompted"
    echo -e "  3. Configure Jenkins URL (default is fine for local development)"
    
    echo -e "\n${BOLD}Recommended Plugins:${NC}"
    echo -e "  - ${BOLD}Pipeline${NC}: Allows creating pipeline jobs (already included in suggested plugins)"
    echo -e "  - ${BOLD}Blue Ocean${NC}: Modern UI for Jenkins pipelines"
    echo -e "  - ${BOLD}Job Import Plugin${NC}: For importing the XML job config provided"
    echo -e "  - ${BOLD}Git Integration${NC}: For source code management (already included in suggested plugins)"
    
    echo -e "\n${BOLD}Setting up a Pipeline Job:${NC}"
    echo -e "  1. Click 'New Item' in Jenkins"
    echo -e "  2. Enter a name and select 'Pipeline'"
    echo -e "  3. In the configuration, scroll down to the Pipeline section"
    echo -e "  4. Select 'Pipeline script from SCM' if your Jenkinsfile is in a repository"
    echo -e "  5. Or copy the contents of ~/jenkins-demo/pipeline-example/Jenkinsfile into the script area"
    
    echo -e "\n${BOLD}For More Information:${NC}"
    echo -e "  - See the README.md file in ~/jenkins-demo/ for more instructions"
    echo -e "  - Explore the example files created in ~/jenkins-demo/"
}

# Main script execution
clear
echo -e "${BOLD}${BLUE}=======================================================${NC}"
echo -e "${BOLD}${BLUE}       JENKINS ZERO TO HERO SETUP SCRIPT              ${NC}"
echo -e "${BOLD}${BLUE}=======================================================${NC}"
echo -e "This script will setup Jenkins, create example files, and provide"
echo -e "detailed explanations of Jenkins concepts."
echo -e "${BOLD}${BLUE}=======================================================${NC}"
echo

# Confirm execution
read -p "Do you want to proceed with the setup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup aborted."
    exit 0
fi

# Run all the functions
check_wsl_ubuntu
install_java
install_jenkins
install_python_packages
create_python_script
create_jenkinsfile
create_jenkins_job_xml
create_readme
display_jenkins_instructions

# Final message
print_section "SETUP COMPLETE"
echo -e "${GREEN}Jenkins Zero to Hero setup completed successfully!${NC}"
echo -e "All example files have been created in: ${BOLD}~/jenkins-demo/${NC}"
echo -e "Follow the instructions above to complete the Jenkins configuration."
echo -e "\n${YELLOW}Happy Jenkins-ing!${NC}"
