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
  <title>Resources - BDS Search Platform</title>
  <meta name="description" content="Essential resources for understanding the BDS movement, corporate accountability, and ethical investment decisions." />
</svelte:head>

{#if mounted}
  <div class="page-container" in:fade={{ duration: 600 }}>
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content" in:fly={{ y: 30, duration: 800, delay: 200 }}>
        <h1 class="hero-title">Resources</h1>
        <p class="hero-description">
          Essential resources for understanding the BDS movement, corporate accountability, and making informed ethical decisions.
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- BDS Movement Resources -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 400 }}>
        <div class="section-header">
          <Icon icon="mdi:flag" class="section-icon" />
          <h2 class="section-title">BDS Movement</h2>
        </div>
        <div class="section-content">
          <p>
            Learn about the origins, goals, and strategies of the Boycott, Divestment, Sanctions movement.
          </p>
          <div class="resources-grid">
            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:web" class="card-icon" />
                <h3>Official BDS Website</h3>
              </div>
              <p>The official website of the Palestinian-led BDS movement with campaigns, news, and resources.</p>
              <a href="https://bdsmovement.net/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Visit Site <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:book" class="card-icon" />
                <h3>BDS Call</h3>
              </div>
              <p>The original 2005 call for boycott, divestment and sanctions from Palestinian civil society.</p>
              <a href="https://bdsmovement.net/call" target="_blank" rel="noopener noreferrer" class="resource-link">
                Read Call <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:gavel" class="card-icon" />
                <h3>Legal Analysis</h3>
              </div>
              <p>Legal resources defending the right to boycott and supporting BDS advocacy.</p>
              <a href="https://palestinelegal.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Palestine Legal <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Research Organizations -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 500 }}>
        <div class="section-header">
          <Icon icon="mdi:magnify" class="section-icon" />
          <h2 class="section-title">Research Organizations</h2>
        </div>
        <div class="section-content">
          <div class="resources-grid">
            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:chart-pie" class="card-icon" />
                <h3>Who Profits</h3>
              </div>
              <p>Research center documenting corporate involvement in human rights violations in Palestine.</p>
              <a href="https://whoprofits.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Visit Site <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:peace" class="card-icon" />
                <h3>AFSC Investigate</h3>
              </div>
              <p>American Friends Service Committee's database tracking corporate complicity.</p>
              <a href="https://investigate.afsc.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Investigate <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:account-group" class="card-icon" />
                <h3>Adalah</h3>
              </div>
              <p>Legal center for Arab minority rights in Israel with research on discrimination.</p>
              <a href="https://www.adalah.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Visit Site <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Ethical Investment -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 600 }}>
        <div class="section-header">
          <Icon icon="mdi:finance" class="section-icon" />
          <h2 class="section-title">Ethical Investment</h2>
        </div>
        <div class="section-content">
          <div class="resources-grid">
            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:school" class="card-icon" />
                <h3>Divest This!</h3>
              </div>
              <p>Campus divestment campaigns and resources for students and faculty.</p>
              <a href="https://divestthis.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Learn More <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:church" class="card-icon" />
                <h3>Fossil Free</h3>
              </div>
              <p>Resources on divestment strategies and ethical investment alternatives.</p>
              <a href="https://gofossilfree.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                Visit Site <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:handshake" class="card-icon" />
                <h3>SRI Guidelines</h3>
              </div>
              <p>Socially responsible investing principles and screening methodologies.</p>
              <a href="https://www.unpri.org/" target="_blank" rel="noopener noreferrer" class="resource-link">
                UN PRI <Icon icon="mdi:open-in-new" class="external-icon" />
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Academic Resources -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 700 }}>
        <div class="section-header">
          <Icon icon="mdi:school-outline" class="section-icon" />
          <h2 class="section-title">Academic Resources</h2>
        </div>
        <div class="section-content">
          <div class="academic-list">
            <div class="academic-item">
              <h3>Reports & Studies</h3>
              <ul>
                <li><a href="https://www.btselem.org/" target="_blank">B'Tselem - Human Rights Reports</a></li>
                <li><a href="https://www.amnesty.org/en/countries/middle-east-and-north-africa/israel-and-occupied-palestinian-territories/" target="_blank">Amnesty International - Palestine/Israel</a></li>
                <li><a href="https://www.hrw.org/middle-east/north-africa/israel/palestine" target="_blank">Human Rights Watch - Palestine</a></li>
              </ul>
            </div>

            <div class="academic-item">
              <h3>Research Journals</h3>
              <ul>
                <li><a href="https://www.tandfonline.com/toc/fjps20/current" target="_blank">Journal of Palestine Studies</a></li>
                <li><a href="https://www.tandfonline.com/toc/cmes20/current" target="_blank">Middle Eastern Studies</a></li>
                <li><a href="https://www.cambridge.org/core/journals/international-organization" target="_blank">International Organization</a></li>
              </ul>
            </div>

            <div class="academic-item">
              <h3>Educational Materials</h3>
              <ul>
                <li><a href="https://teachpalestine.org/" target="_blank">Teach Palestine Project</a></li>
                <li><a href="https://www.palestineportal.org/" target="_blank">Palestine Portal</a></li>
                <li><a href="https://www.ifamericansknew.org/" target="_blank">If Americans Knew</a></li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Tools & Platforms -->
      <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 800 }}>
        <div class="section-header">
          <Icon icon="mdi:tools" class="section-icon" />
          <h2 class="section-title">Tools & Platforms</h2>
        </div>
        <div class="section-content">
          <div class="resources-grid">
            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:shopping" class="card-icon" />
                <h3>Boycott Apps</h3>
              </div>
              <p>Mobile applications to help consumers make informed purchasing decisions.</p>
              <div class="app-links">
                <a href="https://boycott.thewitness.news/" target="_blank" class="app-link">Boycott.thewitness</a>
                <a href="https://buycott.com/" target="_blank" class="app-link">Buycott</a>
              </div>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:newspaper" class="card-icon" />
                <h3>News Sources</h3>
              </div>
              <p>Reliable news sources covering Palestine and BDS campaigns.</p>
              <div class="app-links">
                <a href="https://electronicintifada.net/" target="_blank" class="app-link">Electronic Intifada</a>
                <a href="https://mondoweiss.net/" target="_blank" class="app-link">Mondoweiss</a>
              </div>
            </div>

            <div class="resource-card">
              <div class="card-header">
                <Icon icon="mdi:database" class="card-icon" />
                <h3>Data Sources</h3>
              </div>
              <p>Open data and research databases for further analysis.</p>
              <div class="app-links">
                <a href="https://data.un.org/" target="_blank" class="app-link">UN Data</a>
                <a href="https://www.ochaopt.org/" target="_blank" class="app-link">OCHA oPt</a>
              </div>
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

  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .resource-card {
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    padding: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .resource-card:hover {
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
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }

  .resource-card p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }

  .resource-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--founder);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .resource-link:hover {
    color: var(--pri);
  }

  :global(.external-icon) {
    font-size: 0.875rem;
  }

  .academic-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .academic-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 1.5rem;
  }

  .academic-item h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0 0 1rem 0;
  }

  .academic-item ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .academic-item li {
    margin-bottom: 0.5rem;
  }

  .academic-item a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .academic-item a:hover {
    color: var(--founder);
  }

  .app-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .app-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.925rem;
    transition: color 0.2s ease;
  }

  .app-link:hover {
    color: var(--founder);
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

    .resources-grid {
      grid-template-columns: 1fr;
    }

    .academic-list {
      grid-template-columns: 1fr;
    }
  }
</style>