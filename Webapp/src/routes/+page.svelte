<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { quintOut } from "svelte/easing";

  let mounted = false;
  let searchTerm = "";
  let companies = [];
  let selectedCompany = null;
  let loading = false;
  let suggestions = [];
  let showSuggestions = false;
  let stats = null;
  let currentPage = 1;
  let totalPages = 1;
  let totalCompanies = 0;
  let showModal = false;
  let modalCompany = null;

  const API_BASE = "/api";

  // Search functionality
  async function performSearch(page = 1) {
    if (!searchTerm.trim() && page === 1) {
      await loadCompanies(page);
      return;
    }

    loading = true;
    try {
      const response = await fetch(
        `${API_BASE}/companies?search=${encodeURIComponent(searchTerm)}&page=${page}&limit=20`
      );
      const data = await response.json();

      companies = data.companies || [];
      currentPage = data.pagination?.page || 1;
      totalPages = data.pagination?.totalPages || 1;
      totalCompanies = data.pagination?.total || 0;

      if (companies.length > 0 && !selectedCompany) {
        selectedCompany = companies[0];
      }
    } catch (error) {
      console.error("Search error:", error);
      companies = [];
    } finally {
      loading = false;
    }
  }

  // Load companies with pagination
  async function loadCompanies(page = 1) {
    loading = true;
    try {
      const response = await fetch(`${API_BASE}/companies?page=${page}&limit=20`);
      const data = await response.json();

      companies = data.companies || [];
      currentPage = data.pagination?.page || 1;
      totalPages = data.pagination?.totalPages || 1;
      totalCompanies = data.pagination?.total || 0;

      if (companies.length > 0 && !selectedCompany) {
        selectedCompany = companies[0];
      }
    } catch (error) {
      console.error("Error loading companies:", error);
      companies = [];
    } finally {
      loading = false;
    }
  }

  // Get search suggestions
  async function getSuggestions() {
    if (searchTerm.length < 2) {
      suggestions = [];
      showSuggestions = false;
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE}/search/suggestions?q=${encodeURIComponent(searchTerm)}`
      );
      suggestions = await response.json();
      showSuggestions = suggestions.length > 0;
    } catch (error) {
      console.error("Error getting suggestions:", error);
      suggestions = [];
      showSuggestions = false;
    }
  }

  // Load statistics
  async function loadStats() {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      stats = await response.json();
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  }

  // Handle search input
  function handleSearchInput() {
    getSuggestions();

    // Debounce search
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      performSearch();
    }, 300);
  }

  let searchTimeout;

  // Handle suggestion selection
  function selectSuggestion(suggestion) {
    searchTerm = suggestion.name;
    showSuggestions = false;
    performSearch();
  }

  // Handle company selection
  async function selectCompany(company) {
    try {
      // Fetch detailed company information
      const response = await fetch(`${API_BASE}/companies/${company.id}`);
      modalCompany = await response.json();
      showModal = true;
    } catch (error) {
      console.error('Error fetching company details:', error);
    }
  }

  // Close modal
  function closeModal() {
    showModal = false;
    modalCompany = null;
  }

  // Format numbers
  function formatNumber(num) {
    if (!num) return "0";
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  // Capitalize text
  function cap(s) {
    if (s && typeof s === "string") {
      return s
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
    }
    return "";
  }

  // Handle pagination
  function goToPage(page) {
    if (page >= 1 && page <= totalPages) {
      currentPage = page;
      performSearch(page);
    }
  }

  onMount(() => {
    mounted = true;
    loadCompanies();
    loadStats();
  });
</script>


<!-- Hero Section -->
<div class="hero-section">
  {#if mounted}
    <div class="hero-content" in:fade={{ duration: 800, delay: 200 }}>
      <h1 class="hero-title">BDS Search Platform</h1>
      {#if stats}
        <div class="hero-stats">
          <div class="stat-item" in:fade={{ duration: 600, delay: 400 }}>
            <span class="stat-value">{formatNumber(stats.totalCompanies)}</span>
            <span class="stat-divider">•</span>
            <span class="stat-label">Companies</span>
          </div>
          <div class="stat-item" in:fade={{ duration: 600, delay: 500 }}>
            <span class="stat-value">{stats.totalSources}</span>
            <span class="stat-divider">•</span>
            <span class="stat-label">Sources</span>
          </div>
          <div class="stat-item" in:fade={{ duration: 600, delay: 600 }}>
            <span class="stat-value">{stats.involvementTypes?.length || 0}</span>
            <span class="stat-divider">•</span>
            <span class="stat-label">Categories</span>
          </div>
        </div>
      {/if}
      <p class="hero-description" in:fade={{ duration: 800, delay: 700 }}>
        Search and explore companies involved in activities targeted by BDS campaigns with semantic search capabilities.
      </p>
    </div>
  {/if}
</div>

{#if mounted}
  <div class="main-container" in:fade={{ duration: 600 }}>
    <!-- Search Section -->
    <div class="search-section" in:fly={{ y: 20, duration: 500, delay: 300 }}>
      <div class="search-wrapper">
        <Icon icon="mdi:magnify" class="search-icon" />
        <input
          type="text"
          placeholder="Search companies, industries, involvement types..."
          bind:value={searchTerm}
          on:input={handleSearchInput}
          on:focus={() => showSuggestions = suggestions.length > 0}
          on:blur={() => setTimeout(() => showSuggestions = false, 200)}
          class="search-input"
        />
        {#if searchTerm}
          <button on:click={() => { searchTerm = ""; performSearch(); }} class="clear-btn">
            <Icon icon="mdi:close" />
          </button>
        {/if}

        <!-- Search Suggestions -->
        {#if showSuggestions && suggestions.length > 0}
          <div class="suggestions-dropdown" in:fade={{ duration: 200 }}>
            {#each suggestions as suggestion}
              <button
                class="suggestion-item"
                on:click={() => selectSuggestion(suggestion)}
              >
                <Icon icon="mdi:company" class="suggestion-icon" />
                {suggestion.name}
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <!-- Results Info -->
    {#if !loading}
      <div class="results-info" in:fade={{ duration: 400 }}>
        <span>
          Showing {companies.length} of {formatNumber(totalCompanies)} companies
          {#if searchTerm}for "{searchTerm}"{/if}
        </span>
      </div>
    {/if}

    <!-- Companies Grid -->
    <div class="companies-section" in:fly={{ y: 20, duration: 600, delay: 400 }}>
      {#if loading}
        <div class="loading-message">
          <Icon icon="mdi:loading" class="loading-icon animate-spin" />
          <p>Searching companies...</p>
        </div>
      {:else if companies.length === 0}
        <div class="no-results">
          <Icon icon="mdi:information-outline" class="no-results-icon" />
          <p>No companies found. Try adjusting your search terms.</p>
        </div>
      {:else}
        <div class="companies-grid">
          {#each companies as company (company.id)}
            <div
              class="company-card"
              on:click={() => selectCompany(company)}
              in:fade={{ duration: 300 }}
            >
              <div class="company-header">
                <h4 class="company-name">{cap(company.name)}</h4>
              </div>

              {#if company.industry}
                <p class="company-industry">{company.industry}</p>
              {/if}

              {#if company.country_hq}
                <p class="company-location">
                  <Icon icon="mdi:map-marker" class="location-icon" />
                  {company.country_hq}
                </p>
              {/if}

              {#if company.involvement_types && company.involvement_types.length > 0}
                <div class="involvement-tags">
                  {#each company.involvement_types.slice(0, 2) as type}
                    <span class="involvement-tag">{cap(type.replace('_', ' '))}</span>
                  {/each}
                  {#if company.involvement_types.length > 2}
                    <span class="involvement-tag more">+{company.involvement_types.length - 2}</span>
                  {/if}
                </div>
              {/if}

              <div class="card-action">
                <span class="view-details">View Details</span>
                <Icon icon="mdi:arrow-right" class="arrow-icon" />
              </div>
            </div>
          {/each}
        </div>

        <!-- Pagination -->
        {#if totalPages > 1}
          <div class="pagination">
            <button
              class="pagination-btn"
              disabled={currentPage <= 1}
              on:click={() => goToPage(currentPage - 1)}
            >
              <Icon icon="mdi:chevron-left" />
              Previous
            </button>

            <div class="pagination-info">
              Page {currentPage} of {totalPages}
            </div>

            <button
              class="pagination-btn"
              disabled={currentPage >= totalPages}
              on:click={() => goToPage(currentPage + 1)}
            >
              Next
              <Icon icon="mdi:chevron-right" />
            </button>
          </div>
        {/if}
      {/if}
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer" in:fade={{ duration: 600, delay: 500 }}>
      <Icon icon="mdi:information-outline" class="disclaimer-icon" />
      <p>
        This database aggregates information from multiple BDS-related sources including
        BDS Coalition, AFSC Investigate, and Boycott.thewitness. Data is provided for
        informational purposes. Please verify information independently before making decisions.
      </p>
    </div>
  </div>
{/if}

<!-- Company Details Modal -->
{#if showModal && modalCompany}
  <div class="modal-overlay" on:click={closeModal} in:fade={{ duration: 300 }}>
    <div class="modal-content" on:click|stopPropagation in:fly={{ y: 50, duration: 400 }}>
      <div class="modal-header">
        <h2 class="modal-title">{cap(modalCompany.name)}</h2>
        <button class="modal-close" on:click={closeModal}>
          <Icon icon="mdi:close" />
        </button>
      </div>

      <div class="modal-body">

        {#if modalCompany.description}
          <div class="modal-section">
            <h4 class="section-label">Description</h4>
            <p class="section-text">{modalCompany.description}</p>
          </div>
        {/if}

        <div class="info-grid">
          {#if modalCompany.industry}
            <div class="info-item">
              <span class="info-label">Industry</span>
              <span class="info-value">{modalCompany.industry}</span>
            </div>
          {/if}

          {#if modalCompany.country_hq}
            <div class="info-item">
              <span class="info-label">Headquarters</span>
              <span class="info-value">{modalCompany.country_hq}</span>
            </div>
          {/if}

          {#if modalCompany.parent_company}
            <div class="info-item">
              <span class="info-label">Parent Company</span>
              <span class="info-value">{modalCompany.parent_company}</span>
            </div>
          {/if}
        </div>

        {#if modalCompany.involvement_types && modalCompany.involvement_types.length > 0}
          <div class="modal-section">
            <h4 class="section-label">Involvement Types</h4>
            <div class="tags-grid">
              {#each modalCompany.involvement_types as type}
                <span class="involvement-badge">{cap(type.replace('_', ' '))}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if modalCompany.stock_symbols && modalCompany.stock_symbols.length > 0 && modalCompany.stock_symbols[0].symbol}
          <div class="modal-section">
            <h4 class="section-label">Stock Information</h4>
            <div class="stock-grid">
              {#each modalCompany.stock_symbols as stock}
                <div class="stock-item">
                  <span class="stock-symbol">{stock.symbol}</span>
                  <span class="stock-exchange">{stock.exchange}</span>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        {#if modalCompany.sectors && modalCompany.sectors.length > 0}
          <div class="modal-section">
            <h4 class="section-label">Sectors</h4>
            <div class="tags-grid">
              {#each modalCompany.sectors as sector}
                <span class="sector-tag">{cap(sector)}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if modalCompany.boycott_actions && modalCompany.boycott_actions.length > 0}
          <div class="modal-section">
            <h4 class="section-label">Suggested Boycott Actions</h4>
            <ul class="actions-list">
              {#each modalCompany.boycott_actions as action}
                <li>{action}</li>
              {/each}
            </ul>
          </div>
        {/if}

        {#if modalCompany.alternatives && modalCompany.alternatives.length > 0}
          <div class="modal-section">
            <h4 class="section-label">Alternatives</h4>
            <div class="tags-grid">
              {#each modalCompany.alternatives as alternative}
                <span class="alternative-tag">{alternative}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if modalCompany.data_sources && modalCompany.data_sources.length > 0}
          <div class="modal-section">
            <h4 class="section-label">Data Sources</h4>
            <div class="sources-grid">
              {#each modalCompany.data_sources as source}
                <span class="source-badge">{source}</span>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style lang="postcss">
  :global(body) {
    overflow-x: hidden;
  }


  .hero-section {
    padding: 1.5rem 1rem;
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
    text-align: center;
    position: relative;
    z-index: 1;
  }

  .hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
  }

  .hero-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1rem;
    flex-wrap: nowrap;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: white;
  }

  .stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--sec);
    font-family: "Space Grotesk", sans-serif;
  }

  .stat-divider {
    color: rgba(255, 255, 255, 0.4);
    font-size: 1.25rem;
  }

  .stat-label {
    font-size: 0.925rem;
    color: rgba(255, 255, 255, 0.95);
    font-weight: 500;
  }

  .hero-description {
    max-width: 600px;
    margin: 0 auto;
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.5;
  }

  .main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }

  .search-section {
    margin-bottom: 2rem;
    display: flex;
    justify-content: center;
  }

  .search-wrapper {
    position: relative;
    width: 100%;
    max-width: 600px;
  }

  :global(.search-icon) {
    position: absolute;
    left: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    font-size: 1.25rem;
    z-index: 2;
  }

  .search-input {
    width: 100%;
    padding: 1rem 3.5rem;
    border: 2px solid var(--border);
    border-radius: 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
    box-shadow: var(--shadow-sm);
  }

  .search-input:focus {
    outline: none;
    border-color: var(--founder);
    box-shadow:
      0 0 0 3px rgba(59, 126, 161, 0.1),
      var(--shadow-md);
    transform: translateY(-1px);
  }

  .clear-btn {
    position: absolute;
    right: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    z-index: 2;
  }

  .clear-btn:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }

  .suggestions-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    box-shadow: var(--shadow-lg);
    margin-top: 0.5rem;
    max-height: 300px;
    overflow-y: auto;
    z-index: 100;
  }

  .suggestion-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.75rem 1rem;
    text-align: left;
    border: none;
    background: none;
    cursor: pointer;
    transition: background-color 0.2s ease;
    font-size: 0.925rem;
  }

  .suggestion-item:hover {
    background: var(--bg-secondary);
  }

  .suggestion-item:first-child {
    border-top-left-radius: 0.75rem;
    border-top-right-radius: 0.75rem;
  }

  .suggestion-item:last-child {
    border-bottom-left-radius: 0.75rem;
    border-bottom-right-radius: 0.75rem;
  }

  :global(.suggestion-icon) {
    color: var(--founder);
    font-size: 1rem;
  }

  .results-info {
    margin-bottom: 1.5rem;
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.925rem;
  }

  .companies-section {
    margin-bottom: 2rem;
  }

  .companies-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .company-card {
    padding: 1.5rem;
    border: 2px solid var(--border);
    border-radius: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    overflow: hidden;
  }

  .company-card:hover {
    border-color: var(--founder);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .company-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(135deg, var(--founder), var(--pri));
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .company-card:hover::before {
    opacity: 1;
  }

  .company-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .company-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.2;
  }


  .company-industry {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0 0 0.5rem 0;
  }

  .company-location {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0 0 0.75rem 0;
  }

  :global(.location-icon) {
    font-size: 1rem;
  }

  .involvement-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .involvement-tag {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.25rem 0.5rem;
    border-radius: 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .involvement-tag.more {
    background: var(--founder);
    color: white;
  }

  .card-action {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border);
  }

  .view-details {
    color: var(--founder);
    font-weight: 500;
    font-size: 0.875rem;
  }

  :global(.arrow-icon) {
    color: var(--founder);
    font-size: 1rem;
    transition: transform 0.3s ease;
  }

  .company-card:hover :global(.arrow-icon) {
    transform: translateX(4px);
  }

  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .modal-content {
    background: white;
    border-radius: 1.5rem;
    max-width: 800px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border: 1px solid var(--border);
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem 2rem 1rem;
    border-bottom: 2px solid var(--border);
    position: sticky;
    top: 0;
    background: white;
    border-radius: 1.5rem 1.5rem 0 0;
  }

  .modal-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0;
    line-height: 1.2;
  }

  .modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal-close:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }

  .modal-body {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }


  .modal-section {
    margin-bottom: 1.5rem;
  }

  .section-label {
    display: block;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .section-text {
    color: var(--text-primary);
    line-height: 1.6;
    margin: 0;
  }

  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: 0.5rem;
    border: 1px solid var(--border);
  }

  .info-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .info-value {
    font-weight: 500;
    color: var(--text-primary);
  }

  .tags-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .stock-grid {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
  }

  .pagination-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: white;
    border: 2px solid var(--border);
    border-radius: 0.5rem;
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .pagination-btn:hover:not(:disabled) {
    border-color: var(--founder);
    color: var(--founder);
  }

  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .pagination-info {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }


  .loading-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
    color: var(--text-secondary);
  }

  :global(.loading-icon) {
    font-size: 2rem;
    color: var(--founder);
    margin-bottom: 1rem;
  }

  .no-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
    color: var(--text-secondary);
  }

  :global(.no-results-icon) {
    font-size: 3rem;
    color: var(--border);
    margin-bottom: 1rem;
  }


  .involvement-badge {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 500;
  }


  .stock-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 1rem;
    background: var(--bg-secondary);
    border-radius: 0.5rem;
  }

  .stock-symbol {
    font-weight: 600;
    color: var(--founder);
    font-family: "Space Grotesk", sans-serif;
  }

  .stock-exchange {
    color: var(--text-secondary);
    font-size: 0.875rem;
  }


  .sector-tag {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.375rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    border: 1px solid var(--border);
  }

  .actions-list {
    margin: 0;
    padding-left: 1.5rem;
  }

  .actions-list li {
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }


  .alternative-tag {
    background: linear-gradient(135deg, var(--soybean), var(--medalist));
    color: white;
    padding: 0.375rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
  }


  .source-badge {
    background: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 0.375rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    border: 1px solid var(--border);
  }

  .disclaimer {
    display: flex;
    gap: 1rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1rem;
    border: 1px solid var(--border);
    margin-top: 2rem;
  }

  :global(.disclaimer-icon) {
    flex-shrink: 0;
    color: var(--founder);
    font-size: 1.5rem;
    margin-top: 0.125rem;
  }

  .disclaimer p {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.925rem;
    margin: 0;
  }

  @media (max-width: 1024px) {
    .companies-grid {
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .hero-stats {
      gap: 1.5rem;
    }

    .stat-value {
      font-size: 1.25rem;
    }

    .main-container {
      padding: 1.5rem 1rem;
    }

    .modal-overlay {
      padding: 1rem;
    }

    .modal-content {
      max-height: 95vh;
    }

    .modal-header, .modal-body {
      padding: 1.5rem;
    }
  }

  @media (max-width: 768px) {
    .companies-grid {
      grid-template-columns: 1fr;
    }

    .search-input {
      padding: 0.875rem 3rem 0.875rem 2.5rem;
      font-size: 0.925rem;
    }

    .modal-title {
      font-size: 1.25rem;
    }

    .info-grid {
      grid-template-columns: 1fr;
    }

    .modal-overlay {
      padding: 0.5rem;
    }

    .modal-header, .modal-body {
      padding: 1rem;
    }
  }

  @media (max-width: 640px) {
    .hero-section {
      padding: 1rem 0.75rem;
    }

    .hero-title {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
    }

    .hero-stats {
      flex-direction: column;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
    }

    .stat-item {
      justify-content: center;
    }

    .stat-value {
      font-size: 1.125rem;
    }

    .stat-label {
      font-size: 0.875rem;
    }

    .hero-description {
      font-size: 0.925rem;
      padding: 0 0.5rem;
    }


    .main-container {
      padding: 1rem 0.75rem;
    }

    .search-section {
      margin-bottom: 1.5rem;
    }

    .search-input {
      padding: 0.75rem 2.5rem 0.75rem 2rem;
      font-size: 0.875rem;
    }


    .disclaimer {
      flex-direction: column;
      gap: 0.75rem;
      padding: 1rem;
      margin-top: 1rem;
    }

    .disclaimer p {
      font-size: 0.875rem;
    }

    .pagination {
      flex-direction: column;
      gap: 1rem;
    }

    .pagination-btn {
      width: 100%;
      justify-content: center;
    }
  }
</style>
