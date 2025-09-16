<script>
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";

  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

<svelte:head>
  <title>Contributing - BDS Search Platform</title>
  <meta name="description" content="Learn how to contribute to the BDS Search Platform through data submissions, technical contributions, financial support, and community engagement." />
</svelte:head>

{#if mounted}
  <div class="page-container" in:fade={{ duration: 600 }}>
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content" in:fly={{ y: 30, duration: 800, delay: 200 }}>
        <h1 class="hero-title">Contributing</h1>
        <p class="hero-description">
          Help improve and expand the BDS Search Platform through data contributions, technical support, or community engagement.
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Data Contributions Section -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 400 }}>
        <div class="section-header">
          <Icon icon="mdi:database-plus" class="section-icon" />
          <h2 class="section-title">Data Contributions</h2>
        </div>
        <div class="section-content">
          <p>
            The accuracy and comprehensiveness of our database depends on community contributions. We welcome submissions of verified information about corporate involvement in activities targeted by BDS campaigns.
          </p>

          <div class="contribution-types">
            <div class="contribution-card">
              <div class="card-header">
                <Icon icon="mdi:file-document-plus" class="card-icon" />
                <h3>Research Submissions</h3>
              </div>
              <p>Submit new research findings, reports, or documented evidence of corporate involvement.</p>
              <div class="requirements">
                <h4>Requirements:</h4>
                <ul>
                  <li>Verifiable sources and documentation</li>
                  <li>Clear description of corporate involvement</li>
                  <li>Date and context of involvement</li>
                  <li>Contact information for follow-up questions</li>
                </ul>
              </div>
              <a href="mailto:press@ucinvestments.info?subject=Data Submission - BDS Search" class="cta-button">
                <Icon icon="mdi:email" />
                Submit Research
              </a>
            </div>

            <div class="contribution-card">
              <div class="card-header">
                <Icon icon="mdi:alert-circle" class="card-icon" />
                <h3>Corrections & Updates</h3>
              </div>
              <p>Help us maintain accuracy by reporting outdated information, errors, or missing details.</p>
              <div class="requirements">
                <h4>How to Report:</h4>
                <ul>
                  <li>Include the company name and ID from our database</li>
                  <li>Specify what information needs correction</li>
                  <li>Provide updated information with sources</li>
                  <li>Explain the significance of the correction</li>
                </ul>
              </div>
              <a href="mailto:press@ucinvestments.info?subject=Data Correction - BDS Search" class="cta-button">
                <Icon icon="mdi:pencil" />
                Report Correction
              </a>
            </div>

            <div class="contribution-card">
              <div class="card-header">
                <Icon icon="mdi:link" class="card-icon" />
                <h3>Source Integration</h3>
              </div>
              <p>Suggest new data sources or help integrate existing databases from credible BDS-related organizations.</p>
              <div class="requirements">
                <h4>Source Criteria:</h4>
                <ul>
                  <li>Established organization with clear methodology</li>
                  <li>Publicly accessible or licensable data</li>
                  <li>Regular updates and maintenance</li>
                  <li>Alignment with BDS principles and goals</li>
                </ul>
              </div>
              <a href="mailto:dev@ucinvestments.info?subject=New Data Source - BDS Search" class="cta-button">
                <Icon icon="mdi:source-branch" />
                Suggest Source
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Technical Contributions Section -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 500 }}>
        <div class="section-header">
          <Icon icon="mdi:code-tags" class="section-icon" />
          <h2 class="section-title">Technical Contributions</h2>
        </div>
        <div class="section-content">
          <p>
            The BDS Search Platform is built with modern web technologies and welcomes technical contributions from developers who support the mission.
          </p>

          <div class="tech-stack">
            <h3>Technology Stack</h3>
            <div class="tech-grid">
              <div class="tech-item">
                <Icon icon="mdi:language-javascript" class="tech-icon" />
                <span>SvelteKit</span>
              </div>
              <div class="tech-item">
                <Icon icon="mdi:language-typescript" class="tech-icon" />
                <span>TypeScript</span>
              </div>
              <div class="tech-item">
                <Icon icon="mdi:database" class="tech-icon" />
                <span>PostgreSQL</span>
              </div>
              <div class="tech-item">
                <Icon icon="mdi:docker" class="tech-icon" />
                <span>Docker</span>
              </div>
              <div class="tech-item">
                <Icon icon="mdi:language-python" class="tech-icon" />
                <span>Python</span>
              </div>
              <div class="tech-item">
                <Icon icon="mdi:tailwindcss" class="tech-icon" />
                <span>Tailwind CSS</span>
              </div>
            </div>
          </div>

          <div class="contribution-areas">
            <h3>Areas for Contribution</h3>
            <div class="areas-grid">
              <div class="area-card">
                <Icon icon="mdi:magnify" class="area-icon" />
                <h4>Search Improvements</h4>
                <p>Enhance search algorithms, add filters, improve relevance scoring</p>
              </div>
              <div class="area-card">
                <Icon icon="mdi:chart-line" class="area-icon" />
                <h4>Data Visualization</h4>
                <p>Create charts, graphs, and interactive visualizations for insights</p>
              </div>
              <div class="area-card">
                <Icon icon="mdi:api" class="area-icon" />
                <h4>API Development</h4>
                <p>Expand API endpoints, improve performance, add new features</p>
              </div>
              <div class="area-card">
                <Icon icon="mdi:phone" class="area-icon" />
                <h4>Mobile Experience</h4>
                <p>Optimize mobile interface, create progressive web app features</p>
              </div>
              <div class="area-card">
                <Icon icon="mdi:translate" class="area-icon" />
                <h4>Internationalization</h4>
                <p>Add multi-language support, localize content and interface</p>
              </div>
              <div class="area-card">
                <Icon icon="mdi:shield-check" class="area-icon" />
                <h4>Security & Privacy</h4>
                <p>Enhance security measures, improve data protection practices</p>
              </div>
            </div>
          </div>

          <div class="github-section">
            <h3>Getting Started</h3>
            <p>
              The project is open source and hosted on GitHub. Contributors should follow the established code style and contribute through pull requests.
            </p>
            <div class="github-actions">
              <a href="https://github.com/TheArctesian/BDS-Search" target="_blank" rel="noopener noreferrer" class="github-button">
                <Icon icon="mdi:github" />
                View Repository
                <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
              <a href="mailto:dev@ucinvestments.info?subject=Technical Contribution - BDS Search" class="github-button secondary">
                <Icon icon="mdi:email" />
                Contact Developer
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Financial Support Section -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 600 }}>
        <div class="section-header">
          <Icon icon="mdi:heart" class="section-icon" />
          <h2 class="section-title">Financial Support</h2>
        </div>
        <div class="section-content">
          <p>
            The BDS Search Platform is currently self-funded. Financial contributions help cover hosting costs, database maintenance, and development time.
          </p>

          <div class="support-info">
            <div class="support-card">
              <h3>Current Costs</h3>
              <ul>
                <li>Database hosting and backups</li>
                <li>Web hosting and CDN</li>
                <li>Domain registration and SSL certificates</li>
                <li>Development tools and services</li>
                <li>Data processing and storage</li>
              </ul>
            </div>

            <div class="support-card">
              <h3>Donation Options</h3>
              <div class="crypto-options">
                <div class="crypto-address">
                  <strong>Ethereum (ETH):</strong>
                  <code class="address">0x623c7559ddC51BAf15Cc81bf5bc13c0B0EA14c01</code>
                </div>
                <div class="crypto-address">
                  <strong>Monero (XMR):</strong>
                  <code class="address">44bvXALNkxUgSkGChKQPnj79v6JwkeYEkGijgKyp2zRq3EiuL6oewAv5u2c7FN7jbN1z7uj1rrPfL77bbsJ3cC8U2ADFoTj</code>
                </div>
                <p class="alt-contact">
                  For other donation methods, please <a href="mailto:admin@ucinvestments.info?subject=Donation - BDS Search">contact admin</a>.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Community Engagement Section -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 700 }}>
        <div class="section-header">
          <Icon icon="mdi:account-group" class="section-icon" />
          <h2 class="section-title">Community Engagement</h2>
        </div>
        <div class="section-content">
          <p>
            Help spread awareness about the platform and its mission through community engagement and education.
          </p>

          <div class="engagement-options">
            <div class="engagement-card">
              <Icon icon="mdi:share" class="engagement-icon" />
              <h3>Share the Platform</h3>
              <p>Share the BDS Search Platform with organizations, activists, and individuals who would benefit from this resource.</p>
            </div>

            <div class="engagement-card">
              <Icon icon="mdi:school" class="engagement-icon" />
              <h3>Educational Use</h3>
              <p>Use the platform as a teaching tool in courses on corporate responsibility, social justice, or Middle Eastern studies.</p>
            </div>

            <div class="engagement-card">
              <Icon icon="mdi:forum" class="engagement-icon" />
              <h3>Feedback & Ideas</h3>
              <p>Provide feedback on the platform's usability, suggest new features, or share ideas for improvement.</p>
            </div>

            <div class="engagement-card">
              <Icon icon="mdi:handshake" class="engagement-icon" />
              <h3>Partnerships</h3>
              <p>Connect us with organizations that might benefit from integration or data sharing partnerships.</p>
            </div>
          </div>

          <div class="contact-section">
            <h3>Get Involved</h3>
            <p>
              Ready to contribute? Whether you have data to share, technical skills to offer, or ideas to discuss, we'd love to hear from you.
            </p>
            <div class="contact-buttons">
              <a href="mailto:admin@ucinvestments.info?subject=Contributing to BDS Search" class="contact-button">
                <Icon icon="mdi:email" />
                Contact Admin
              </a>
              <a href="mailto:press@ucinvestments.info?subject=Research Contribution" class="contact-button secondary">
                <Icon icon="mdi:database" />
                Submit Data
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  .page-container {
    min-height: 100vh;
  }

  .hero-section {
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    position: relative;
    overflow: hidden;
  }

  .hero-section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  .hero-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    text-align: center;
    position: relative;
    z-index: 1;
  }

  .hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
  }

  .hero-description {
    max-width: 700px;
    margin: 0 auto;
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.6;
  }

  .main-content {
    max-width: 1000px;
    margin: 0 auto;
    padding: 4rem 2rem;
  }

  .content-section {
    margin-bottom: 4rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  :global(.section-icon) {
    font-size: 2rem;
    color: var(--founder);
  }

  .section-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .section-content {
    line-height: 1.7;
    color: var(--text-primary);
  }

  .section-content h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 2rem 0 1rem 0;
  }

  .contribution-types {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .contribution-card {
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .contribution-card:hover {
    border-color: var(--founder);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  :global(.card-icon) {
    font-size: 1.5rem;
    color: var(--founder);
  }

  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }

  .requirements {
    margin: 1.5rem 0;
  }

  .requirements h4 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
  }

  .requirements ul {
    margin: 0;
    padding-left: 1.5rem;
  }

  .requirements li {
    margin-bottom: 0.25rem;
    color: var(--text-secondary);
  }

  .cta-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--founder);
    color: white;
    text-decoration: none;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
    margin-top: 1rem;
  }

  .cta-button:hover {
    background: var(--pri);
    transform: translateY(-2px);
  }

  .tech-stack {
    margin: 2rem 0;
  }

  .tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .tech-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    font-weight: 500;
  }

  :global(.tech-icon) {
    font-size: 1.25rem;
    color: var(--founder);
  }

  .areas-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
  }

  .area-card {
    padding: 1.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    text-align: center;
  }

  :global(.area-icon) {
    font-size: 2rem;
    color: var(--founder);
    margin-bottom: 0.5rem;
  }

  .area-card h4 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0.5rem 0;
  }

  .area-card p {
    color: var(--text-secondary);
    margin: 0;
  }

  .github-section {
    margin-top: 2rem;
    padding: 2rem;
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border: 1px solid var(--border);
    border-radius: 1rem;
  }

  .github-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .github-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--text-primary);
    color: white;
    text-decoration: none;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .github-button:hover {
    background: var(--founder);
    transform: translateY(-2px);
  }

  .github-button.secondary {
    background: var(--border);
    color: var(--text-primary);
  }

  .github-button.secondary:hover {
    background: var(--founder);
    color: white;
  }

  :global(.external-icon) {
    font-size: 0.875rem;
  }

  .support-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .support-card {
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: var(--shadow-sm);
  }

  .support-card h3 {
    margin-top: 0;
    color: var(--pri);
  }

  .support-card ul {
    margin: 0;
    padding-left: 1.5rem;
  }

  .support-card li {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
  }

  .crypto-options {
    margin-top: 1rem;
  }

  .crypto-address {
    margin-bottom: 1rem;
  }

  .crypto-address strong {
    display: block;
    color: var(--pri);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
  }

  .address {
    display: block;
    background: var(--bg-secondary);
    padding: 0.75rem;
    border-radius: 0.25rem;
    font-family: "JetBrains Mono", monospace;
    font-size: 0.75rem;
    word-break: break-all;
    border: 1px solid var(--border);
    color: var(--text-primary);
    cursor: text;
    user-select: all;
  }

  .alt-contact {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 1rem;
  }

  .alt-contact a {
    color: var(--founder);
    text-decoration: none;
    font-weight: 500;
  }

  .alt-contact a:hover {
    color: var(--pri);
    text-decoration: underline;
  }

  .engagement-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .engagement-card {
    padding: 1.5rem;
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .engagement-card:hover {
    border-color: var(--founder);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  :global(.engagement-icon) {
    font-size: 2rem;
    color: var(--founder);
    margin-bottom: 1rem;
  }

  .engagement-card h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 1rem 0;
  }

  .engagement-card p {
    color: var(--text-secondary);
    margin: 0;
  }

  .contact-section {
    margin-top: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border: 1px solid var(--border);
    border-radius: 1rem;
    text-align: center;
  }

  .contact-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
  }

  .contact-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--founder);
    color: white;
    text-decoration: none;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .contact-button:hover {
    background: var(--pri);
    transform: translateY(-2px);
  }

  .contact-button.secondary {
    background: var(--border);
    color: var(--text-primary);
  }

  .contact-button.secondary:hover {
    background: var(--founder);
    color: white;
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 2rem;
    }

    .hero-description {
      font-size: 1.125rem;
    }

    .main-content {
      padding: 2rem 1rem;
    }

    .section-title {
      font-size: 1.5rem;
    }

    .contribution-types {
      grid-template-columns: 1fr;
    }

    .github-actions {
      flex-direction: column;
    }

    .contact-buttons {
      flex-direction: column;
      align-items: center;
    }

    .tech-grid {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
  }
</style>