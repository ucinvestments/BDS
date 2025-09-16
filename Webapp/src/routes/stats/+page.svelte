<script>
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";

  let mounted = false;
  let stats = null;
  let loading = true;

  async function loadStats() {
    try {
      const response = await fetch('/api/stats');
      stats = await response.json();
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    mounted = true;
    loadStats();
  });
</script>

<svelte:head>
  <title>Statistics - BDS Search Platform</title>
  <meta name="description" content="Statistical overview of the BDS Search Platform database including company counts, data sources, and involvement types." />
</svelte:head>

{#if mounted}
  <div class="page-container" in:fade={{ duration: 600 }}>
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content" in:fly={{ y: 30, duration: 800, delay: 200 }}>
        <h1 class="hero-title">Database Statistics</h1>
        <p class="hero-description">
          Overview of the companies, data sources, and categories in our comprehensive BDS database.
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      {#if loading}
        <div class="loading-section" in:fade={{ duration: 400 }}>
          <Icon icon="mdi:loading" class="loading-icon animate-spin" />
          <p>Loading statistics...</p>
        </div>
      {:else if stats}
        <!-- Overview Stats -->
        <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 400 }}>
          <div class="section-header">
            <Icon icon="mdi:chart-bar" class="section-icon" />
            <h2 class="section-title">Overview</h2>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon-container">
                <Icon icon="mdi:office-building" class="stat-icon" />
              </div>
              <div class="stat-content">
                <div class="stat-number">{stats.totalCompanies?.toLocaleString() || '0'}</div>
                <div class="stat-label">Total Companies</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon-container">
                <Icon icon="mdi:database" class="stat-icon" />
              </div>
              <div class="stat-content">
                <div class="stat-number">{stats.totalSources || '0'}</div>
                <div class="stat-label">Data Sources</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon-container">
                <Icon icon="mdi:tag-multiple" class="stat-icon" />
              </div>
              <div class="stat-content">
                <div class="stat-number">{stats.involvementTypes?.length || '0'}</div>
                <div class="stat-label">Involvement Types</div>
              </div>
            </div>
          </div>
        </section>

        <!-- Involvement Types -->
        {#if stats.involvementTypes && stats.involvementTypes.length > 0}
          <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 500 }}>
            <div class="section-header">
              <Icon icon="mdi:tag" class="section-icon" />
              <h2 class="section-title">Involvement Types</h2>
            </div>
            <div class="involvement-grid">
              {#each stats.involvementTypes as type}
                <div class="involvement-card">
                  <div class="involvement-name">{type.involvement_type.replace('_', ' ')}</div>
                  <div class="involvement-count">{type.count} companies</div>
                  <div class="involvement-bar">
                    <div
                      class="involvement-fill"
                      style="width: {(type.count / stats.involvementTypes[0].count) * 100}%"
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          </section>
        {/if}

        <!-- Top Countries -->
        {#if stats.topCountries && stats.topCountries.length > 0}
          <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 600 }}>
            <div class="section-header">
              <Icon icon="mdi:earth" class="section-icon" />
              <h2 class="section-title">Top Countries by Headquarters</h2>
            </div>
            <div class="countries-grid">
              {#each stats.topCountries as country}
                <div class="country-card">
                  <div class="country-info">
                    <div class="country-name">{country.country_hq}</div>
                    <div class="country-count">{country.count} companies</div>
                  </div>
                  <div class="country-bar">
                    <div
                      class="country-fill"
                      style="width: {(country.count / stats.topCountries[0].count) * 100}%"
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          </section>
        {/if}

        <!-- Top Industries -->
        {#if stats.topIndustries && stats.topIndustries.length > 0}
          <section class="content-section" in:fly={{ y: 30, duration: 600, delay: 700 }}>
            <div class="section-header">
              <Icon icon="mdi:factory" class="section-icon" />
              <h2 class="section-title">Top Industries</h2>
            </div>
            <div class="industries-grid">
              {#each stats.topIndustries as industry}
                <div class="industry-card">
                  <div class="industry-info">
                    <div class="industry-name">{industry.industry}</div>
                    <div class="industry-count">{industry.count} companies</div>
                  </div>
                  <div class="industry-bar">
                    <div
                      class="industry-fill"
                      style="width: {(industry.count / stats.topIndustries[0].count) * 100}%"
                    ></div>
                  </div>
                </div>
              {/each}
            </div>
          </section>
        {/if}

      {:else}
        <div class="error-section" in:fade={{ duration: 400 }}>
          <Icon icon="mdi:alert-circle" class="error-icon" />
          <p>Unable to load statistics. Please try again later.</p>
        </div>
      {/if}
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

  .loading-section, .error-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
    color: var(--text-secondary);
  }

  :global(.loading-icon), :global(.error-icon) {
    font-size: 3rem;
    color: var(--founder);
    margin-bottom: 1rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }

  .stat-card {
    background: white;
    border: 2px solid var(--border);
    border-radius: 1rem;
    padding: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .stat-card:hover {
    border-color: var(--founder);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .stat-icon-container {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    border-radius: 1rem;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  :global(.stat-icon) {
    font-size: 2rem;
    color: white;
  }

  .stat-number {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--pri);
    line-height: 1;
  }

  .stat-label {
    font-size: 0.925rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-top: 0.25rem;
  }

  .involvement-grid, .countries-grid, .industries-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
  }

  .involvement-card, .country-card, .industry-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 1.5rem;
    transition: all 0.3s ease;
  }

  .involvement-card:hover, .country-card:hover, .industry-card:hover {
    border-color: var(--founder);
    box-shadow: var(--shadow-md);
  }

  .involvement-name, .country-name, .industry-name {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    text-transform: capitalize;
  }

  .involvement-count, .country-count, .industry-count {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }

  .involvement-bar, .country-bar, .industry-bar {
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 4px;
    overflow: hidden;
  }

  .involvement-fill {
    height: 100%;
    background: linear-gradient(135deg, var(--founder), var(--pri));
    transition: width 0.8s ease;
  }

  .country-fill {
    height: 100%;
    background: linear-gradient(135deg, var(--soybean), var(--medalist));
    transition: width 0.8s ease;
  }

  .industry-fill {
    height: 100%;
    background: linear-gradient(135deg, var(--lawrence), var(--founder));
    transition: width 0.8s ease;
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

    .stats-grid {
      grid-template-columns: 1fr;
    }

    .stat-card {
      flex-direction: column;
      text-align: center;
    }

    .involvement-grid, .countries-grid, .industries-grid {
      grid-template-columns: 1fr;
    }
  }
</style>