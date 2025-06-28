# GitHub Repository Setup Guide

This guide will help you create and configure the UAV Path Planning Demo repository on GitHub.

## Prerequisites

1. **Git** - Version control system

   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

2. **GitHub CLI** - Command line interface for GitHub

   - Download from: https://cli.github.com/
   - Verify installation: `gh --version`

3. **GitHub Account** - You need a GitHub account
   - Create at: https://github.com/

## Step-by-Step Setup

### 1. Authenticate with GitHub

First, authenticate with GitHub using the CLI:

```bash
gh auth login
```

Follow the prompts to authenticate. Choose:

- GitHub.com
- HTTPS
- Yes to authenticate Git operations
- Login with a web browser (recommended)

### 2. Automatic Setup (Recommended)

Use the provided setup script:

```bash
python setup_github.py
```

The script will:

- Check prerequisites
- Create the repository on GitHub
- Initialize local git repository
- Add all files and commit
- Push to GitHub

### 3. Manual Setup (Alternative)

If you prefer to set up manually:

#### Create Repository on GitHub

```bash
gh repo create uav-path-planning-demo --public --description "UAV Path Planning Simulation Demo"
```

#### Initialize Local Repository

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: UAV Path Planning Demo"

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/uav-path-planning-demo.git

# Push to GitHub
git push -u origin main
```

## Repository Configuration

### Update Repository URL

After creating the repository, update the URL in these files:

1. **README.md** - Update the clone URL
2. **setup.py** - Update the repository URL
3. **QUICKSTART.md** - Update the clone URL

### Repository Settings

Configure these settings on GitHub:

1. **Description**: "UAV Path Planning Simulation Demo - A demonstration of UAV path planning and target acquisition simulation"

2. **Topics**: Add relevant topics like:

   - uav
   - path-planning
   - simulation
   - python
   - robotics
   - computer-vision

3. **Website**: (Optional) Add your research page URL

4. **Social Preview**: Upload a screenshot of the simulation

## Repository Features

### GitHub Pages (Optional)

Enable GitHub Pages to create a project website:

1. Go to repository Settings
2. Scroll to "Pages" section
3. Select source: "Deploy from a branch"
4. Select branch: "main"
5. Select folder: "/ (root)"
6. Click "Save"

### Issues and Discussions

Enable these features for community interaction:

1. **Issues**: For bug reports and feature requests
2. **Discussions**: For questions and community interaction
3. **Wiki**: For additional documentation

### Branch Protection

Protect the main branch:

1. Go to Settings > Branches
2. Add rule for "main" branch
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators

## Content Guidelines

### What's Included

✅ **Safe to include:**

- Demo simulation code
- Basic visualization
- Simplified algorithms
- Documentation
- Setup scripts
- License and README

❌ **Not included (Protected):**

- Proprietary algorithms
- Advanced research implementations
- Rust engine code
- Database schemas
- Performance optimizations
- Research data

### Intellectual Property Protection

1. **License**: MIT License with IP notice
2. **README**: Clear disclaimer about demo nature
3. **Code**: Simplified implementations only
4. **Contact**: Research team contact information

## Maintenance

### Regular Updates

1. **Dependencies**: Keep requirements.txt updated
2. **Documentation**: Update README and guides
3. **Issues**: Respond to community feedback
4. **Releases**: Create releases for major updates

### Version Management

Use semantic versioning:

```bash
# Create a new release
git tag v1.0.0
git push origin v1.0.0

# Create GitHub release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Initial release"
```

## Community Guidelines

### Contributing

Create a CONTRIBUTING.md file with:

1. Code of conduct
2. Contribution guidelines
3. Development setup
4. Testing requirements

### Code of Conduct

Create a CODE_OF_CONDUCT.md file based on:

- Contributor Covenant
- GitHub's community guidelines

## Analytics and Insights

Monitor repository activity:

1. **Traffic**: View clone/download statistics
2. **Issues**: Track community engagement
3. **Stars**: Monitor project popularity
4. **Forks**: Track community interest

## Security

### Security Policy

Create a SECURITY.md file with:

1. Supported versions
2. Reporting process
3. Disclosure policy
4. Security contacts

### Dependencies

Regularly check for vulnerabilities:

```bash
# Check for security vulnerabilities
pip-audit

# Update dependencies
pip-review --auto
```

## Final Steps

1. **Test the demo** locally before pushing
2. **Update documentation** with correct URLs
3. **Create initial release** on GitHub
4. **Share the repository** with your network
5. **Monitor feedback** and respond to issues

## Support

For help with GitHub setup:

- GitHub Documentation: https://docs.github.com/
- GitHub CLI Documentation: https://cli.github.com/
- GitHub Community: https://github.community/

For research-related questions:

- **Author**: Solomon Makuwa
- **Email**: 202211185@spu.ac.za
- **Institution**: Sol Plaatje University
