<script>
	import { fade, fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';

	let mounted = false;

	onMount(() => {
		mounted = true;
	});
</script>

<svelte:head>
	<title>About - BDS Search Platform</title>
	<meta
		name="description"
		content="Learn about the BDS Search Platform, its methodology, data sources, and mission to provide transparency about corporate involvement in activities targeted by BDS campaigns."
	/>
</svelte:head>

{#if mounted}
	<div class="page-container" in:fade={{ duration: 600 }}>
		<!-- Hero Section -->
		<div class="hero-section">
			<div class="hero-content" in:fly={{ y: 30, duration: 800, delay: 200 }}>
				<h1 class="hero-title">About BDS Search</h1>
				<p class="hero-description">
					A comprehensive platform providing transparency about corporate involvement in activities
					targeted by the Boycott, Divestment, Sanctions (BDS) movement.
				</p>
			</div>
		</div>

		<!-- Main Content -->
		<div class="main-content">
			<!-- Mission Section -->
			<section class="content-section" in:fly={{ y: 30, duration: 600, delay: 400 }}>
				<div class="section-header">
					<Icon icon="mdi:target" class="section-icon" />
					<h2 class="section-title">Our Mission</h2>
				</div>
				<div class="section-content">
					<p>
						The BDS Search Platform was created to provide accessible, comprehensive information
						about companies identified by various BDS-related organizations. Our goal is to
						aggregate data from multiple sources to help individuals, organizations, and
						institutions make informed decisions about their investments and purchasing choices.
					</p>
					<p>
						We believe in transparency and the right to information. This platform serves as a
						research tool for those seeking to understand corporate involvement in activities that
						various organizations have identified as problematic under BDS criteria.
					</p>
				</div>
			</section>

			<!-- Methodology Section -->
			<section class="content-section" in:fly={{ y: 30, duration: 600, delay: 500 }}>
				<div class="section-header">
					<Icon icon="mdi:chart-line" class="section-icon" />
					<h2 class="section-title">Methodology</h2>
				</div>
				<div class="section-content">
					<h3>Data Collection</h3>
					<p>
						Our database aggregates information from multiple established BDS-related organizations
						and research institutions. We continuously monitor and update our sources to ensure the
						most current information is available.
					</p>

					<h3>Data Processing</h3>
					<ul>
						<li>
							<strong>Normalization:</strong> Company names and identifiers are standardized across different
							sources
						</li>
						<li>
							<strong>Deduplication:</strong> Advanced fuzzy matching algorithms identify and merge duplicate
							entries
						</li>
						<li>
							<strong>Verification:</strong> Cross-referencing between multiple sources to improve data
							reliability
						</li>
						<li>
							<strong>Confidence Scoring:</strong> Each entry receives a confidence score based on source
							reliability and verification
						</li>
					</ul>

					<h3>Search Technology</h3>
					<p>
						The platform uses PostgreSQL's full-text search capabilities combined with semantic
						matching to provide relevant results across company names, descriptions, industries, and
						involvement types.
					</p>
				</div>
			</section>

			<!-- Data Sources Section -->
			<section class="content-section" in:fly={{ y: 30, duration: 600, delay: 600 }}>
				<div class="section-header">
					<Icon icon="mdi:database" class="section-icon" />
					<h2 class="section-title">Data Sources</h2>
				</div>
				<div class="section-content">
					<div class="sources-grid">
						<div class="source-card">
							<div class="source-header">
								<Icon icon="mdi:web" class="source-icon" />
								<h4>BDS Movement</h4>
							</div>
							<p>Official BDS movement website and coalition information</p>
							<a
								href="https://bdsmovement.net/"
								target="_blank"
								rel="noopener noreferrer"
								class="source-link"
							>
								Visit Source <Icon icon="mdi:open-in-new" class="external-icon" />
							</a>
						</div>

						<div class="source-card">
							<div class="source-header">
								<Icon icon="mdi:magnify" class="source-icon" />
								<h4>AFSC Investigate</h4>
							</div>
							<p>American Friends Service Committee's corporate research database</p>
							<a
								href="https://investigate.afsc.org/"
								target="_blank"
								rel="noopener noreferrer"
								class="source-link"
							>
								Visit Source <Icon icon="mdi:open-in-new" class="external-icon" />
							</a>
						</div>

						<div class="source-card">
							<div class="source-header">
								<Icon icon="mdi:newspaper" class="source-icon" />
								<h4>Boycott.thewitness</h4>
							</div>
							<p>Community-driven platform for tracking boycott targets</p>
							<a
								href="https://boycott.thewitness.news/"
								target="_blank"
								rel="noopener noreferrer"
								class="source-link"
							>
								Visit Source <Icon icon="mdi:open-in-new" class="external-icon" />
							</a>
						</div>

						<div class="source-card">
							<div class="source-header">
								<Icon icon="mdi:chart-pie" class="source-icon" />
								<h4>Who Profits</h4>
							</div>
							<p>Research center documenting corporate involvement in human rights violations</p>
							<a
								href="https://whoprofits.org/"
								target="_blank"
								rel="noopener noreferrer"
								class="source-link"
							>
								Visit Source <Icon icon="mdi:open-in-new" class="external-icon" />
							</a>
						</div>
					</div>
				</div>
			</section>

			<!-- Developer Section -->
			<section class="content-section" in:fly={{ y: 30, duration: 600, delay: 700 }}>
				<div class="section-header">
					<Icon icon="mdi:account" class="section-icon" />
					<h2 class="section-title">Developers</h2>
				</div>
				<div class="section-content">
					<div class="developer-info">
						<div class="developer-text">
							<h3>Stephen Okita</h3>
							<p>
								Rn it's just me Stephen Okita and claude code, I would like friends to help on this
								project. Please.
							</p>
							<div class="developer-links">
								<a
									href="https://stephenokita.com"
									target="_blank"
									rel="noopener noreferrer"
									class="dev-link"
								>
									<Icon icon="mdi:web" />
									Personal Website
								</a>
								<a href="mailto:admin@ucinvestments.info" class="dev-link">
									<Icon icon="mdi:email" />
									Contact Admin
								</a>
							</div>
						</div>
					</div>
				</div>
			</section>

			<!-- Disclaimers Section -->
			<section class="content-section" in:fly={{ y: 30, duration: 600, delay: 800 }}>
				<div class="section-header">
					<Icon icon="mdi:information-outline" class="section-icon" />
					<h2 class="section-title">Important Disclaimers</h2>
				</div>
				<div class="section-content">
					<div class="disclaimer-box">
						<h3>Data Accuracy</h3>
						<p>
							While we strive for accuracy, this platform aggregates data from multiple sources that
							may have different verification standards. Information should be independently
							verified before making important decisions.
						</p>
					</div>

					<div class="disclaimer-box">
						<h3>Educational Purpose</h3>
						<p>
							This platform is intended for educational and research purposes only. It is not
							intended to provide financial, legal, or investment advice.
						</p>
					</div>

					<div class="disclaimer-box">
						<h3>Neutral Aggregation</h3>
						<p>
							The platform aggregates information from various sources without editorial judgment.
							Inclusion in this database does not constitute an endorsement of any particular
							viewpoint or action.
						</p>
					</div>

					<div class="disclaimer-box">
						<h3>Continuous Updates</h3>
						<p>
							Corporate information and involvement status can change rapidly. We update our
							database regularly, but there may be delays in reflecting the most current
							information.
						</p>
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
		content: '';
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
		font-family: 'Space Grotesk', sans-serif;
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
		font-family: 'Space Grotesk', sans-serif;
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

	.section-content ul {
		margin: 1rem 0;
		padding-left: 1.5rem;
	}

	.section-content li {
		margin-bottom: 0.5rem;
	}

	.sources-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.5rem;
		margin-top: 2rem;
	}

	.source-card {
		background: white;
		border: 2px solid var(--border);
		border-radius: 1rem;
		padding: 1.5rem;
		transition: all 0.3s ease;
		box-shadow: var(--shadow-sm);
	}

	.source-card:hover {
		border-color: var(--founder);
		transform: translateY(-4px);
		box-shadow: var(--shadow-lg);
	}

	.source-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	:global(.source-icon) {
		font-size: 1.5rem;
		color: var(--founder);
	}

	.source-card h4 {
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--text-primary);
		margin: 0;
	}

	.source-card p {
		color: var(--text-secondary);
		margin-bottom: 1rem;
	}

	.source-link {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		color: var(--founder);
		text-decoration: none;
		font-weight: 500;
		transition: color 0.2s ease;
	}

	.source-link:hover {
		color: var(--pri);
	}

	:global(.external-icon) {
		font-size: 0.875rem;
	}

	.developer-info {
		background: linear-gradient(135deg, var(--bg-secondary), white);
		border: 1px solid var(--border);
		border-radius: 1rem;
		padding: 2rem;
	}

	.developer-text h3 {
		margin-top: 0;
	}

	.developer-links {
		display: flex;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.dev-link {
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

	.dev-link:hover {
		background: var(--pri);
		transform: translateY(-2px);
	}

	.disclaimer-box {
		background: var(--bg-secondary);
		border: 1px solid var(--border);
		border-radius: 0.75rem;
		padding: 1.5rem;
		margin-bottom: 1rem;
	}

	.disclaimer-box h3 {
		margin-top: 0;
		margin-bottom: 1rem;
		color: var(--pri);
	}

	.disclaimer-box p {
		margin: 0;
		color: var(--text-secondary);
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

		.sources-grid {
			grid-template-columns: 1fr;
		}

		.developer-links {
			flex-direction: column;
		}

		.dev-link {
			justify-content: center;
		}
	}
</style>
