import subprocess
import sys

# Define categories and the packages in each category
categories = {
    "Programming Languages": [
        ("Python 3", "python3"),
        ("Python 3 Pip", "python3-pip"),
        ("GCC", "gcc"),
        ("G++", "g++"),
        ("Java", "openjdk-11-jdk"),  # Example: Java
        ("Ruby", "ruby"),            # Example: Ruby
        ("Go", "golang-go"),         # Example: Go
        ("Rust", "rustc"),           # Example: Rust
    ],
    "Databases": [
        ("SQLite3", "sqlite3"),
        ("MySQL Server", "mysql-server"),  # Example: MySQL
        ("PostgreSQL", "postgresql"),      # Example: PostgreSQL
        ("MongoDB", "mongodb"),            # Example: MongoDB
        ("Redis", "redis-server"),         # Example: Redis
        ("Cassandra", "cassandra"),        # Example: Cassandra
    ],
    "Version Control": [
        ("Git", "git"),
        ("Mercurial", "mercurial"),  # Example: Mercurial
        ("SVN", "subversion"),       # Example: SVN
        ("Bazaar", "bzr"),           # Example: Bazaar
    ],
    "Web Server": [
        ("Nginx", "nginx"),
        ("Apache2", "apache2"),         # Example: Apache HTTP Server
        ("Node.js", "nodejs"),          # Example: Node.js
        ("Ruby on Rails", "rails"),     # Example: Ruby on Rails
        ("Django", "python3-django"),   # Example: Django
        ("Flask", "python3-flask"),     # Example: Flask
    ],
    "Deployment": [
        ("Docker", "docker-ce"),  # Example: Docker
        ("Kubernetes", "kubeadm"),  # Example: Kubernetes
        ("Ansible", "ansible"),    # Example: Ansible
        ("Jenkins", "jenkins"),    # Example: Jenkins
        ("Terraform", "terraform"),  # Example: Terraform
    ],
}

# Function to install packages using apt package manager (for Debian-based systems)
def install_packages_apt(packages):
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y"] + packages)
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

# Function to install packages using yum package manager (for Red Hat-based systems)
def install_packages_yum(packages):
    try:
        subprocess.check_call(["sudo", "yum", "install", "-y"] + packages)
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

# Function to install packages based on selected categories and options
def install_categories(selected_categories):
    for category, options in selected_categories.items():
        if category in categories:
            print(f"Installing {category}...")
            install_packages = [package for name, package in categories[category] if name in options]
            if install_packages:
                print(f"Installing {', '.join(install_packages)}...")
                if distro_id == "debian" or distro_id == "ubuntu":
                    install_packages_apt(install_packages)
                elif distro_id == "centos" or distro_id == "rhel":
                    install_packages_yum(install_packages)
            else:
                print(f"No packages selected for {category}. Skipping.")
            print(f"{category} installation complete.\n")
        else:
            print(f"Skipping unknown category: {category}")

# Check the Linux distribution and choose the appropriate package manager
try:
    with open("/etc/os-release", "r") as os_release:
        for line in os_release:
            if line.startswith("ID="):
                distro_id = line.split("=")[1].strip()
                break
    if distro_id == "debian" or distro_id == "ubuntu":
        package_manager = "apt"
    elif distro_id == "centos" or distro_id == "rhel":
        package_manager = "yum"
    else:
        print("Unsupported Linux distribution.")
        sys.exit(1)
except FileNotFoundError:
    print("Unable to determine the Linux distribution.")
    sys.exit(1)

# Display available categories and options and prompt the user to select categories and options for installation
selected_categories = {}
print("Available Categories:")
for category, options in categories.items():
    print(f"{category}:")
    for option_name, option_package in options:
        print(f"  {option_name}")
    user_input = input(f"Select options for {category} (comma-separated, or leave empty to skip): ")
    selected_options = [option.strip() for option in user_input.split(",")]
    selected_categories[category] = selected_options

# Install selected categories and options
install_categories(selected_categories)

print("Development environment setup complete.")
